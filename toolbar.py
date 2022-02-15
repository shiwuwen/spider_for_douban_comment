# -*- encoding: utf-8 -*-

from operator import index
import xlwt
import os

def txt_to_xls(txt_name, xls_name):
    '''
    将 TXT 文件转换为 Excel文件
    '''
    try:
        f = open(txt_name, encoding = "UTF-8")
        xls = xlwt.Workbook()
        sheet = xls.add_sheet('sheet1', cell_overwrite_ok=True)
        x = 0
        while True:
            line = f.readline()
            if not line:
                break
            for i in range(len(line.split('$^&'))):
                item = line.split('$^&')[i]
                sheet.write(x, i, item)
            x += 1
            print("current line: ", x)
        f.close()
        xls.save(xls_name)
    except:
        raise

def extract_comment(txt_name, target_name):
    '''
    从 txt_name 中提取部分内容到 target_name 文件中
    '''
    if not os.path.exists(target_name):
        open(target_name, 'w').close()
    
    inputs = open(txt_name, 'r', encoding='utf-8')
    target = open(target_name, 'a', encoding='utf-8')

    index = 1
    while True:
        print('current line: ', index)
        line = inputs.readline()
        if not line:
            inputs.close()
            target.close()
            break
        split_line = line.split('$^&')
        target.write(split_line[-1])
        # target.write('\n')

        index += 1



if __name__ == "__main__" :
    txt_name = os.path.join(os.getcwd(), 'douban_comment.txt')
    xls_name  = os.path.join(os.getcwd(), 'douban_comment.xls')
    # txt_to_xls(txt_name, xls_name)

    target_name = os.path.join(os.getcwd(), 'comment_only.txt')
    extract_comment(txt_name, target_name)
