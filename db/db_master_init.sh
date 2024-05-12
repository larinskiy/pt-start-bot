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

#Создать пользователя репликации
psql -c "CREATE USER repl_user WITH REPLICATION LOGIN PASSWORD '$PASSWORD_REPL';" #Создать пользователя репликатора

#Добавить правила доступа к БД
echo 'host replication repl_user 0.0.0.0/0 trust' >> /var/lib/postgresql/data/pg_hba.conf #Разрешить подключение репликатора
echo 'host all postgres bot trust' >> /var/lib/postgresql/data/pg_hba.conf #Разрешить подключение бота

#Перезапустить БД
pg_ctl restart