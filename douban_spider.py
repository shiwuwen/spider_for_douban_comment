from fileinput import filename
import requests
import json
from bs4 import BeautifulSoup
import random
import os
import time

# 生成不同的 user_agent 信息，预防反爬虫程序
user_agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
    'Opera/8.0 (Windows NT 5.1; U; en)',
    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 ',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
]

# 登录信息，使用cookie登录才能爬取全部内容
cookie = "ll=\"108297\"; bid=mcVUr-JBIFY; __utmz=30149280.1643333435.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; dbcl2=\"193230294:M8mu++tLH1c\"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.19323; __utmz=223695111.1643333532.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _vwo_uuid_v2=DCB697B237717F2DC8BB5FA744DD96152|c062805d57f63ef67005f10f40f744e1; __gads=ID=13881c648233d087-22c897932bcd0073:T=1643333543:RT=1643333543:S=ALNI_MaJrWsK8WNt8BF_vLLDNkOJn-8kAg; ck=LxbO; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1643350168%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_id.100001.4cf6=d54cd00a385602f9.1643333532.4.1643350168.1643341188.; _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=30149280.722495531.1643333435.1643340289.1643350170.4; __utmb=30149280.0.10.1643350170; __utmc=30149280; __utma=223695111.1313823080.1643333532.1643340289.1643350170.4; __utmb=223695111.0.10.1643350170; __utmc=223695111"

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

def pause_comment(comment_html):
    '''
    对网页内容进行解析
    返回 用户名、推荐指数、评论时间、评论内容
    '''
    # id = comment_html['data-cid']
    # name = comment_html.div.a['title']
    comment_info = comment_html.find_all('span', attrs={"class":"comment-info"})[0]
    # print(comment_info)
    user_name = comment_info.a.text
    # print(user_name)
    comment_span = comment_info.find_all('span') #[-1]['title']
    rating_star = comment_span[1]['title']
    comment_time = comment_span[-1]['title']
    comment_span_short = comment_html.find_all('span', attrs={"class":"short"})[0]
    comment_text = comment_span_short.text
    # print(text)
    return user_name, rating_star, comment_time, comment_text

def write_to_txt(input_list, file_name):
    '''
    将 input_list 中内容写入 file_name 中
    '''
    with open(file_name, "a", encoding="utf-8") as f:
        for context in input_list:
            f.write(context)
            f.write('\n')

def read_from_txt(file_name):
    '''
    从 file_name 中读取内容
    '''
    comment = []
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            comment.append(line)
    
    return comment

def read_from_network():
    '''
    通过 URL 获取网页内容并分析
    '''
    # 觉醒年代ID：30228394
    movie_id = 30228394
    total_comment_num = 145683
    comment_num_for_one_epoch = 100
    total_epoch = total_comment_num // comment_num_for_one_epoch
    current_start = 0

    # print("hello")

    for epoch in range(total_epoch):
        print("epoch start: ", epoch)
        # current_start = epoch * comment_num_for_one_epoch
        basic_url = "https://movie.douban.com/subject/" + str(movie_id) + "/comments?start=" + str(current_start) + "&limit=" + str(comment_num_for_one_epoch) +"&status=P&sort=new_score"
        
        # print(basic_url)

        response2 = requests.get(basic_url, headers=get_random_headers())
        print("response code: ", response2.status_code)

        html = BeautifulSoup(response2.text, 'xml')
        comments = html.find_all("div", attrs={"class": "comment-item "})
        print("comment nums: ", len(comments))

        context_list = []
        for comment in comments:
            # print("________________")
            user_name, rating_star, comment_time, comment_text = pause_comment(comment)
            # print(user_name, rating_star, comment_time, comment_text)
            # print("________________")

            current_context = '$^&'.join([user_name, rating_star, comment_time, comment_text])
            context_list.append(current_context.replace("\n", " ").replace("\r", " "))
        
        # print(context_list)

        write_to_txt(context_list, file_name)
        # time.sleep(0.1)
        # if len(comments) <= 0:
        #     break
        current_start += len(comments)
        print("next start num: ", current_start)
        print("epoch end: ", epoch)

def read_from_local_html(html_name):
    '''
    读取本地 HTML 文件
    '''
    html_path = os.path.join(os.getcwd(), html_name)
    html_file = open(html_path, 'r', encoding='utf-8')
    html = BeautifulSoup(html_file.read(), 'lxml')
    print(html)

    comments = html.find_all("div", attrs={"class": "comment-item "})
    print(len(comments))

    context_list = []
    for comment in comments:
        print("________________")
        print(comment)
        user_name, rating_star, comment_time, comment_text = pause_comment(comment)
        print(user_name, rating_star, comment_time, comment_text)
        print("________________")

        current_context = '$^&'.join([user_name, rating_star, comment_time, comment_text])
        context_list.append(current_context.strip('\n'))
        
    # print(context_list)

    write_to_txt(context_list, file_name)



if __name__ == '__main__':
    
    file_name = os.path.join(os.getcwd(), 'douban_comment.txt')
    # html_path = os.path.join(os.getcwd(), 'juexingniandai_html_1.html')
    if not os.path.exists(file_name):
        open(file_name, 'w').close()
    
    read_from_network()

    # html_name = 'data_1.html'
    # read_from_local_html(html_name)
    
    

    # comments = read_from_txt(file_name)
    # for index in range(len(comments)):
    #     print(comments[index])
    #     print("              ")
