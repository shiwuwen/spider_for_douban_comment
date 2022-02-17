from attr import attr
import requests
from bs4 import BeautifulSoup
import os
import time

# 登录微博的 cookies
# cookie = 'SINAGLOBAL=227520802342.12714.1593160007291; UOR=,,cn.bing.com; ariaDefaultTheme=default; ariaFixed=true; ariaReadtype=1; ariaMouseten=null; ariaStatus=false; login_sid_t=20f5c32786a79669f59c7afa1a44012b; cross_origin_proto=SSL; _s_tentry=cn.bing.com; Apache=5246036563695.347.1645065980695; ULV=1645065980702:9:3:3:5246036563695.347.1645065980695:1644994292329; XSRF-TOKEN=CtfPvYapVQxU7A6DsstqxrQf; WBtopGlobal_register_version=2022021711; wb_view_log=1536*8641.25&1536*8641; SUB=_2A25PCcy1DeRhGeBL61UR9yjLyzmIHXVsfrl9rDV8PUNbmtANLVb3kW9NR0MY4CAmarLIovmS6uID7Ri7LftJM3eL; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5jfFeO_fBcQn8jiQQrMKiS5JpX5KzhUgL.FoqfehM7S0qNeh-2dJLoI7U3IPH.Igyf; ALF=1676603493; SSOLoginState=1645067493; wb_view_log_6507076705=1536*8641; WBPSESS=Dt2hbAUaXfkVprjyrAZT_Mxq7f7FpHpzm39UKapoweBW2KILcihQOW7krRfFaoHLrXpIh3gMds4Xy4WVWywU2LXw05lP_NAxQEodZjEmhAa1ebtQEgvHIXByuvYYv0h954CJOHIinUt4vLplLNaOZsqqqwnSvnJVm-NQskKcW1g0eLWK1fu7Ti2ISio0Ku5xvTO9FZ8brnsbh5hdQd8E3A==; webim_unReadCount={"time":1645068029892,"dm_pub_total":0,"chat_group_client":0,"chat_group_notice":0,"allcountNum":84,"msgbox":0}; TC-V-WEIBO-G0=b09171a17b2b5a470c42e2f713edace0'

cookie = "SUB=_2A25PCZJfDeRhGeBL61UR9yjLyzmIHXVs9T4XrDV6PUJbktCOLRHGkW1NR0MY4IzntiLY7I5ZYPadPYUXSrdL6A1p; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5jfFeO_fBcQn8jiQQrMKiS5NHD95QcSK5NehMcS05fWs4DqcjGIJLf9sLQUBtt; SSOLoginState=1645077007; _T_WM=85869034439; XSRF-TOKEN=942c4c; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D20000174%26uicode%3D20000174"

def get_random_headers():
    '''
    返回headers
    '''
    # index = random.randint(0, 10)
    # user_agent = user_agents[index]
    # random_headers = {
    #     'User-Agent': user_agent
    # }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Referer': "http://www.google.com",
        'accept': "application/vnd.github.mercy-preview+json",
        'Cookie': cookie
    }
    return headers

def get_user_info_url(file_name):

    for page_index in range(50):
        # 用于保存用户信息
        user_info_list = []

        # 觉醒年代URL
        basic_url = "https://s.weibo.com/realtime?q=%E8%A7%89%E9%86%92%E5%B9%B4%E4%BB%A3&rd=realtime&tw=realtime&Refer=user_realtime&page=" + str(page_index)
        # 获取URL信息
        response2 = requests.get(basic_url, headers=get_random_headers())
        print("response code: ", response2)
        # 解析获取的网页
        html = BeautifulSoup(response2.text, 'lxml')
        # print(html)
        # 提取用户评论所在的 div
        comments = html.find_all("div", attrs={"class": "card-feed"})
        print(len(comments))
        # 分析每一个用户评论
        for comment in comments:
            # 获取用户个人页超链接
            user_url_temp = comment.find_all("div", attrs={"class": "avator"})[0].find_all("a")[0].get('href')
            # 提取 userID
            user_id = user_url_temp.split('/')[-1].split('?')[0]
            # print(user_id)
            # 生成用户个人页URL
            user_url = "https://weibo.cn/" + str(user_id) + "/info"
            # 从个人也提取用户名和生日
            name, birthday = get_user_info(user_url)

            print(name + " : " + birthday)
            # 添加用户信息
            user_info_list.append(name + " " + birthday)
        # 保存用户信息
        write_to_txt(user_info_list, file_name)
        # 睡眠3秒，防止被禁
        time.sleep(3)


def get_user_info(user_url):
    # 获取URL内容
    response2 = requests.get(user_url, headers=get_random_headers())
    # 提取网页信息
    html = BeautifulSoup(response2.text, 'lxml')
    # 提取用户信息
    user_info = html.find_all("div", attrs={"class": "c"})
    user_info = str(user_info[3]).split('<br/>')
    # 获取用户名
    user_name = user_info[0].split(':')[-1]
    # 获取生日
    user_birthday = user_info[3].split(':')[-1]
    return user_name, user_birthday

def write_to_txt(info_list, file_name):
    # 保存到TXT文件
    with open(file_name, 'a+', encoding='utf-8') as f:
        for info in info_list:
            f.write(info)
            f.write('\n')
    
if __name__ == '__main__':
    txt_name = os.path.join(os.getcwd(), 'weibo_userinfo.txt')
    get_user_info_url(txt_name)