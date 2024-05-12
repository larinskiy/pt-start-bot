FROM postgres:latest
ENV POSTGRES_DB db_bot
COPY ./db_slave_init.sh /docker-entrypoint-initdb.d/init.sh
RUN chmod +x /docker-entrypoint-initdb.d/init.sh