# telebot

telebot is a Telegram bot that allows you to monitor the parameters of a remote server using SSH, search for phone numbers and emails in text, record detected data into a database, as well as output data from a database.

You can use it as bot.py to work on the host, both Dockerfile or docker-compose.yaml for running the bot and databases.

For this bot to work, you need to create a .env file and put the following variables in it:

`HOST`=IP of the monitoring host

`PORT`=Host port for monitoring

`USER`=SSH user on the monitoring host

`PASSWORD`=SSH user password on the monitoring host

`PASSWORD_REPL`=The user's password for replication

`HOST_PG`=Database IP address

`PORT_PG`=Database port

`USER_PG`=Database User

`PASSWORD_PG`=Password of the database user

`DB_PG`=Name of the database

`TOKEN`=A token for a telegram bot