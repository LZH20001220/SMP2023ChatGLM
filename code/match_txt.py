import os
import json
import jieba
from fuzzywuzzy import fuzz

def create_filesdict(path, dict_fn) :
    filesdict = {'2019年':{}, '2020年':{}, '2021年':{}}
    f = open(dict_fn, 'w', encoding='utf8')
    f.write('股份有限公司 999 n\n')
    f.write('2019年 999 n\n')
    f.write('2020年 999 n\n')
    f.write('2021年 999 n\n')
    f.write('2019-2021年 999 n\n')
    f.write('2019至2021年 999 n\n')
    f.write('2019年至2021年 999 n\n')
    files = os.listdir(path)
    for fn in files :
        words = fn.split("__")
        f.write(words[1] + ' 99 n\n')
        f.write(words[3] + ' 999 n\n')
        filesdict[words[4]][words[3]] = {'filename':fn}
        filesdict[words[4]][words[1]] = {'filename':fn}
    f.close()
    return filesdict

def question_to_filename(question, filesdict) :
    fn1 = ""
    fn2 = ""
    fn3 = ""
    dict = []
    words = jieba.lcut(question)
    # print(words)
    year = 0
    for word in words :
        if '2019-2021' in word or '2019至2021' in word or '2019年至2021' in word:
            dict.append(filesdict['2019年'])
            dict.append(filesdict['2020年'])
            dict.append(filesdict['2021年'])
            break
        if len(word) != 5 :
            continue
        if '2019' in word :
            year = 2019
            dict.append(filesdict['2019年'])
        if '2020' in word :
            year = 2020
            dict.append(filesdict['2020年'])
        if '2021' in word :
            year = 2021
            dict.append(filesdict['2021年'])
    
    if "增长率" in words:
        if year != 0 and year != 2019:
            dict.append(filesdict[str((int)(year-1)) + '年'])
            
    # print(len(dict))
    company_name = ""
    if len(dict) > 0 :
        for word in words :
            if len(word) < 3 :
                continue
            if word in dict[0] :
                company_name = word
                fn1 = dict[0][word]['filename']
            if len(dict) >1:
                if word in dict[1] :
                    fn2 = dict[1][word]['filename']
            if len(dict) >2:
                if word in dict[2]:
                    fn3 = dict[2][word]['filename']
    return fn1, fn2, fn3, company_name

def files_dict():
    path = '../data/alltxt'
    dict_fn = '../dataset/custom_dict.txt'
    
    filesdict = create_filesdict(path, dict_fn)
    
    return dict_fn, filesdict

if __name__ == '__main__':
    
    dict_fn, filesdict = files_dict()
    jieba.load_userdict(dict_fn)
    f0 = open('../dataset/test_questions.jsonl', 'r', encoding='utf8')


    match_dict = []
    for line in f0 :
        row = json.loads(line)
        id = row['id']
        
        
        question = row['question']
        if '2019' not in question and '2020' not in question and '2021' not in question :
            continue
        
        question_str = question.replace('（', '').replace('）', '').replace('(', '').replace(')', '')
        
        prompt = question_str
        fn1, fn2, fn3, company_name = question_to_filename(prompt, filesdict)
            
        match_dict.append({"id":id,"question":question,"filename1":fn1, "filename2": fn2, "filename3": fn3, "company_name":company_name})

    with open('../dataset/match_test.json', 'w', encoding='utf-8', newline='') as fw:
        for i in match_dict:
            json.dump(i, fw, ensure_ascii=False, indent=None)
            print("", file=fw)

