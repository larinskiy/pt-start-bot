#!/bin/bash
sleep 20
DB_BIN_PATH=`pg_config --bindir`
/$DB_BIN_PATH/pg_ctl stop
rm -rf /var/lib/postgresql/data/*
pg_basebackup -R -h db -U $DB_REPL_USER -D /var/lib/postgresql/data -P
/$DB_BIN_PATH/pg_ctl start