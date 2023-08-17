import json
import re
import pandas as pd


#从JSON文件中读取问题数据
def chinese_num(value):
    NUM = [ '(一)', '(二)', '(三)', '(四)', '(五)', '(六)', '(七)', '(八)', '(九)', '(十)',
           '（一）', '（二）', '（三）', '（四）', '（五）', '（六）', '（七）', '（八）', '（九）', '（十）']
    for i in NUM:
        if i in value:
            return True
    return False

def check_seven(value):
    ss = ['七．', '七.', '七-', '七·', '七/', '七：', '七之', '七（', '七(', '七 (', '六.', '六/', '六．', '五.', '四(']
    for i in ss:
        if i in value:
            return True
    return False

def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    
def convert_to_numeric(value):
    try:
        numeric_value = float(value)
        return numeric_value
    except ValueError:
        return 0 

def replace_num_str(value):
    if type(value) == str:
        value = value.replace(',', '').replace('\n','').replace('\r','')
    return value

def replace_return_str(value):
    if type(value) == str:
        value = value.replace('\n','').replace('\r','')
    return value

def read_questions_from_json(json_file_path):
    questions = []
    with open(json_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            question = json.loads(line)
            questions.append(question)
    return questions

def checkflag(item_value):
    flag = False
    if item_value != None and item_value != '' and type(item_value) != float:
        if item_value == "" or item_value == "-" or item_value == "--" or item_value == "）" or item_value == "/":
            flag = True
        if '。' in item_value or '，' in item_value:
            flag = True
        if '变化' in item_value or "适用" in item_value or "主要" in item_value or "报告" in item_value or item_value=="无":
            flag = True
        if ('、' in item_value):
            flag = True
        if ('附注' in item_value) or ('注释' in item_value):
            flag = True
        if ('，' in item_value):
            flag = True
        if chinese_num(item_value):
            flag = True
        if '(' in item_value and '十' in item_value:
            flag = True
        if '（' in item_value and '十' in item_value:
            flag = True 
        if item_value == "七":
            flag = True
        if check_seven(item_value):
            flag = True
        if re.match(r'[0-9]-', item_value):
            flag = True
        if re.match(r'七[\s]*[0-9]+', item_value):
            flag = True
    return flag

def extract_table_data(file_name, table_header):
    allname = file_name.split('/')[-1]
    company_name = allname.split('__')[1]
    company_short_name = allname.split('__')[3]
    company_code = allname.split('__')[2]
    year = allname.split('__')[4]
    
    table_data = {}
    
    for col_name in table_header:
        with open(file_name, 'r', encoding='utf-8') as file:
            
            for line in file:
                if col_name in table_data.keys():
                    break
                
                match = re.search(r'\[(.*?)\]', line)  # 在每一行中查找以[]包裹的内容
                
                if match:
                    
                    result_list = match.group(1).split('\', ')  # 分割匹配项成元素
                    
                    for i in range(min(len(result_list), 2)):
                        result_list[i] = result_list[i].replace("'", "").replace(",", "").split('.')[-1].split('．')[-1]
                        
                        if result_list[i].startswith(col_name) or result_list[i].endswith(col_name):
                            # print(result_list[i], result_list[i+1])
                            for j in range(i + 1, len(result_list)):
                                # cleaned_str = result_list[j].replace("'", "").replace(",", "").replace(" ", "")
                                cleaned_str = result_list[j].replace("'", "").replace(",", "")
                                
                                # print(result_list[j], cleaned_str)
                                item_value = cleaned_str
                                flag = checkflag(item_value)
                                if flag or item_value == '':
                                    continue
                                if not flag and col_name not in table_data.keys():
                                    table_data[col_name] = item_value
                                    # print("=> yes", col_name, item_value)
                                    break  # 找到数字后跳出内层循环
                else:
                    continue
                
                
    
    table_data['公司名称'] = company_name
    table_data['年份'] = year
    table_data['证券代码'] = company_code
    
    return table_data         

def loop_file(table_header, name_list, folder_path, questions, save_path):
    table_data = []
    
    table_path = save_path + '/question_table_data.xlsx'
        
    for question in questions:
        id = json.loads(question)['id']
        question_text = json.loads(question)['question']
        file = json.loads(question)['filename1']
        file2 = json.loads(question)['filename2']
        file3 = json.loads(question)['filename3']

        # if id != 132:
        #     continue
        #### first file
        if file == "":
            continue
        
        file_name = folder_path + "/" + file
        print(file_name)
        
        name_list.append(file_name)
        
    
        table_data_loc = extract_table_data(file_name,table_header)
        
        table_data_loc["id"] = id
        table_data.append(table_data_loc)

        # save_table_data(table_path, table_data)
        
        #### second file
        if file2 == "":
            continue
        
        file_name = folder_path + "/" + file2
        print(file_name)
        
        name_list.append(file_name)
        
    
        table_data_loc = extract_table_data(file_name,table_header)
        
        table_data_loc["id"] = id
        table_data.append(table_data_loc)
        
        # save_table_data(table_path, table_data)
        
        
        #### third file
        if file3 == "":
            continue
        
        file_name = folder_path + "/" + file3
        print(file_name)
        
        name_list.append(file_name)
    
        table_data_loc = extract_table_data(file_name,table_header)
        
        table_data_loc["id"] = id
        table_data.append(table_data_loc)
        
        # save_table_data(table_path, table_data)
        
        
    return table_data

def save_table_data(table_path, table_data):
    ## 保存表格数据
    writer = pd.ExcelWriter(table_path, engine='xlsxwriter')
    
    table_template={}
    table_template['id']  = ""
    table_template['公司名称'] = ""
    table_template['年份'] = ""
    table_template['证券代码'] = ""
    for item in table_header:
        table_template[item] = ""
        
    table_data = [table_template] + table_data
    
    for id in range(len(table_data)):
        table_tmp = pd.DataFrame(table_data[id], index=[id])
        if id > 0:
            table = pd.concat([table, table_tmp])
        else:
            table = table_tmp
                        
    table.to_excel(writer, index=False)
    
    writer.close()
    

if __name__ == '__main__':
    name_list = []
    dataset_path = '../dataset'
    
    save_path = '../dataset'
    
    table_header = []
    with open(dataset_path+"/table_new.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            if line.strip() != "":
                table_header.append(line.strip())
    
    filename = dataset_path + '/match_test.json'
    
    folder_path = '../data/alltxt'
    
    test_questions = open(filename,"r", encoding="utf-8").readlines()
    
    table_data = loop_file(table_header, name_list, folder_path, test_questions, save_path)
    
    
    table_path = save_path + '/question_table_data.xlsx'
    save_table_data(table_path, table_data)


