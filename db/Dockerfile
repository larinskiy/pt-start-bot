FROM postgres:latest
ENV POSTGRES_DB db_bot
COPY ./db_master_init.sh /docker-entrypoint-initdb.d/init.sh
COPY ./db_master_init.sql /docker-entrypoint-initdb.d/init.sql
RUN chmod +x /docker-entrypoint-initdb.d/init.sh