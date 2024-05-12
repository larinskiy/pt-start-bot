#!/bin/bash

#Настроить БД
sed -i "s/^#*\(log_replication_commands *= *\).*/\1on/" /var/lib/postgresql/data/postgresql.conf
sed -i "s/^#*\(archive_mode *= *\).*/\1on/" /var/lib/postgresql/data/postgresql.conf
sed -i "s|^#*\(archive_command *= *\).*|\1'cp %p /pg_data/archive/%f'|" /var/lib/postgresql/data/postgresql.conf
sed -i "s/^#*\(max_wal_senders *= *\).*/\110/" /var/lib/postgresql/data/postgresql.conf
sed -i "s/^#*\(wal_level *= *\).*/\1replica/" /var/lib/postgresql/data/postgresql.conf
sed -i "s/^#*\(wal_log_hints *= *\).*/\1on/" /var/lib/postgresql/data/postgresql.conf
sed -i "s/^#*\(logging_collector *= *\).*/\1on/" /var/lib/postgresql/data/postgresql.conf
sed -i -e"s/^#log_filename = 'postgresql-\%Y-\%m-\%d_\%H\%M\%S.log'.*$/log_filename = 'postgresql.log'/" /var/lib/postgresql/data/postgresql.conf
sed -i "s/#log_line_prefix = '%m \[%p\] '/log_line_prefix = '%m [%p] %q%u@%d '/g" /var/lib/postgresql/data/postgresql.conf

mkdir -p /pg_data/archive

psql -c "CREATE USER $DB_REPL_USER WITH REPLICATION LOGIN PASSWORD '$DB_REPL_PASSWORD';" #Создать пользователя репликатора
psql -c "CREATE DATABASE $DB_DATABASE;" #Создать пользователя репликатора
psql -d $DB_DATABASE -a -f /init.sql #Создать таблицы с данными в БД
psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" #Создать пользователя БД
psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_DATABASE TO $DB_USER;" #Дать пользователю права на БД
psql -d $DB_DATABASE -c "ALTER TABLE Emails OWNER TO $DB_USER;"
psql -d $DB_DATABASE -c "ALTER TABLE Phones OWNER TO $DB_USER;"

#Добавить правила доступа к БД
echo "host replication $DB_REPL_USER 0.0.0.0/0 trust" >> /var/lib/postgresql/data/pg_hba.conf #Разрешить подключение репликатора
echo "host all $DB_USER bot trust" >> /var/lib/postgresql/data/pg_hba.conf #Разрешить подключение бота

#Перезапустить БД
pg_ctl restart