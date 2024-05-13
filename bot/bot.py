import paramiko
import psycopg2
import telebot
import re
import logging
import os
from psycopg2 import Error

# Инициализация логирования
logging.basicConfig(
    filename='logfile.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

# Учетные данные сервера
host = os.getenv('RM_HOST')
port = os.getenv('RM_PORT')
username = os.getenv('RM_USER')
password = os.getenv('RM_PASSWORD')

# Учетные данные для бд
host_pg = os.getenv('DB_HOST')
port_pg = os.getenv('DB_PORT')
username_pg = os.getenv('DB_USER')
password_pg = os.getenv('DB_PASSWORD')
db = os.getenv('DB_DATABASE')
db_repl_user = os.getenv('DB_REPL_USER')

# Токен ТГ
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)

# Функция для работы с SSH


def paramikoExec(command, host=host, port=port, username=username, password=password):
    print()
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port, username, password)
    stdin, stdout, stderr = client.exec_command(command)
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    return data

# Функция для работы с БД


def dbExec(command, data=None):
    connection = None
    try:
        connection = psycopg2.connect(user=username_pg,
                                      password=password_pg,
                                      host=host_pg,
                                      port=port_pg,
                                      database=db)
        cursor = connection.cursor()
        if data:
            for d in data:
                cursor.execute(command, (d, ))
            connection.commit()
            logging.info("Команда успешно выполнена")
            return ('Данные были успешно записаны')
        else:
            cursor.execute(command)
            data = cursor.fetchall()
            logging.info("Команда успешно выполнена")
            if len(data):
                return data
            else:
                return 0
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
        return -1
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

# Приветствие (/start)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.username}!")

# Поиск почты (/find_email)


@bot.message_handler(commands=['find_email'])
def find_email(message):
    bot.send_message(
        message.chat.id, f"Введите текст, в котором необходимо найти почтовые адреса")
    bot.register_next_step_handler(message, find_email_handler)

# Обработка вывода поиска почт


def find_email_handler(message):
    emailRegex = re.compile(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
    el = emailRegex.findall(message.text)
    if el:
        answer = 'Обнаруженные почтовые адреса:\n'
        for i in range(len(el)):
            answer += f'{i+1}. {el[i]}\n'
        answer += '\nУкажите /write, если вы хотите записать найденные данные в БД, или /skip для пропуска записи'
        bot.register_next_step_handler(message, db_write_handler_email, el)
    else:
        answer = 'Не удалось найти почтовых адресов'
    bot.send_message(message.chat.id, answer)

# Обработка записи почт в БД


def db_write_handler_email(message, el):
    if message.text == "/write":
        bot.send_message(message.chat.id, dbExec(
            "INSERT INTO Emails VALUES (DEFAULT, %s);", el))
    else:
        bot.send_message(message.chat.id, "Данные в БД не были записаны")

# Поиск телефона


@bot.message_handler(commands=['find_phone_number'])
def find_phone_number(message):
    bot.send_message(
        message.chat.id, f"Введите текст, в котором необходимо найти телефонные номера")
    bot.register_next_step_handler(message, find_phone_number_handler)

# Обработка вывода поиска номеров


def find_phone_number_handler(message):
    phoneRegex = re.compile(
        r'(?:(?:8|\+7)[\- ]?)?\(?:?\d{3,5}\)?[\- ]?\d{1}[\- ]?\d{1}[\- ]?\d{1}[\- ]?\d{1}[\- ]?\d{1}(?:(?:[\- ]?\d{1})?[\- ]?\d{1})?')
    nl = phoneRegex.findall(message.text)
    if nl:
        answer = 'Обнаруженные телефонные номера:\n'
        for i in range(len(nl)):
            answer += f'{i + 1}. {nl[i]}\n'
        answer += '\nУкажите /write, если вы хотите записать найденные данные в БД, или /skip для пропуска записи'
        bot.register_next_step_handler(message, db_write_handler, nl)
    else:
        answer = 'Не удалось найти телефонных номеров'
    bot.send_message(message.chat.id, answer)

# Обработчик записи в бд


def db_write_handler(message, nl):
    if message.text == "/write":
        bot.send_message(message.chat.id, dbExec(
            "INSERT INTO Phones VALUES (DEFAULT, %s);", nl))
    else:
        bot.send_message(message.chat.id, "Данные в БД не были записаны")

# Проверка сложности пароля


@bot.message_handler(commands=['verify_password'])
def find_phone_number(message):
    bot.send_message(
        message.chat.id, f"Введите пароль, который нужно проверить на сложность")
    bot.register_next_step_handler(message, verify_password_handler)


def verify_password_handler(message):
    passRegex = re.compile(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()])[A-Za-z\d!@#$%^&*()]{8,}$')
    ps = passRegex.match(message.text)
    if ps is None:
        answer = 'Пароль простой'
    else:
        answer = 'Пароль сложный'
    bot.send_message(message.chat.id, answer)

# Релиз


@bot.message_handler(commands=['get_release'])
def uname_r(message):
    bot.send_message(message.chat.id, paramikoExec('uname -r'))

# Релиз (другой)


@bot.message_handler(commands=['get_uname'])
def uname_mnv(message):
    bot.send_message(message.chat.id, paramikoExec('uname -mnv'))

# Время работы


@bot.message_handler(commands=['get_uptime'])
def uptime(message):
    bot.send_message(message.chat.id, paramikoExec('uptime'))

# Файловая система


@bot.message_handler(commands=['get_df'])
def df(message):
    bot.send_message(message.chat.id, paramikoExec('df -h'))

# Состояние ОП


@bot.message_handler(commands=['get_free'])
def free(message):
    bot.send_message(message.chat.id, paramikoExec('free -h'))

# Производительность системы


@bot.message_handler(commands=['get_mpstat'])
def mpstat(message):
    bot.send_message(message.chat.id, paramikoExec('mpstat'))

# Активные пользователи


@bot.message_handler(commands=['get_w'])
def w(message):
    bot.send_message(message.chat.id, paramikoExec('w'))

# Последние 10 входов


@bot.message_handler(commands=['get_auths'])
def last(message):
    bot.send_message(message.chat.id, paramikoExec('last -5'))

# Последние 5 критических логов


@bot.message_handler(commands=['get_critical'])
def journalctl(message):
    bot.send_message(message.chat.id, paramikoExec(
        'journalctl -p 2 --since yesterday | tail -5'))

# Сведения о процессах


@bot.message_handler(commands=['get_ps'])
def ps(message):
    bot.send_message(message.chat.id, paramikoExec('ps au'))

# Сведения об используемых портах


@bot.message_handler(commands=['get_ss'])
def ss(message):
    bot.send_message(message.chat.id, paramikoExec('ss -tO --ipv4'))

# Сведения об установленных пакетах


@bot.message_handler(commands=['get_apt_list'])
def apt_list(message):
    if len(message.text.split()) == 1:
        result = paramikoExec('apt list --installed')
        for x in range(0, len(result), 4096):
            bot.send_message(message.chat.id, result[x:x+4096])
    else:
        request = message.text.split()[1].replace('&', '').replace(';', '')
        result = paramikoExec(f'apt info {request}')
        print(f'apt info {message.text.split()[1:]}')
        for x in range(0, len(result), 4096):
            bot.send_message(message.chat.id, result[x:x+4096])

# Сведения о сервисах


@bot.message_handler(commands=['get_services'])
def services(message):
    result = paramikoExec('systemctl list-units --type=service')
    for x in range(0, len(result), 4096):
        bot.send_message(message.chat.id, result[x:x+4096])

# Вывод логов репликации


@bot.message_handler(commands=['get_repl_logs'])
def get_repl_logs(message):
    data = dbExec("SELECT pg_read_file(pg_current_logfile());")[0][0].replace(
        '\\n', '\n').replace('\\t', '\t')[2:-1]
    answer = 'Логи репликации:\n'
    for str in data.split('\n'):
        if db_repl_user in str:
            answer += str + '\n'
    if len(answer) == 17:
        answer = 'События репликации не обнаружены'
    for x in range(0, len(answer), 4096):
        bot.send_message(message.chat.id, answer[x:x+4096])

# Вывод почтовых адресов из БД


@bot.message_handler(commands=['get_emails'])
def get_emails(message):
    data = dbExec('SELECT Email FROM Emails;')
    if data == -1:
        answer = 'Произошла ошибка при работе с базой данных'
    elif data == 0:
        answer = 'В базе данных отсутствуют почтовые адреса'
    else:
        answer = 'Почтовые адреса в базе данных:\n'
        i = 1
        for email in data:
            answer += f'{i}. {email[0]}\n'
            i += 1
    bot.send_message(message.chat.id, answer)

# Вывод телефонных номеров из БД


@bot.message_handler(commands=['get_phone_numbers'])
def get_phone_numbers(message):
    data = dbExec('SELECT Phone FROM Phones;')
    if data == -1:
        answer = 'Произошла ошибка при работе с базой данных'
    elif data == 0:
        answer = 'В базе данных отсутствуют телефонные номера'
    else:
        answer = 'Телефонные номера в базе данных:\n'
        i = 1
        for num in data:
            answer += f'{i}. {num[0]}\n'
            i += 1
    bot.send_message(message.chat.id, answer)


bot.polling(none_stop=True)
