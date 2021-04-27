import os

import telebot

import config

TOKEN = os.environ.get('TOKEN') or config.TGBOT_TOKEN
bot = telebot.TeleBot(TOKEN)
logger = config.setup_log()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, '欢迎使用Odyssey_机器人路易\n'
                                      '输入 /help 可以获得更多帮助\n'
                                      '输入 /register 可以注册账号\n'
                                      '输入 /status 可以查看服务器状态\n'
                                      '输入 /reset 可以重置个人账号密码\n'
                                      '输入 /delete 可以删除个人账号')


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, '欢迎使用Odyssey机器人路易，这是我们的帮助手册：\n'
                                      '输入 /register 可以注册账号\n'
                                      '输入 /status 可以查看服务器状态\n'
                                      '输入 /reset 可以重置个人账号密码\n'
                                      '输入 /delete 可以删除个人账号')


# @bot.message_handler(commands=['status'])
# def send_status(message):
#     url1 = "https://shogouki.youremby.gq:443"
#     url2 = "http://aga01.youremby.gq:8096"
#     ip_list = [url1, url2]
#     for ip in ip_list:
#         response = os.popen(f"ping {ip}").read()
#
#         if "Received = 4" in response:
#             bot.send_message(message.chat.id, f'URL网址{ip}可以正常访问哦~~')
#         else:
#             bot.send_message(message.chat.id, f'URL网址{ip}暂时不能正常访问哦~~')

@bot.message_handler(commands=['status'])
def send_status(message):
    hostname1 = "https://shogouki.youremby.gq:443"
    hostname2 = "http://aga01.youremby.gq:8096"

    response1 = os.system("ping -c 1 " + hostname1)

    if response1 == 0:
        bot.send_message(message.chat.id, 'CF源可以正常访问哦~')
    else:
        bot.send_message(message.chat.id, 'CF源不能正常访问哦~')

    response2 = os.system("ping -c 1 " + hostname2)

    if response2 == 0:
        bot.send_message(message.chat.id, 'AGA源可以正常访问哦~')
    else:
        bot.send_message(message.chat.id, 'AGA源不能正常访问哦~')


@bot.message_handler()
def echo(message):
    bot.reply_to(message, text='你好，我能帮你做些什么吗？如果忘记了指令，请输入 /help 获取帮助~')


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True, timeout=600)
    except Exception as e:
        logger.exception("__main__ Telegram Bot运行异常，抛出信息:{}".format(e))
