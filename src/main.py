import os
import requests
import telebot
from configparser import ConfigParser

from telebot import types

import config
from random import choice
import string
import sqlite3

TOKEN = os.environ.get('TOKEN') or config.TGBOT_TOKEN
bot = telebot.TeleBot(TOKEN)
logger = config.setup_log()

conn = sqlite3.connect("D:/update/Odyssey_Bot.db")
print("Opened database successfully")


def GenPassword(length=8, chars=string.ascii_letters + string.digits):
    return ''.join([choice(chars) for i in range(length)])


def get_config():
    config = ConfigParser()
    config.read('config.ini')
    config_vars = dict()
    config_vars['SERVER'] = config['EMBY']['SERVER']
    config_vars['EMBY_API'] = config['EMBY']['API_KEY']
    config_vars['EMBY_REGISTER'] = config['EMBY']['REGISTER']
    return config_vars


def get_endpoint(param):
    config = get_config()
    endpoint = config['SERVER'] + param + "?api_key=" + config['EMBY_API']
    return endpoint


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


# 未完成
@bot.message_handler(commands=['status'])
def check_server(url, message):
    url = get_endpoint("System/Ping")
    try:
        response = requests.post(url)
        data = response.text
        if data == "Emby Server":
            bot.send_message(message.chat.id, 'Odyssey-Emby服务可以正常访问哦~')
            bot.send_message(message.chat.id, 'Odyssey-Emby服务器状态：\n'
                             # '在线人数：\n'
                             # '播放人数：\n'
                             # '开机时间：\n'
                             # '实时下载：\n'
                             # '实时上传：\n'
                             # '累计下载：\n'
                             # '累计上传：\n'
                             # '负载：'
                             )

    except:
        bot.send_message(message.chat.id, 'Odyssey-Emby服务暂时不可以访问~')


@bot.message_handler(commands=['register'])
def register_user(message):
    global response1, embyId, embyName

    string1 = "Users"
    url = get_endpoint(string1)
    response = requests.get(url)
    data = response.json()

    cursor = conn.execute("SELECT id,telegramID,telegramUID,password from t_telegrameUser")

    string2 = "Users/New"
    new = get_endpoint(string2)

    config1 = get_config()

    yourUserName = str(message.from_user.username)
    yourUserUID = str(message.from_user.id)
    yourPasswd = GenPassword(8)

    if config1['EMBY_REGISTER'] == 'TRUE':

        # print("ID = ", row[0])
        # print("telegramID = ", row[1])
        # print("telegramUID = ", row[2])
        # print("password = ", row[3], "\n")

        # 先查emby的user表是否有yourusername，如果查到了，再查本地数据库，因为emby数据库无法查密码，很神秘，所以查本地数据库保存的密码
        for user in data:
            for row in cursor:
                if user["Name"] == yourUserName:
                    if yourUserName == row[1] and yourUserUID == row[2]:
                        bot.send_message(message.chat.id, '你好，你的telegram已经注册了Odyssey公益服务器啦~快点登录吧~ \n')
                        bot.send_message(message.chat.id, '你的账号是：' + row[1] + '\n'
                                                                              '你的密码是：' + row[3])
                    else:
                        bot.send_message(message.chat.id, '您已注册，但是本机器人本地数据库无法查询到您的账号密码，请尝试重置密码~')
                        break
                else:
                    try:
                        response1 = requests.post(new, {'Name': yourUserName})
                        print('Odyssey远程数据库已创建用户')
                    except:
                        bot.send_message(message.chat.id, '创建账号失败，请联系管理员~')
                        break

                    data1 = response1.json()
                    for user1 in data1:
                        embyName = user1["Name"]
                        embyId = user1["Id"]

                    try:
                        # 更新emby密码
                        string3 = "Users/{" + embyId + "}/Password"
                        requests.post(string3, {'Id': embyId, 'NewPw': yourPasswd})

                        bot.send_message(message.chat.id, '您的账号创建成功！\n')
                        print('Odyssey远程数据库已更新' + embyName + '初始密码')
                        bot.send_message(message.chat.id, '账号：' + embyName + '\n'
                                                                             '密码：' + yourPasswd)

                    except:
                        bot.send_message(message.chat.id, '账号生成初始密码失败，请联系管理员~')
                        break

                    try:
                        conn.execute(
                            "INSERT INTO t_telegrameUser ( telegramID, telegramUID, password ) VALUES ( '" + yourUserName + "', '" + yourUserUID + "', '" + yourPasswd + "' )")
                        conn.execute(
                            "INSERT INTO t_embyUser ( embyID, password ) VALUES('" + embyName + "','" + yourPasswd + "')")
                        conn.execute(
                            "INSERT INTO t_sayHello ( telegramID, embyID ) VALUES('" + yourUserName + "','" + embyName + "')")
                        conn.commit()
                        bot.send_message(message.chat.id, '新用户' + embyName + '本地数据库已写入成功')
                        print('新用户' + embyName + '本地数据库已写入成功')
                        break

                    except:
                        bot.send_message(message.chat.id, '本地机器人数据库写入失败，可能会导致无法查询用户账号密码，请联系管理员！')
                        print('本地机器人数据库写入失败，可能会导致无法查询用户账号密码，请联系管理员！')
                        break

    elif config1['EMBY_REGISTER'] == 'FALSE':
        bot.send_message(message.chat.id, 'Odyssey已关闭注册！')

    else:
        bot.send_message(message.chat.id, 'config配置register参数错误，请联系管理员解决！')
        print('config配置register参数错误，请联系管理员解决！')


@bot.message_handler(commands=['delete'])
def delete_user(message):
    global user1
    string1 = "Users"
    url = get_endpoint(string1)
    response = requests.get(url)
    data = response.json()

    cursor = conn.execute("SELECT id,telegramID,telegramUID,password from t_telegrameUser")

    yourUserName = str(message.from_user.username)
    yourUserUID = str(message.from_user.id)

    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('我确定我要删除我的账号')
    itembtn2 = types.KeyboardButton('我按错了，我不想删除我的账号')
    markup.add(itembtn1, itembtn2)
    rell = bot.send_message(message.chat.id, '请问你一定要删除账号吗？\n'
                                             '如果需要删除账号，请选择：', reply_markup=markup)
    if str(rell) == '我按错了，我不想删除我的账号':
        bot.send_message(message.chat.id, '你好，我能帮你做些什么吗？如果忘记了指令，请输入 /help 获取帮助~')

    elif str(rell) == '我确定我要删除我的账号':
        bot.send_message(message.chat.id, '正在执行账号删除工作~')
        for user in data:
            for row in cursor:
                if user["Name"] == yourUserName:

                    embyName = user["Name"]
                    embyId = user["Id"]

                    if yourUserName == row[1] and yourUserUID == row[2]:

                        try:
                            conn.execute("DELETE from t_telegrameUser where telegramID=" + yourUserName + ";")
                            conn.execute("DELETE from t_embyUser where embyID=" + yourUserName + ";")
                            conn.execute("DELETE from t_sayHello where telegramID=" + yourUserName + ";")
                            conn.commit()

                            bot.send_message(message.chat.id, "本地数据库删除" + yourUserName + "成功！")
                            print("本地数据库删除" + yourUserName + "成功！")

                        except:
                            bot.send_message(message.chat.id, "本地数据库删除" + yourUserName + "失败！请联系管理员手动删除！")
                            print("本地数据库删除" + yourUserName + "失败！请联系管理员手动删除！")

                        try:
                            string2 = "/Users/{" + embyId + "}"
                            dele = get_endpoint(string2)
                            requests.delete(dele)
                            bot.send_message(message.chat.id, "emby远程数据库删除" + embyName + "成功！")
                            print("emby远程数据库删除" + embyName + "成功！")
                            break

                        except:
                            bot.send_message(message.chat.id, "emby远程数据库删除" + embyName + "失败！请联系管理员手动删除！")
                            print("emby远程数据库删除" + embyName + "失败！请联系管理员手动删除！")
                            break

                    else:
                        bot.send_message(message.chat.id, '本地数据库未查找到您的注册记录，开始删除emby远程数据库里的账号~')
                        try:
                            string2 = "/Users/{" + embyId + "}"
                            dele = get_endpoint(string2)
                            requests.delete(dele, {'id': embyId})
                            bot.send_message(message.chat.id, "emby远程数据库删除" + embyName + "成功！")
                            print("emby远程数据库删除" + embyName + "成功！")
                            break

                        except:
                            bot.send_message(message.chat.id, "emby远程数据库删除" + embyName + "失败！请联系管理员手动删除！")
                            print("emby远程数据库删除" + embyName + "失败！请联系管理员手动删除！")
                            break

    else:
        bot.send_message(message.chat.id, 'bot遇到错误，请联系管理员！')
        print('bot遇到错误，请联系管理员！')


@bot.message_handler(commands=['reset'])
def reset_user(message):
    yourUserName = str(message.from_user.username)
    yourUserUID = str(message.from_user.id)
    yourPasswd = GenPassword(8)

    string1 = "Users"
    url = get_endpoint(string1)
    response = requests.get(url)
    data = response.json()

    cursor = conn.execute("SELECT id,telegramID,telegramUID,password from t_telegrameUser")

    for user in data:
        for row in cursor:
            if user["Name"] == yourUserName:

                embyName = user["Name"]
                embyId = user["Id"]

                if yourUserName == row[1] and yourUserUID == row[2]:
                    try:
                        conn.execute(
                            "UPDATE t_telegrameUser set password = " + yourPasswd + " where telegramID=" + yourUserName)
                        conn.execute("UPDATE t_embyUser set password = " + yourPasswd + " where embyID=" + embyName)
                        conn.commit()
                        bot.send_message(message.chat.id, "机器人重置本地数据库密码成功")
                    except:
                        bot.send_message(message.chat.id, "机器人重置本地数据库密码失败，请联系管理员！")
                        break

                    string2 = "Users/{" + embyId + "}/Password"
                    res = get_endpoint(string2)
                    try:
                        requests.post(res, {'Id': embyId, 'NewPw': yourPasswd, 'ResetPassword': True})
                        bot.send_message(message.chat.id, "机器人重置emby远程数据库密码成功\n"
                                                          "你的账号是：" + embyName + "\n"
                                                                                "你的密码是:" + yourPasswd)
                    except:
                        bot.send_message(message.chat.id, "机器人重置emby远程数据库密码失败，请联系管理员！")
                        break

                else:
                    bot.send_message(message.chat.id, "机器人没有在本地数据库找到你的账号，将重置emby数据库密码并更新到本地数据库~")
                    string2 = "Users/{" + embyId + "}/Password"
                    res = get_endpoint(string2)
                    try:
                        requests.post(res, {'Id': embyId, 'NewPw': yourPasswd, 'ResetPassword': True})
                        bot.send_message(message.chat.id, "机器人重置emby远程数据库密码成功\n"
                                                          "你的账号是：" + embyName + "\n"
                                                                                "你的密码是:" + yourPasswd)
                    except:
                        bot.send_message(message.chat.id, "机器人重置emby远程数据库密码失败，请联系管理员！")
                        break

                    try:
                        conn.execute(
                            "INSERT INTO t_telegrameUser ( telegramID, telegramUID, password ) VALUES ( '" + yourUserName + "', '" + yourUserUID + "', '" + yourPasswd + "' )")
                        conn.execute(
                            "INSERT INTO t_embyUser ( embyID, password ) VALUES('" + embyName + "','" + yourPasswd + "')")
                        conn.execute(
                            "INSERT INTO t_sayHello ( telegramID, embyID ) VALUES('" + yourUserName + "','" + embyName + "')")
                        conn.commit()
                        bot.send_message(message.chat.id, '新用户' + embyName + '本地数据库已写入成功')
                        print('新用户' + embyName + '本地数据库已写入成功')
                        break

                    except:
                        bot.send_message(message.chat.id, '本地机器人数据库写入失败，可能会导致无法查询用户账号密码，请联系管理员！')
                        print('本地机器人数据库写入失败，可能会导致无法查询用户账号密码，请联系管理员！')
                        break


@bot.message_handler()
def echo(message):
    bot.reply_to(message, text='你好，我能帮你做些什么吗？如果忘记了指令，请输入 /help 获取帮助~')


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True, timeout=600)
    except Exception as e:
        logger.exception("__main__ Telegram Bot运行异常，抛出信息:{}".format(e))

conn.close()
