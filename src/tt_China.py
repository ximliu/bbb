import requests
from lxml import etree
from film import film

def get_file_top_ten():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.88 Safari/537.36'}
    movieurl = "https://ent.sina.com.cn/movie/top10bang/"

    res = requests.get(url=movieurl, headers=headers).content
    selector = etree.HTML(res)
    file_list = []
    for j in range(2, 12):
        file_temp = film()
        title_name = \
            selector.xpath('//*[@id="__liveLayoutContainer"]/div/div/div/div/div[2]/div/div[2]/div[2]/ul[' + str(
                j) + ']/li[3]/a/@title')[0]
        wk_money_temp = selector.xpath('//*[@id="__liveLayoutContainer"]/div/div/div/div/div[2]/div/div[2]/div[2]/ul['+str(j) +']/li[6]/text()')[0]
        all_money_temp = selector.xpath(
            '//*[@id="__liveLayoutContainer"]/div/div/div/div/div[2]/div/div[2]/div[2]/ul['+str(j)+']/li[7]/text()')[0]

        wk_money_temp = float(wk_money_temp)
        wk_money_temp = int(wk_money_temp)
        wk_money_temp = str(wk_money_temp)

        all_money_temp = float(all_money_temp)
        all_money_temp = int(all_money_temp)
        all_money_temp = str(all_money_temp)

        file_temp.name = title_name
        file_temp.wk_money = wk_money_temp
        file_temp.all_money = all_money_temp

        file_list.append(file_temp)
    return file_list