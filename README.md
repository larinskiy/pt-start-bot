# telebot

telebot is a Telegram bot that allows you to monitor the parameters of a remote server using SSH, search for phone numbers and emails in text, record detected data into a database, as well as output data from a database.

You can use it as bot.py to work on the host, both Dockerfile or docker-compose.yaml for running the bot and databases.

For this bot to work, you need to create a .env file and put the following variables in it:

`HOST`=IP of the monitoring host

`PORT`=Host port for monitoring

`USER`=SSH user on the monitoring host

`PASSWORD`=SSH user password on the monitoring host

`DB_REPL_PASSWORD`=The user's password for replication

`DB_HOST`=Database IP address

`DB_PORT`=Database port

`DB_USER`=Database User

`DB_PASSWORD`=Password of the database user

`DB_DATABASE`=Name of the database

`TOKEN`=A token for a telegram bot