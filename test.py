# import requests
# from bs4 import BeautifulSoup
# import urllib.parse

# # import xlwt
# # import xlrd

# # 账号密码
# def login(username, password):
#     url = 'https://accounts.douban.com/j/mobile/login/basic'
#     header = {
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
#         'Referer': 'https://accounts.douban.com/passport/login_popup?login_source=anony',
#         'Origin': 'https://accounts.douban.com',
#         'content-Type': 'application/x-www-form-urlencoded',
#         'x-requested-with': 'XMLHttpRequest',
#         'accept': 'application/json',
#         'accept-encoding': 'gzip, deflate, br',
#         'accept-language': 'zh-CN,zh;q=0.9',
#         'connection': 'keep-alive'
#         , 'Host': 'accounts.douban.com'
#     }
#     # 登陆需要携带的参数
#     data = {
#         'ck' : '',
#         'name': '',
#         'password': '',
#         'remember': 'false',
#         'ticket': ''
#     }
#     data['name'] = username
#     data['password'] = password
#     data = urllib.parse.urlencode(data)
#     print(data)
#     req = requests.post(url, headers=header, data=data, verify=False)
#     print(req.status_code)
#     cookies = requests.utils.dict_from_cookiejar(req.cookies)
#     print(cookies)
#     return cookies

# def getcomment(cookies, mvid):  # 参数为登录成功的cookies(后台可通过cookies识别用户，电影的id)
#     start = 0
#     # w = xlwt.Workbook(encoding='ascii')  # #创建可写的workbook对象
#     # ws = w.add_sheet('sheet1')  # 创建工作表sheet
#     index = 1  # 表示行的意思，在xls文件中写入对应的行数
#     total_num = 0
#     while True:
#         # 模拟浏览器头发送请求
#         header = {
#             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
#         }
#         # try catch 尝试，一旦有错误说明执行完成，没错误继续进行
#         try:
#             # 拼凑url 每次star加20
#             url = 'https://movie.douban.com/subject/' + str(mvid) + '/comments?start=' + str(
#                 start) + '&limit=1000&sort=new_score&status=P&comments_only=1'
#             start += 1000
#             # 发送请求
#             req = requests.get(url, cookies=cookies, headers=header)
#             print(req.status_code)
#             # 返回的结果是个json字符串 通过req.json()方法获取数据
#             res = req.json()
#             res = res['html']  # 需要的数据在`html`键下
#             soup = BeautifulSoup(res, 'lxml')  # 把这个结构化html创建一个BeautifulSoup对象用来提取信息
#             node = soup.select('.comment-item')  # 每组class 均为comment-item  这样分成20条记录(每个url有20个评论)
#             total_num += len(node)
#             # for va in node:  # 遍历评论
#             #     name = va.a.get('title')  # 获取评论者名称
#             #     star = va.select_one('.comment-info').select('span')[1].get('class')[0][-2]  # 星数好评
#             #     votes = va.select_one('.votes').text  # 投票数
#             #     comment = va.select_one('.short').text  # 评论文本
#             #     print(name, star, votes, comment)
#             #     # ws.write(index, 0, index)  # 第index行，第0列写入 index
#             #     # ws.write(index, 1, name)  # 第index行，第1列写入 评论者
#             #     # ws.write(index, 2, star)  # 第index行，第2列写入 评星
#             #     # ws.write(index, 3, votes)  # 第index行，第3列写入 投票数
#             #     # ws.write(index, 4, comment)  # 第index行，第4列写入 评论内容
#             #     index += 1
#         except Exception as e:  # 有异常退出
#             # print(e)
#             print(total_num)
#             break
#     # w.save('test.xls')  # 保存为test.xls文件


# if __name__ == '__main__':
#     username = '13572850223'
#     password = 'wsw20160820'
#     cookies = login(username, password)
#     mvid = 30228394
#     getcomment(cookies, mvid)


import requests

# 用于维持登录会话，requests高级用法
s = requests.Session()

# 登录
def login():
    
    #url ='https://accounts.douban.com/passport/login'
    url = 'https://accounts.douban.com/j/mobile/login/basic'
    cookie = "ll=\"108297\"; bid=mcVUr-JBIFY; __utmz=30149280.1643333435.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; dbcl2=\"193230294:M8mu++tLH1c\"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.19323; __utmz=223695111.1643333532.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _vwo_uuid_v2=DCB697B237717F2DC8BB5FA744DD96152|c062805d57f63ef67005f10f40f744e1; __gads=ID=13881c648233d087-22c897932bcd0073:T=1643333543:RT=1643333543:S=ALNI_MaJrWsK8WNt8BF_vLLDNkOJn-8kAg; ck=LxbO; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1643350168%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_id.100001.4cf6=d54cd00a385602f9.1643333532.4.1643350168.1643341188.; _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=30149280.722495531.1643333435.1643340289.1643350170.4; __utmb=30149280.0.10.1643350170; __utmc=30149280; __utma=223695111.1313823080.1643333532.1643340289.1643350170.4; __utmb=223695111.0.10.1643350170; __utmc=223695111"


    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Referer': "http://www.google.com",
        'accept': "application/vnd.github.mercy-preview+json",
        'Cookie': cookie
    }
    
    data = {
        'ck': '',
        "name":'13572850223',
        "password":'wsw20160820',
        'remember': 'false',
        'ticket': ''
    }
    
    html = s.post(url,headers=headers)
    print(html.status_code)
    return s,html
  

# 获取个人信息
def get_user_data(s):
    url = 'https://music.douban.com/'
    html = s.get(url)
    print(html)
    return html

if __name__ == '__main__':
    s, html1 = login()
    html2 = get_user_data(s)