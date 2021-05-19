import os
import telebot
import emoji
import config
import requests
from lxml import etree
import tt_USA
import tt_China

odyssey_id = 'YOUR CHAT_ID'

film_list = tt_USA.get_file_top_ten()
film_list_China = tt_China.get_file_top_ten()


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/87.0.4280.88 Safari/537.36'}
movieurl = "https://ent.sina.com.cn/movie/top10bang/"

res = requests.get(url=movieurl, headers=headers).content
selector = etree.HTML(res)

TOKEN = os.environ.get('TOKEN') or config.TGBOT_TOKEN
bot = telebot.TeleBot(TOKEN)
logger = config.setup_log()

photo_china = open("Mainland.jpg", "rb")
photo_usa = open("NorthAmerica.jpg", "rb")


baomihua = emoji.emojize(':popcorn:')
one = "1️⃣"
two = '2️⃣'
thr = '3️⃣'
four = '4️⃣'
five = '5️⃣'
six = '6️⃣'
seven = '7️⃣'
eight = '8️⃣'
nine = '9️⃣'
ten = '🔟'

date_USA = selector.xpath('//*[@id="__liveLayoutContainer"]/div/div/div/div/div[1]/div/div[1]/div[2]/span/text()')
date_USA = date_USA[0]
date_USA = date_USA[-10:]

date_China = selector.xpath('//*[@id="__liveLayoutContainer"]/div/div/div/div/div[2]/div/div[1]/div[2]/span/text()')
date_China = date_China[0]
date_China = date_China[-10:]

name_USA = []
wk_money_USA = []
all_money_USA = []
for film in film_list:
    name_USA.append(film.name)
    wk_money_USA.append(film.wk_money)
    all_money_USA.append(film.all_money)

name_China = []
wk_money_China = []
all_money_China = []
for film in film_list_China:
    name_China.append(film.name)
    wk_money_China.append(film.wk_money)
    all_money_China.append(film.all_money)

wk_money_USA1 = []
all_money_USA1 = []
for i in wk_money_USA:
    i = i[:-4]
    wk_money_USA1.append(i)

for i in all_money_USA:
    i = i[:-4]
    all_money_USA1.append(i)

for index in range(len(name_USA)):
    name_USA[index] = " " + name_USA[index]

for index in range(len(name_China)):
    name_China[index] = " " + name_China[index]


@bot.message_handler(commands=['list_China'])
def send_photo1(message):
    msg = bot.send_photo(chat_id=odyssey_id, photo=photo_china, caption=[baomihua + "#TopBoxOffice #Mainland #票房\n"
                                                                                    "\n"
                                                                                    "中国票房周榜（" + date_China + " 日 ，数据为该周末票房 / 电影总票房 结算货币：人民币）\n"
                                                                                                             "\n"
                                                                         + one + name_China[0] + "\n"
                                                                                                 "       " +
                                                                         wk_money_China[0][
                                                                             0] + "万 / " + all_money_China[0] + "万\n "
                                                                                                                "\n"
                                                                         + two + name_China[1] + "\n"
                                                                                                 "       " +
                                                                         wk_money_China[
                                                                             1] + "万 / " + all_money_China[1] + "万\n "
                                                                                                                "\n"
                                                                         + thr + name_China[2] + "\n "
                                                                                                 "       " +
                                                                         wk_money_China[
                                                                             2] + "万 / " + all_money_China[2] + "万\n "
                                                                                                                "\n"
                                                                         + four + name_China[3] + "\n"
                                                                                                  "       " +
                                                                         wk_money_China[
                                                                             3] + "万 / " + all_money_China[3] + "万\n "
                                                                                                                "\n"
                                                                         + five + name_China[4] + "\n"
                                                                                                  "       " +
                                                                         wk_money_China[
                                                                             4] + "万 / " + all_money_China[4] + "万\n "
                                                                                                                "\n"
                                                                         + six + name_China[5] + "\n"
                                                                                                 "       " +
                                                                         wk_money_China[
                                                                             5] + "万 / " + all_money_China[5] + "万\n "
                                                                                                                "\n"
                                                                         + seven + name_China[6] + "\n"
                                                                                                   "       " +
                                                                         wk_money_China[6] + "万 / " + all_money_China[
                                                                             6] + "万\n "
                                                                                  "\n"
                                                                         + eight + name_China[7] + "\n"
                                                                                                   "       " +
                                                                         wk_money_China[7] + "万 / " + all_money_China[
                                                                             7] + "万\n "
                                                                                  "\n"
                                                                         + nine + name_China[8] + "\n"
                                                                                                  "       " +
                                                                         wk_money_China[
                                                                             8] + "万 / " + all_money_China[8] + "万\n "
                                                                                                                "\n"
                                                                         + ten + name_China[9] + "\n"
                                                                                                 "       " +
                                                                         wk_money_China[
                                                                             9] + "万 / " + all_money_China[9] + "万\n "
                                                                                                                "\n"
                                                                                                                "Channel: https://t.me/odysseyplus"])
    bot.send_message(message.chat.id, "中国电影票房榜单已推送到Odyssey频道")
    bot.delete_message(odyssey_id, msg.message_id + 1)


@bot.message_handler(commands=['list_USA'])
def send_photo1(message):
    msg = bot.send_photo(chat_id=odyssey_id, photo=photo_usa, caption=[baomihua + "#TopBoxOffice #NorthAmerica #票房\n"
                                                                                  "\n"
                                                                                  "北美票房周榜（" + date_USA + " 日 ，数据为该周末票房 / 电影总票房 结算货币：美元）\n"
                                                                                                         "\n"
                                                                       + one + name_USA[0] + "\n"
                                                                                             "       " + wk_money_USA1[
                                                                           0] + "万 / " + all_money_USA1[0] + "万\n "
                                                                                                             "\n"
                                                                       + two + name_USA[1] + "\n"
                                                                                             "       " + wk_money_USA1[
                                                                           1] + "万 / " + all_money_USA1[1] + "万\n "
                                                                                                             "\n"
                                                                       + thr + name_USA[2] + "\n "
                                                                                             "       " + wk_money_USA1[
                                                                           2] + "万 / " + all_money_USA1[2] + "万\n "
                                                                                                             "\n"
                                                                       + four + name_USA[3] + "\n"
                                                                                              "       " + wk_money_USA1[
                                                                           3] + "万 / " + all_money_USA1[3] + "万\n "
                                                                                                             "\n"
                                                                       + five + name_USA[4] + "\n"
                                                                                              "       " + wk_money_USA1[
                                                                           4] + "万 / " + all_money_USA1[4] + "万\n "
                                                                                                             "\n"
                                                                       + six + name_USA[5] + "\n"
                                                                                             "       " + wk_money_USA1[
                                                                           5] + "万 / " + all_money_USA1[5] + "万\n "
                                                                                                             "\n"
                                                                       + seven + name_USA[6] + "\n"
                                                                                               "       " +
                                                                       wk_money_USA1[6] + "万 / " + all_money_USA1[
                                                                           6] + "万\n "
                                                                                "\n"
                                                                       + eight + name_USA[7] + "\n"
                                                                                               "       " +
                                                                       wk_money_USA1[7] + "万 / " + all_money_USA1[
                                                                           7] + "万\n "
                                                                                "\n"
                                                                       + nine + name_USA[8] + "\n"
                                                                                              "       " + wk_money_USA1[
                                                                           8] + "万 / " + all_money_USA1[8] + "万\n "
                                                                                                             "\n"
                                                                       + ten + name_USA[9] + "\n"
                                                                                             "       " + wk_money_USA1[
                                                                           9] + "万 / " + all_money_USA1[9] + "万\n "
                                                                                                             "\n"
                                                                                                             "Channel: https://t.me/odysseyplus"])
    bot.send_message(message.chat.id, "美国电影票房榜单已推送到Odyssey频道")
    bot.delete_message(odyssey_id, msg.message_id + 1)


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True, timeout=600)
    except Exception as e:
        logger.exception("__main__ Telegram Bot运行异常，抛出信息:{}".format(e))
