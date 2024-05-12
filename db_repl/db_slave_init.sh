#!/bin/bash
sleep 20
pg_ctl stop
rm -rf /var/lib/postgresql/data/*
pg_basebackup -R -h db -U $DB_REPL_USER -D /var/lib/postgresql/data -P
pg_ctl start