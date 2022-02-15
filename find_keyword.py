import jieba
import os

from matplotlib.pyplot import get

def read_keywords_from_txt(file_name):
    '''
    从 file_name 中提取关键字并生成字典
    '''
    keywords_dict = {}
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            first_split = line.strip().split('：')
            second_split = first_split[-1].split('、')
            keywords_dict[first_split[0]] = second_split
    
    return keywords_dict


def count_word_numbers(keywords_dict, comment_filename):
    '''
    统计 comment_filename 中评论的关键字出现次数
    其中 count_numbers_dict 为主关键字频次
         count_every_word 为次关键字频次
    '''
    f = open(comment_filename, 'r', encoding='utf-8')
    count_numbers_dict = {}
    count_every_word = {}

    index = 0
    while True:
        curr_line = f.readline()
        # print("curr line: ", index)
        if not curr_line:
            break
        words = jieba.lcut(curr_line)

        for word in words:
            # print(word)
            for keyword in keywords_dict.keys():
                if word in keywords_dict[keyword]:
                    count_numbers_dict[keyword] = count_numbers_dict.get(keyword, 0) + 1
                    count_every_word[word] = count_every_word.get(word, 0) + 1
                    break
        index += 1
    f.close()
    return count_numbers_dict, count_every_word

def get_detailed_keywords_nums(count_every_word, keywords_dict):
    '''
    统计每个主关键字下的次关键字的频次
    '''
    detailed_keywords_nums = {}

    for keyword in keywords_dict.keys():
        detailed_keywords_nums[keyword] = []
        for word in count_every_word.keys():
            if word in keywords_dict[keyword]:
                string = word + ':' + str(count_every_word[word])
                detailed_keywords_nums[keyword].append(string)
    
    return detailed_keywords_nums


if __name__ == '__main__':
    keywords_filename = os.path.join(os.getcwd(), 'keyword.txt')
    keywords_dict = read_keywords_from_txt(keywords_filename)
    # print(keywords_dict)

    comment_filename = os.path.join(os.getcwd(), 'comment_only.txt')
    count_numbers_dict, count_every_word = count_word_numbers(keywords_dict, comment_filename)
    print(count_numbers_dict)
    # print(count_every_word)
    print()
    print()
    print()
    print()

    detailed_keywords_nums = get_detailed_keywords_nums(count_every_word, keywords_dict)
    print(detailed_keywords_nums)


