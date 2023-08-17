import json
import pandas as pd


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
        return 0  # 如果无法转换为数字，返回None

def replace_dollar_str(value):
    if type(value) == str:
        if "万元" in value:
            value = value.split("万元")[0]
            return float(value)*10000
    return value

def add_two(value1, value2):
    if pd.isna(value1):
        value1 = 0
    if pd.isna(value2):
        value2 = 0
    return convert_to_numeric(value1) + convert_to_numeric(value2)

def replace_num_str(value):
    if type(value) == str:
        value = value.replace(',', '').replace('\n','').replace('\r','')
    return value

def replace_return_str(value):
    if type(value) == str:
        value = value.replace('\n','').replace('\r','').replace(' ', '')
    return value

def replace_return_space_str(value):
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

def question_year(question_text):
    if '2019' in question_text:
        return '2019'
    if '2020' in question_text:
        return '2020'
    if '2021' in question_text:
        return '2021'
    return False

def check_growth_question(question_text):
    if "增长率" in question_text:
        return True
    return False

def check_law_people_question(question_text):
    if "法定代表人是否" in question_text or "法定代表人对比" in question_text or "法定代表人与" in question_text:
        return True
    return False
    
# 将问题和回答保存为JSON文件
def save_answers_to_json(answers, json_file_path):
    with open(json_file_path, 'w', encoding='utf-8') as file:
        for answer in answers:    
            json.dump(answer, file, ensure_ascii=False, indent=None)
            print("", file=file)

if __name__ == '__main__':
    
    dataset_path = '../dataset'
    
    
    filename = dataset_path + '/match_test.json'
        
    table_path = dataset_path + '/question_table_data.xlsx'
    df = pd.read_excel(table_path)
    
    
    # match_test.json中读取问题
    test_questions = read_questions_from_json(filename)

    
    # 使用模型回答问题并保存回答
    answers = []
    cnt = 0
    for item in test_questions:
        question_id = item["id"]
        question_text = item["question"]
        filename = item["filename1"]
        
        if filename == "":
            answer = "抱歉，经查询，无法回答问题"+question_text.split('？')[0].split('?')[0].split('。')[0].split('请问，')[-1].split('请问')[-1] + "。"
                
            answer_dict = {
                "id": question_id,
                "question": question_text,
                "answer": answer
            }
            answers.append(answer_dict)
            continue
        
        year_match = question_year(question_text)
        company_name_match = item["company_name"]
        
        security_code_match = filename.split('__')[2]
        company_short_name = filename.split('__')[3]
        matches = [company_name_match, security_code_match, company_short_name]
        

        if question_id >= 0:
            answer = ""
            row_index = df[df['id'] == question_id].index.tolist()
            
            if not row_index:
                answer = "抱歉，经查询，无法回答问题"+question_text.split('？')[0].split('?')[0].split('。')[0].split('请问，')[-1].split('请问')[-1] + "。"
                
                answer_dict = {
                    "id": question_id,
                    "question": question_text,
                    "answer": answer
                }
                answers.append(answer_dict)
                continue
            row_index = row_index[0]  # 获取匹配行的索引
            
            flag = check_growth_question(question_text)
            if flag:
                row_index2 = df[df['id'] == question_id].index.tolist()
                if not row_index2:
                    answer = "抱歉，经查询，无法回答问题"+question_text.split('？')[0].split('?')[0].split('。')[0].split('请问，')[-1].split('请问')[-1] + "。"
                
                    answer_dict = {
                        "id": question_id,
                        "question": question_text,
                        "answer": answer
                    }
                    answers.append(answer_dict)
                    continue
                row_index2_0 = row_index2[0]  # 获取匹配行的索引
                if(len(row_index2) > 1):
                    row_index2_1 = row_index2[1]
                else:
                    row_index2_1 = 0
            
            flag = check_law_people_question(question_text)
            if flag:
                row_index3 = df[df['id'] == question_id].index.tolist()
                row_index3_0 = 0
                row_index3_1 = 0
                row_index3_2 = 0
                if not row_index3:
                    answer = "抱歉，经查询，无法回答问题"+question_text.split('？')[0].split('?')[0].split('。')[0].split('请问，')[-1].split('请问')[-1] + "。"
                
                    answer_dict = {
                        "id": question_id,
                        "question": question_text,
                        "answer": answer
                    }
                    answers.append(answer_dict)
                    continue
                row_index3_0 = row_index3[0]  # 获取匹配行的索引
                if(len(row_index3) > 1):
                    row_index3_1 = row_index3[1]
                if(len(row_index3) > 2):
                    row_index3_2 = row_index3[2]
                    
            ##### 公司信息 #####
            if "证券代码" in question_text:
                answer = ""
                if year_match and company_name_match and security_code_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = security_code_match
                    # security_code = security_code_match.group(1)

                    # Store the extracted information in the answer string
                    answer = f"{year}年{company_name}的证券代码是{security_code}。"

            elif "证券简称" in question_text:
                value = replace_return_str(df.at[row_index, '股票简称'])
                if type(value) == str:
                    value = value.split("（")[0]
                    if value == "":
                        value = matches[2]
                elif pd.isna(value):
                    value = matches[2]
                answer = ""
                if year_match and company_name_match and security_code_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_name = value
                    # Store the extracted information in the answer string
                    answer = f"{year}年{company_name}的证券简称是{security_name}。"

                
            elif "电子信箱" in question_text or "电子邮箱" in question_text:
                value = df.at[row_index, '电子信箱']  
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    
                    answer = f"{year}年{company_name}的电子信箱是{security_code}。"

            elif "企业名称" in question_text:
                value = replace_return_str(df.at[row_index, '公司名称'])
                if value=="":
                    value = matches[0]
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的企业名称是{security_code}。"
                
            elif "外文名称" in question_text:
                value = replace_return_str(df.at[row_index, '公司的外文名称'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    
                    answer = f"{year}年{company_name}的外文名称是{security_code}。"

            elif "法定代表人是否" in question_text or "法定代表人对比" in question_text or "法定代表人与" in question_text:
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    if('2019-2021' in question_text or '2019至2021' in question_text):
                        if(row_index3_0 == 0 or row_index3_1 == 0 or row_index3_2 == 0):
                            answer = ""
                        else:
                            value0 = (df.at[row_index3_0, '公司的法定代表人']).split("先生")[0]
                            value1 = (df.at[row_index3_1, '公司的法定代表人']).split("先生")[0]
                            value2 = (df.at[row_index3_2, '公司的法定代表人']).split("先生")[0]
                            if(type(value0) == str):
                                value0 = value0.split("（")[0].strip()
                                value0 = value0.lower()
                            if(type(value1) == str):
                                value1 = value1.split("（")[0].strip()
                                value1 = value1.lower()
                            if(type(value2) == str):
                                value2 = value2.split("（")[0].strip()
                                value2 = value2.lower()
                            year0 = replace_return_str(df.at[row_index3_0, '年份'].split("年")[0]).split("年")[0]
                            year1 = replace_return_str(df.at[row_index3_1, '年份'].split("年")[0]).split("年")[0]
                            year2 = replace_return_str(df.at[row_index3_2, '年份'].split("年")[0]).split("年")[0]
                            if(value0 == value1 and value1 == value2):
                                answer = f"{year0}年{company_name}的法定代表人是{value0}，{year1}年{company_name}的法定代表人是{value1}，{year2}年{company_name}的法定代表人是{value2}，因此2019-2021年的法定代表人相同。"
                            else:
                                answer = f"{year0}年{company_name}的法定代表人是{value0}，{year1}年{company_name}的法定代表人是{value1}，{year2}年{company_name}的法定代表人是{value2}，因此2019-2021年的法定代表人不相同。"
                    else:
                        if(row_index3_0 == 0 or row_index3_1 == 0):
                            answer = ""
                        else:
                            value0 = (df.at[row_index3_0, '公司的法定代表人']).split("先生")[0]
                            value1 = (df.at[row_index3_1, '公司的法定代表人']).split("先生")[0]
                            year0 = replace_return_str(df.at[row_index3_0, '年份'].split("年")[0]).split("年")[0]
                            year1 = replace_return_str(df.at[row_index3_1, '年份'].split("年")[0]).split("年")[0]
                            if(type(value0) == str):
                                value0 = value0.split("（")[0].strip()
                                value0 = value0.lower()
                            if(type(value1) == str):
                                value1 = value1.split("（")[0].strip()
                                value1 = value1.lower()
                            if(value0 == value1):
                                answer = f"{year0}年{company_name}的法定代表人是{value0}，{year1}年{company_name}的法定代表人是{value1}，因此{year0}年和{year1}年的法定代表人相同。"
                            else:
                                answer = f"{year0}年{company_name}的法定代表人是{value0}，{year1}年{company_name}的法定代表人是{value1}，因此{year0}年和{year1}年的法定代表人不相同。"

            elif "法定代表人" in question_text:
                value = replace_return_str(df.at[row_index, '公司的法定代表人']).split("先生")[0]
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的法定代表人是{security_code}。"

            elif "注册地址" in question_text:
                value = replace_return_str(df.at[row_index, '注册地址'])
                if pd.isna(value):
                    value = replace_return_str(df.at[row_index, '办公地址'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的注册地址是{security_code}。"

            elif "办公地址" in question_text:
                value = replace_return_str(df.at[row_index, '办公地址'])
                if pd.isna(value):
                    value = replace_return_str(df.at[row_index, '注册地址'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的办公地址是{security_code}。"

            elif "网址" in question_text:
                value = df.at[row_index, '网址']  # 提取电子邮箱值
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的公司网址是{security_code}。"

            
            # type2
            ##### 增长率 ######
            elif "营业利润增长率" in question_text:
                if(row_index2_1 == 0):
                    answer = ""
                else:
                    value0 = replace_num_str(df.at[row_index2_0, '三、营业利润'])
                    value1 = replace_num_str(df.at[row_index2_1, '三、营业利润'])
                    year0 = df.at[row_index2_0,  '年份'].split("年")[0]
                    year1 = df.at[row_index2_1,  '年份'].split("年")[0]
                    if year_match and company_name_match:
                        year = year_match
                    # year = year_match.group(1)
                        company_name = company_name_match
                        value0 = convert_to_numeric(value0)
                        value1 = convert_to_numeric(value1)
                        if value1 == 0 or pd.isna(value1):
                            answer = ""
                        else:
                            security_code2 = round((value0 - value1) / abs(value1), 4)
                            answer = f"{year0}年{company_name}的营业利润是{value0}元，{year1}年{company_name}的营业利润是{value1}元，根据公式，营业利润增长率=(营业利润-上年营业利润)/上年营业利润，得出结果{company_name}{year0}的营业利润增长率是{'{:.2%}'.format(security_code2)}。"
                            
            elif "净利润增长率" in question_text:
                if(row_index2_1 == 0):
                    answer = ""

                else:
                    value0 = replace_num_str(df.at[row_index2_0, '五、净利润'])
                    value1 = replace_num_str(df.at[row_index2_1, '五、净利润'])
                    year0 = df.at[row_index2_0,  '年份'].split("年")[0]
                    year1 = df.at[row_index2_1,  '年份'].split("年")[0]
                    if year_match and company_name_match:
                        year = year_match
                    # year = year_match.group(1)
                        company_name = company_name_match
                        value0 = convert_to_numeric(value0)
                        value1 = convert_to_numeric(value1)
                        if value1 == 0 or pd.isna(value1):
                            answer = ""
                        else:
                            security_code2 = round((value0 - value1) / abs(value1), 4)
                            answer = f"{year0}年{company_name}的净利润是{value0}元，{year1}年{company_name}的净利润是{value1}元，根据公式，净利润增长率=(净利润-上年净利润)/上年净利润，得出结果{company_name}{year0}的净利润增长率是{'{:.2%}'.format(security_code2)}。"

            elif "固定资产增长率" in question_text:
                if(row_index2_1 == 0):
                    answer = ""

                else:
                    value0 = replace_num_str(df.at[row_index2_0, '固定资产'])
                    value1 = replace_num_str(df.at[row_index2_1, '固定资产'])
                    year0 = df.at[row_index2_0, '年份'].split("年")[0]
                    year1 = df.at[row_index2_1, '年份'].split("年")[0]
                    if year_match and company_name_match:
                        year = year_match
                    # year = year_match.group(1)
                        company_name = company_name_match
                        value0 = convert_to_numeric(value0)
                        value1 = convert_to_numeric(value1)
                        if value1 == 0 or pd.isna(value1):
                            answer = ""
                        else:
                            security_code2 = round((value0 - value1) / abs(value1), 4)
                            answer = f"{year0}年{company_name}的固定资产是{value0}元，{year1}年{company_name}的固定资产是{value1}元，根据公式，固定资产增长率=(固定资产-上年固定资产)/上年固定资产，得出结果{company_name}{year0}的固定资产增长率是{'{:.2%}'.format(security_code2)}。"

            elif "无形资产增长率" in question_text:
                if(row_index2_1 == 0):
                    answer = ""

                else:
                    value0 = replace_num_str(df.at[row_index2_0, '无形资产'])
                    value1 = replace_num_str(df.at[row_index2_1, '无形资产'])
                    year0 = df.at[row_index2_0, '年份'].split("年")[0]
                    year1 = df.at[row_index2_1, '年份'].split("年")[0]
                    if year_match and company_name_match:
                        year = year_match
                    # year = year_match.group(1)
                        company_name = company_name_match
                        value0 = convert_to_numeric(value0)
                        value1 = convert_to_numeric(value1)
                        if value1 == 0 or pd.isna(value1):
                            answer = ""
                        else:
                            security_code2 = round((value0 - value1) / abs(value1), 4)
                            answer = f"{year0}年{company_name}的无形资产是{value0}元，{year1}年{company_name}的无形资产是{value1}元，根据公式，无形资产增长率=(无形资产-上年无形资产)/上年无形资产，得出结果{company_name}{year0}的无形资产增长率是{'{:.2%}'.format(security_code2)}。"

            elif "总资产增长率" in question_text:
                if(row_index2_1 == 0):
                    answer = ""

                else:
                    value0 = replace_num_str(df.at[row_index2_0, '资产总计'])
                    if pd.isna(value0):
                        value0 = replace_num_str(df.at[row_index2_0, '总资产'])
                    if pd.isna(value0):
                        value0 = replace_num_str(df.at[row_index2_0, '资产总额'])
                    value1 = replace_num_str(df.at[row_index2_1, '资产总计'])
                    if pd.isna(value1):
                        value1 = replace_num_str(df.at[row_index2_1, '总资产'])
                    if pd.isna(value1):
                        value1 = replace_num_str(df.at[row_index2_1, '资产总额'])
                    year0 = df.at[row_index2_0, '年份'].split("年")[0]
                    year1 = df.at[row_index2_1, '年份'].split("年")[0]
                    if year_match and company_name_match:
                        year = year_match
                    # year = year_match.group(1)
                        company_name = company_name_match
                        value0 = convert_to_numeric(value0)
                        value1 = convert_to_numeric(value1)
                        if value1 == 0:
                            answer = ""
                        else:
                            security_code2 = round((value0 - value1) / abs(value1), 4)
                            answer = f"{year0}年{company_name}的总资产是{value0}元，{year1}年{company_name}的总资产是{value1}元，根据公式，总资产增长率=(总资产-上年总资产)/上年总资产，得出结果{company_name}{year0}的总资产增长率是{'{:.2%}'.format(security_code2)}。"

            elif "货币资金增长率" in question_text:
                if(row_index2_1 == 0):
                    answer = ""

                else:
                    value0 = replace_num_str(df.at[row_index2_0, '货币资金'])
                    value1 = replace_num_str(df.at[row_index2_1, '货币资金'])
                    year0 = df.at[row_index2_0, '年份'].split("年")[0]
                    year1 = df.at[row_index2_1, '年份'].split("年")[0]
                    if year_match and company_name_match:
                        year = year_match
                    # year = year_match.group(1)
                        company_name = company_name_match
                        value0 = convert_to_numeric(value0)
                        value1 = convert_to_numeric(value1)
                        if value1 == 0:
                            answer = ""
                        else:
                            security_code2 = round((value0 - value1) / abs(value1), 4)
                            answer = f"{year0}年{company_name}的货币资金是{value0}元，{year1}年{company_name}的货币资金是{value1}元，根据公式，货币资金增长率=(货币资金-上年货币资金)/上年货币资金，得出结果{company_name}{year0}的货币资金增长率是{'{:.2%}'.format(security_code2)}。"

            elif "管理费用增长率" in question_text:
                if(row_index2_1 == 0):
                    answer = ""

                else:
                    value0 = replace_num_str(df.at[row_index2_0, '管理费用'])
                    value1 = replace_num_str(df.at[row_index2_1, '管理费用'])
                    year0 = df.at[row_index2_0, '年份'].split("年")[0]
                    year1 = df.at[row_index2_1, '年份'].split("年")[0]
                    if year_match and company_name_match:
                        year = year_match
                    # year = year_match.group(1)
                        company_name = company_name_match
                        value0 = convert_to_numeric(value0)
                        value1 = convert_to_numeric(value1)
                        if value1 == 0:
                            answer = ""
                        else:
                            security_code2 = round((value0 - value1) / abs(value1), 4)
                            answer = f"{year0}年{company_name}的管理费用是{value0}元，{year1}年{company_name}的管理费用是{value1}元，根据公式，管理费用增长率=(管理费用-上年管理费用)/上年管理费用，得出结果{company_name}{year0}的管理费用增长率是{'{:.2%}'.format(security_code2)}。"

            elif "财务费用增长率" in question_text:
                if(row_index2_1 == 0):
                    answer = ""

                else:
                    value0 = replace_num_str(df.at[row_index2_0, '财务费用'])
                    value1 = replace_num_str(df.at[row_index2_1, '财务费用'])
                    year0 = df.at[row_index2_0, '年份'].split("年")[0]
                    year1 = df.at[row_index2_1, '年份'].split("年")[0]
                    if year_match and company_name_match:
                        year = year_match
                    # year = year_match.group(1)
                        company_name = company_name_match
                        value0 = convert_to_numeric(value0)
                        value1 = convert_to_numeric(value1)
                        if value1 == 0:
                            answer = ""
                        else:
                            security_code2 = round((value0 - value1) / abs(value1), 4)
                            answer = f"{year0}年{company_name}的财务费用是{value0}元，{year1}年{company_name}的财务费用是{value1}元，根据公式，财务费用增长率=(财务费用-上年财务费用)/上年财务费用，得出结果{company_name}{year0}的财务费用增长率是{'{:.2%}'.format(security_code2)}。"

            elif "流动负债增长率" in question_text:
                if(row_index2_1 == 0):
                    answer = ""

                else:
                    value0 = replace_num_str(df.at[row_index2_0, '流动负债合计'])
                    value1 = replace_num_str(df.at[row_index2_1, '流动负债合计'])
                    year0 = df.at[row_index2_0, '年份'].split("年")[0]
                    year1 = df.at[row_index2_1, '年份'].split("年")[0]
                    if year_match and company_name_match:
                        year = year_match
                    # year = year_match.group(1)
                        company_name = company_name_match
                        value0 = convert_to_numeric(value0)
                        value1 = convert_to_numeric(value1)
                        if value1 == 0:
                            answer = ""
                        else:
                            security_code2 = round((value0 - value1) / abs(value1), 4)
                            answer = f"{year0}年{company_name}的流动负债是{value0}元，{year1}年{company_name}的流动负债是{value1}元，根据公式，流动负债增长率=(流动负债-上年流动负债)/上年流动负债，得出结果{company_name}{year0}的流动负债增长率是{'{:.2%}'.format(security_code2)}。"

            elif "研发费用增长率" in question_text:
                if(row_index2_1 == 0):
                    answer = ""

                else:
                    value0 = replace_num_str(df.at[row_index2_0, '研发费用'])
                    value1 = replace_num_str(df.at[row_index2_1, '研发费用'])
                    year0 = df.at[row_index2_0, '年份'].split("年")[0]
                    year1 = df.at[row_index2_1, '年份'].split("年")[0]
                    if year_match and company_name_match:
                        year = year_match
                    # year = year_match.group(1)
                        company_name = company_name_match
                        value0 = convert_to_numeric(value0)
                        value1 = convert_to_numeric(value1)
                        if value1 == 0:
                            answer = ""
                        else:
                            security_code2 = round((value0 - value1) / abs(value1), 4)
                            answer = f"{year0}年{company_name}的研发费用是{value0}元，{year1}年{company_name}的研发费用是{value1}元，根据公式，研发费用增长率=(研发费用-上年研发费用)/上年研发费用，得出结果{company_name}{year0}的研发费用增长率是{'{:.2%}'.format(security_code2)}。"

            elif "营业收入增长率" in question_text:
                if(row_index2_1 == 0):
                    answer = ""

                else:
                    value0 = replace_num_str(df.at[row_index2_0, '营业收入'])
                    value1 = replace_num_str(df.at[row_index2_1, '营业收入'])
                    year0 = df.at[row_index2_0, '年份'].split("年")[0]
                    year1 = df.at[row_index2_1, '年份'].split("年")[0]
                    if year_match and company_name_match:
                        year = year_match
                    # year = year_match.group(1)
                        company_name = company_name_match
                        value0 = convert_to_numeric(value0)
                        value1 = convert_to_numeric(value1)
                        if value1 == 0:
                            answer = ""
                        else:
                            security_code2 = round((value0 - value1) / abs(value1), 4)
                            answer = f"{year0}年{company_name}的营业收入是{value0}元，{year1}年{company_name}的营业收入是{value1}元，根据公式，营业收入增长率=(营业收入-上年营业收入)/上年营业收入，得出结果{company_name}{year0}的营业收入增长率是{'{:.2%}'.format(security_code2)}。"

            elif "总负债增长率" in question_text:
                if(row_index2_1 == 0):
                    answer = ""

                else:
                    tmp1 = replace_num_str(df.at[row_index2_0, '流动负债合计'])
                    tmp2 = replace_num_str(df.at[row_index2_0, '非流动负债合计'])
                    value0 = add_two(tmp1, tmp2)
                    tmp1 = replace_num_str(df.at[row_index2_1, '流动负债合计'])
                    tmp2 = replace_num_str(df.at[row_index2_1, '非流动负债合计'])
                    value1 = add_two(tmp1, tmp2)
                    
                    year0 = df.at[row_index2_0, '年份'].split("年")[0]
                    year1 = df.at[row_index2_1, '年份'].split("年")[0]
                    if year_match and company_name_match:
                        year = year_match
                    # year = year_match.group(1)
                        company_name = company_name_match
                        value0 = convert_to_numeric(value0)
                        value1 = convert_to_numeric(value1)
                        if value1 == 0:
                            answer = ""
                        else:
                            security_code2 = round((value0 - value1) / abs(value1), 4)
                            answer = f"{year0}年{company_name}的总负债是{value0}元，{year1}年{company_name}的总负债是{value1}元，根据公式，总负债增长率=(总负债-上年总负债)/上年总负债，得出结果{company_name}{year0}的总负债增长率是{'{:.2%}'.format(security_code2)}。"
                
            elif "投资收益增长率" in question_text:
                if(row_index2_1 == 0):
                    answer = ""

                else:
                    value0 = replace_num_str(df.at[row_index2_0, '投资收益'])
                    value1 = replace_num_str(df.at[row_index2_1, '投资收益'])
                    year0 = df.at[row_index2_0, '年份'].split("年")[0]
                    year1 = df.at[row_index2_1, '年份'].split("年")[0]
                    if year_match and company_name_match:
                        year = year_match
                    # year = year_match.group(1)
                        company_name = company_name_match
                        value0 = convert_to_numeric(value0)
                        value1 = convert_to_numeric(value1)
                        if value1 == 0:
                            answer = ""
                        else:
                            security_code2 = round((value0 - value1) / abs(value1), 4)
                            answer = f"{year0}年{company_name}的投资收益是{value0}元，{year1}年{company_name}的投资收益是{value1}元，根据公式，投资收益增长率=(投资收益-上年投资收益)/上年投资收益，因此{company_name}在{year0}年相较于{year1}年的投资收益增长率是{'{:.2%}'.format(security_code2)}。"
            
            elif "销售费用增长率" in question_text:
                if(row_index2_1 == 0):
                    answer = ""

                else:
                    value0 = replace_num_str(df.at[row_index2_0, '销售费用'])
                    value1 = replace_num_str(df.at[row_index2_1, '销售费用'])
                    year0 = df.at[row_index2_0, '年份'].split("年")[0]
                    year1 = df.at[row_index2_1, '年份'].split("年")[0]
                    if year_match and company_name_match:
                        year = year_match
                    # year = year_match.group(1)
                        company_name = company_name_match
                        value0 = convert_to_numeric(value0)
                        value1 = convert_to_numeric(value1)
                        if value1 == 0:
                            answer = ""
                        else:
                            security_code2 = round((value0 - value1) / abs(value1), 4)
                            answer = f"{year0}年{company_name}的销售费用是{value0}元，{year1}年{company_name}的销售费用是{value1}元，根据公式，销售费用增长率=(销售费用-上年销售费用)/上年销售费用，得出结果{company_name}{year0}的销售费用增长率是{'{:.2%}'.format(security_code2)}。"

            elif "现金及现金等价物增长率" in question_text:
                if(row_index2_1 == 0):
                    answer = ""

                else:
                    value0 = replace_num_str(df.at[row_index2_0, '三、期末现金及现金等价物余额'])
                    value1 = replace_num_str(df.at[row_index2_1, '三、期末现金及现金等价物余额'])
                    year0 = df.at[row_index2_0, '年份'].split("年")[0]
                    year1 = df.at[row_index2_1, '年份'].split("年")[0]
                    if year_match and company_name_match:
                        year = year_match
                    # year = year_match.group(1)
                        company_name = company_name_match
                        value0 = convert_to_numeric(value0)
                        value1 = convert_to_numeric(value1)
                        if value1 == 0:
                            answer = ""
                        else:
                            security_code2 = round((value0 - value1) / abs(value1), 4)
                            answer = f"{year0}年{company_name}的现金及现金等价物是{value0}元，{year1}年{company_name}的现金及现金等价物是{value1}元，根据公式，现金及现金等价物增长率=(现金及现金等价物-上年现金及现金等价物)/上年现金及现金等价物，得出结果{company_name}{year0}的现金及现金等价物增长率是{'{:.2%}'.format(security_code2)}。"

            ##### 率、比率、比例、比值 #####
            elif "净利润率" in question_text:
                value = replace_num_str(df.at[row_index, '五、净利润'])
                value2 = replace_num_str(df.at[row_index, '营业收入'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = convert_to_numeric(value)
                    security_code2 = convert_to_numeric(value2)
                    if security_code2 == 0.0:
                        answer=""
                    else:
                        security_code3 = round(security_code / (security_code2), 4)
                        answer = f"{year}年{company_name}的净利润为{security_code}元，营业收入为{security_code2}元，根据公式，净利润率=净利润/营业收入，所以{year}年{company_name}的净利润率为{'{:.2%}'.format(security_code3)}"

            elif "营业利润率" in question_text:
                value = replace_num_str(df.at[row_index, '三、营业利润'])
                value2 = replace_num_str(df.at[row_index, '营业收入'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = convert_to_numeric(value)
                    security_code2 = convert_to_numeric(value2)
                    if security_code2 == 0:
                        answer = ""
                    else:
                        security_code3 = round(security_code / (security_code2), 4)
                        answer = f"{year}年{company_name}的营业利润为{security_code}元，营业收入为{security_code2}元，根据公式，营业利润率=营业利润/营业收入，所以{year}年{company_name}的营业利润率为{'{:.2%}'.format(security_code3)}"

            elif "营业成本率" in question_text:
                value = replace_num_str(df.at[row_index, '二、营业总成本'])
                value2 = replace_num_str(df.at[row_index, '营业收入'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = convert_to_numeric(value)
                    security_code2 = convert_to_numeric(value2)
                    if security_code2 == 0:
                        answer = ""
                    else:
                        security_code3 = round(security_code / (security_code2), 4)
                        answer = f"{year}年{company_name}的营业成本为{security_code}元，营业收入为{security_code2}元，根据公式，营业成本率=营业利润/营业收入，得出结果{year}年{company_name}的营业成本率是{'{:.2%}'.format(security_code3)}。"
            
            elif "资产负债比率" in question_text:
                tmp1 = replace_num_str(df.at[row_index, '流动负债合计'])
                tmp2 = replace_num_str(df.at[row_index, '非流动负债合计'])
                value = add_two(tmp1, tmp2)
                # value = replace_num_str(df.at[row_index, '负债合计'])
                value2 = replace_num_str(df.at[row_index, '资产总计'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = convert_to_numeric(value)
                    security_code2 = convert_to_numeric(value2)
                    if security_code2 == 0:
                        answer = ""
                    else :
                        security_code3 = round(security_code / (security_code2), 4)
                        answer = f"{year}年{company_name}的负债合计为{security_code}元，资产总计为{security_code2}元，根据公式，资产负债比率=负债总额/资产总额，得出结果{year}年{company_name}的资产负债比率是{'{:.2%}'.format(security_code3)}。"

            elif "现金比率" in question_text:
                value = replace_num_str(df.at[row_index, '货币资金'])
                if not value or not is_numeric(value):
                    value2 = replace_num_str(df.at[row_index, '库存现金'])
                    value3 = replace_num_str(df.at[row_index, '银行存款'])
                    value4 = replace_num_str(df.at[row_index, '其他货币资金'])
                    value = convert_to_numeric(value2) + convert_to_numeric(value3) + convert_to_numeric(value4)
                
                value2 = replace_num_str(df.at[row_index, '流动负债合计'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = convert_to_numeric(value)
                    security_code2 = convert_to_numeric(value2)
                    if security_code2 == 0:
                        answer = ""
                    else:
                        security_code3 = round(security_code / (security_code2), 4)
                        answer = f"{year}年{company_name}的货币资金为{security_code}元，流动负债合计为{security_code2}元，根据公式，现金比率=货币资金/流动负债，得出结果{year}年{company_name}的现金比率是{'{:.2%}'.format(security_code3)}。"

            elif "流动负债比率" in question_text:
                value = replace_num_str(df.at[row_index, '流动负债合计'])
                # value2 = replace_num_str(df.at[row_index, '负债合计'])
                tmp1 = replace_num_str(df.at[row_index, '流动负债合计'])
                tmp2 = replace_num_str(df.at[row_index, '非流动负债合计'])
                value2 = add_two(tmp1, tmp2)
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = convert_to_numeric(value)
                    security_code2 = convert_to_numeric(value2)
                    if security_code2 == 0:
                        answer = ""
                    else:
                        security_code3 = round(security_code / (security_code2), 4)
                        answer = f"{year}年{company_name}的流动负债合计为{security_code}元，负债总计为{security_code2}元，根据公式，流动负债比率=流动负债合计/总负债，得出结果{year}年{company_name}的流动负债比率是{'{:.2%}'.format(security_code3)}。"

            elif "非流动负债比率" in question_text:
                value = replace_num_str(df.at[row_index, '非流动负债合计'])
                # value2 = replace_num_str(df.at[row_index, '负债合计'])
                tmp1 = replace_num_str(df.at[row_index, '流动负债合计'])
                tmp2 = replace_num_str(df.at[row_index, '非流动负债合计'])
                value2 = add_two(tmp1, tmp2)
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = convert_to_numeric(value)
                    security_code2 = convert_to_numeric(value2)
                    if security_code2 == 0:
                        answer = ""
                    else:
                        security_code3 = round(security_code / (security_code2), 4)
                        answer = f"{year}年{company_name}的非流动负债合计为{security_code}元，总负债为{security_code2}元，根据公式，非流动负债比率=非流动负债合计/总负债，得出结果{year}年{company_name}的非流动负债比率是{'{:.2%}'.format(security_code3)}。"

            elif "管理费用率" in question_text:
                value = replace_num_str(df.at[row_index, '管理费用'])
                value2 = replace_num_str(df.at[row_index, '营业收入'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = convert_to_numeric(value)
                    security_code2 = convert_to_numeric(value2)
                    if security_code2 == 0:
                        answer = ""
                    else:
                        security_code3 = round(security_code / (security_code2), 4)
                        answer = f"{year}年{company_name}的管理费用为{security_code}元，营业收入为{security_code2}元，根据公式，管理费用率=管理费用/营业收入，得出结果{year}年{company_name}的管理费用率是{'{:.2%}'.format(security_code3)}。"

            elif "财务费用率" in question_text:
                value = replace_num_str(df.at[row_index, '财务费用'])
                value2 = replace_num_str(df.at[row_index, '营业收入'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = convert_to_numeric(value)
                    security_code2 = convert_to_numeric(value2)
                    if security_code2 == 0:
                        answer = ""
                    else:
                        security_code3 = round(security_code / (security_code2), 4)
                        answer = f"{year}年{company_name}的财务费用为{security_code}元，营业收入为{security_code2}元，根据公式，财务费用率=财务费用/营业收入，得出结果{year}年{company_name}的财务费用率是{'{:.2%}'.format(security_code3)}。"

            elif "毛利率" in question_text:
                value = replace_num_str(df.at[row_index, '营业收入'])
                value2 = replace_num_str(df.at[row_index, '二、营业总成本'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = convert_to_numeric(value)
                    security_code2 = convert_to_numeric(value2)
                    if security_code2 == 0:
                        answer = ""
                    else:
                        security_code3 = round((security_code2 - security_code) / (security_code2), 4)
                        answer = f"{year}年{company_name}的营业收入为{security_code}元，营业成本为{security_code2}元，根据公式，毛利率=(营业收入-营业成本)/营业收入，得出结果{year}年{company_name}的毛利率是{'{:.2%}'.format(security_code3)}。"

            elif "投资收益" in question_text and "营业收入" in question_text:
                value = replace_num_str(df.at[row_index, '投资收益'])
                if pd.isna(value):
                    value = replace_num_str(df.at[row_index, '投资收益（损失以“-”号'])
                value2 = replace_num_str(df.at[row_index, '营业收入'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = convert_to_numeric(value)
                    security_code2 = convert_to_numeric(value2)
                    if security_code2 == 0.0:
                        answer=""
                    else:
                        security_code3 = round(security_code / security_code2, 4)
                        answer = f"{year}年{company_name}的投资收益为{security_code}元，营业收入为{security_code2}元，根据公式，投资收益占营业收入比率=投资收益/营业收入，得出结果{year}年{company_name}的投资收益占营业收入比率是{'{:.2%}'.format(security_code3)}"
                answer_dict = {
                "id": question_id,
                "question": question_text,
                "answer": ""
                }
            
            elif "研发人员" in question_text and "职工人数" in question_text:
                value = replace_num_str(df.at[row_index, '公司研发人员'])
                if '%' in str(value) or pd.isna(value):
                    value = replace_num_str(df.at[row_index, '研发人员的数量'])
                if '%' in str(value) or pd.isna(value):
                    value = replace_num_str(df.at[row_index, '研发人员数量'])
                value2 = replace_num_str(df.at[row_index, '在职员工的数量合计'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    if not pd.isna(value) and '%' not in str(value):
                        security_code = int(float(value))
                    else:
                        security_code = 0
                    if not pd.isna(value2):
                        security_code2 = int(float(value2))
                    else:
                        security_code2 = 0
                    if security_code2 == 0:
                        answer = ""
                    else:
                        security_code3 = round(security_code / security_code2, 2)
                        answer = f"{year}年{company_name}的研发人员数是{security_code}，职工总数是{security_code2}，根据公式，研发人员占职工人数比例=研发人员数/职工总数，得出结果{year}年{company_name}研发人员占职工人数比例是{security_code3}。"
                
            elif "硕士及以上" in question_text and "职工人数" in question_text:
                value = replace_num_str(df.at[row_index, '硕士及以上'])
                value2 = 0
                if pd.isna(value):
                    value = replace_num_str(df.at[row_index, '研究生及以上'])
                
                if type(value)==str and '.' in value:
                    year = year_match
                    company_name = company_name_match
                    answer = f"{year}年{company_name}硕士及以上人数占职工人数比例是{value}。"
               
                else:
                    if pd.isna(value):
                        value = replace_num_str(df.at[row_index, '硕士'])
                        if pd.isna(value):
                            value = replace_num_str(df.at[row_index, '研究生'])
                        value2 = replace_num_str(df.at[row_index, '博士'])
                    
                    if not pd.isna(value2) and not pd.isna(value):
                        value = int(value) + int(value2)
                    elif not pd.isna(value2):
                        value = value2
                    elif not pd.isna(value):
                        value = value
                    else:
                        value = 0
                    value3 = replace_num_str(df.at[row_index, '在职员工的数量合计'])
                    
                    
                    answer = ""
                    if year_match and company_name_match:
                        year = year_match
                        # year = year_match.group(1)
                        company_name = company_name_match
                        security_code = int(value)
                        
                        if value3 == 0 or pd.isna(value3) or value == 0:
                            answer = ""
                        else:
                            security_code3 = int(value3)
                            security_code4 = round(security_code / security_code3, 2)
                            answer = f"{year}年{company_name}的硕士及以上人数是{security_code}，职工总人数是{security_code3}，根据公式，企业硕士及以上人员占职工人数比例=(硕士人数+博士及以上人数)/职工总数，得出结果{year}年{company_name}硕士及以上人数占职工人数比例是{'{:.2f}'.format(security_code4)}。"

            elif "研发经费" in question_text and "费用" in question_text:
                value = replace_num_str(df.at[row_index, '研发费用'])
                value2 = replace_num_str(df.at[row_index, '销售费用'])
                value3 = replace_num_str(df.at[row_index, '管理费用'])
                value4 = replace_num_str(df.at[row_index, '财务费用'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = convert_to_numeric(value)
                    security_code2 = convert_to_numeric(value2)
                    security_code3 = convert_to_numeric(value3)
                    security_code4 = convert_to_numeric(value4)
                    sum = (security_code + security_code2 + security_code3 + security_code4)
                    if sum == 0:
                        answer=""
                    else:
                        security_code5 = round(security_code / sum, 2)
                        answer = f"{year}年{company_name}的研发费用为{security_code}元，销售费用为{security_code2}元，管理费用为{security_code3}元，财务费用为{security_code4}元。根据公式，研发经费占费用比例=研发费用/(研发费用+销售费用+管理费用+财务费用)，得出结果{year}年{company_name}研发经费占费用比例为{security_code5}。"

            elif "研发经费" in question_text and "利润" in question_text:
                value = replace_num_str(df.at[row_index, '研发费用'])
                value2 = replace_num_str(df.at[row_index, '五、净利润'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = convert_to_numeric(value)
                    security_code2 = convert_to_numeric(value2)
                    if security_code2 == 0:
                        answer = ""
                    else:
                        security_code3 = round(security_code / security_code2, 2)
                        answer = f"{year}年{company_name}的研发费用为{security_code}元，净利润为{security_code2}元，根据公式，研发经费与利润比值=研发费用/净利润，得出结果{year}年{company_name}研发经费与利润的比值为{security_code3}。"

            elif "研发经费" in question_text and "营业收入" in question_text:
                value = replace_num_str(df.at[row_index, '研发费用'])
                value2 = replace_num_str(df.at[row_index, '营业收入'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = convert_to_numeric(value)
                    security_code2 = convert_to_numeric(value2)
                    if security_code2 == 0:
                        answer = ""
                    else:
                        security_code3 = round(security_code / security_code2, 2)
                        answer = f"{year}年{company_name}的研发费用为{security_code}元，营业收入为{security_code2}元，根据公式，研发经费与营业收入比值=研发费用/营业收入，得出结果{year}年{company_name}研发经费与营业收入的比值为{security_code3}。"

            elif "速动比率" in question_text:
                value = replace_num_str(df.at[row_index, '流动资产合计'])
                value2 = replace_num_str(df.at[row_index, '存货'])
                value3 = replace_num_str(df.at[row_index, '流动负债合计'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = convert_to_numeric(value)
                    security_code2 = convert_to_numeric(value2)
                    security_code3 = convert_to_numeric(value3)
                    if security_code3 == 0:
                        answer = ""
                    else :
                        security_code4 = round((security_code - security_code2) / security_code3, 2)
                        answer = f"{year}年{company_name}的流动资产为{security_code}元，存货为{security_code2}元，流动负债合计为{security_code3}元，根据公式，速动比率=(流动资产-存货)/流动负债，得出结果{year}年{company_name}速动比率为{security_code4}。"

            elif "流动比率" in question_text:
                value = replace_num_str(df.at[row_index, '流动资产合计'])
                value2 = replace_num_str(df.at[row_index, '流动负债合计'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = convert_to_numeric(value)
                    security_code2 = convert_to_numeric(value2)
                    security_code3 = round(security_code / security_code2, 2)
                    answer = f"{year}年{company_name}的流动资产为{security_code}元，流动负债合计为{security_code2}元，根据公式，流动比率=流动资产/流动负债合计，得出结果{year}年{company_name}流动比率为{security_code3}。"

            elif "三费" in question_text:
                value = replace_num_str(df.at[row_index, '销售费用'])
                value2 = replace_num_str(df.at[row_index, '管理费用'])
                value3 = replace_num_str(df.at[row_index, '财务费用'])
                value4 = replace_num_str(df.at[row_index, '营业收入'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = convert_to_numeric(value)
                    security_code2 = convert_to_numeric(value2)
                    security_code3 = convert_to_numeric(value3)
                    security_code4 = convert_to_numeric(value4)
                    if security_code4 == 0.0:
                        answer = ""
                    else:
                        security_code5 = round((security_code + security_code2 + security_code3) / security_code4, 2)
                        answer = f"{year}年{company_name}的销售费用为{security_code}元，管理费用为{security_code2}元，财务费用为{security_code3}元，营业收入为{security_code4}元，根据公式，三费比重=(销售费用+管理费用+财务费用)/营业收入，得出结果{year}年{company_name}三费比重为{security_code5}。"

            
            ##### 主要会计数据和财务指标 #####
            elif "营业收入" in question_text and "营业外收入" in question_text:
                value = replace_num_str(df.at[row_index, '营业收入']  )
                value2 = replace_num_str(df.at[row_index, '加：营业外收入'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    security_code2 = value2
                    answer = f"{year}年{company_name}的营业收入是{security_code}元，营业外收入是{security_code2}元。"

            elif "营业外支出" in question_text and "营业外收入" in question_text:
                value = replace_num_str(df.at[row_index, '减：营业外支出'])
                value2 = replace_num_str(df.at[row_index, '加：营业外收入'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    security_code2 = value2
                    answer = f"{year}年{company_name}的营业外支出是{security_code}元,营业外收入是{security_code2}元。"

            elif "营业收入" in question_text:
                value = replace_num_str(df.at[row_index, '营业收入'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的营业收入是{security_code}元。"

            elif "营业外收入" in question_text:
                value = replace_num_str(df.at[row_index, '加：营业外收入'] )
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的营业外收入是{security_code}元。"

            elif "营业外支出" in question_text:
                value = replace_num_str(df.at[row_index, '减：营业外支出']) 
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的营业外支出是{security_code}元。"
            
            elif "每股经营现金流量" in question_text:
                value1 = replace_num_str(df.at[row_index, '经营活动产生的现金流量净额'])
                value2 = replace_num_str(df.at[row_index, '投资活动产生的现金流量净额'])
                value3 = replace_num_str(df.at[row_index, '筹资活动产生的现金流量净额'])
                value4 = replace_dollar_str(replace_num_str(df.at[row_index, '实收资本']))
                if pd.isna(value4):
                    value4 = replace_dollar_str(replace_num_str(df.at[row_index, '股本']))
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    value4 = convert_to_numeric(value4)
                    if pd.isna(value4) or value4 == 0:
                        security_code2 = 0
                    else:
                        security_code2 = (convert_to_numeric(value1) + convert_to_numeric(value2) + convert_to_numeric(value3)) / convert_to_numeric(value4)
                        # answer = f"{year}年{company_name}的每股经营现金流量=（经营活动产生的现金流量净额+投资活动产生的现金流量净额+筹资活动产生的现金流量净额）/实收资本，根据公式，所以每股经营现金流量为（{convert_to_numeric(value1)}+{convert_to_numeric(value2)}+{convert_to_numeric(value3)}/{convert_to_numeric(value4)}={'{:.2f}'.format(security_code2)}元。"
                        
                        answer = f"{year}年{company_name}的每股经营现金流量是{'{:.3f}'.format(security_code2)}元。"
                
            elif "每股收益" in question_text and "每股净资产" in question_text:
                value = replace_num_str(df.at[row_index, '基本每股收益'])
                value2 = replace_num_str(df.at[row_index, '资产总计'])
                # value3 = replace_num_str(df.at[row_index, '负债合计'])
                tmp1 = replace_num_str(df.at[row_index, '流动负债合计'])
                tmp2 = replace_num_str(df.at[row_index, '非流动负债合计'])
                value3 = add_two(tmp1, tmp2)
                value4 = replace_dollar_str(replace_num_str(df.at[row_index, '实收资本']))
                if pd.isna(value4):
                    value4 = replace_dollar_str(replace_num_str(df.at[row_index, '股本']))
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    value4 = convert_to_numeric(value4)
                    if pd.isna(value4) or value4 == 0:
                        security_code2 = 0
                        answer = f"{year}年{company_name}的每股收益是{convert_to_numeric(value)}元。"
                    else:
                        security_code = convert_to_numeric(value)
                        security_code2 = (convert_to_numeric(value2) - convert_to_numeric(value3)) / convert_to_numeric(value4)
                    # answer = f"{year}年{company_name}的每股收益是{convert_to_numeric(security_code)}元，每股净资产=（资产总额-负债总额）/实收资本，根据公式，得出结果{year}年{company_name}的（{convert_to_numeric(value2)}-{convert_to_numeric(value3)}/{convert_to_numeric(value4)}={security_code2}元。"
                        answer = f"{year}年{company_name}的每股收益是{convert_to_numeric(security_code)}元，每股净资产是{'{:.4f}'.format(security_code2)}元。"

            
            elif "每股净资产" in question_text:
                value2 = replace_num_str(df.at[row_index, '资产总计'])
                # value3 = replace_num_str(df.at[row_index, '负债合计'])
                tmp1 = replace_num_str(df.at[row_index, '流动负债合计'])
                tmp2 = replace_num_str(df.at[row_index, '非流动负债合计'])
                value3 = add_two(tmp1, tmp2)
                value4 = replace_dollar_str(replace_num_str(df.at[row_index, '实收资本']))
                if pd.isna(value4):
                    value4 = replace_dollar_str(replace_num_str(df.at[row_index, '股本']))
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    if pd.isna(value4):
                        security_code2 = 0
                    else:
                        security_code = convert_to_numeric(value)
                        security_code2 = (convert_to_numeric(value2) - convert_to_numeric(value3)) / convert_to_numeric(value4)
                    # answer = f"{year}年{company_name}的每股收益是{convert_to_numeric(security_code)}元，每股净资产=（资产总额-负债总额）/实收资本，根据公式，得出结果{year}年{company_name}的（{convert_to_numeric(value2)}-{convert_to_numeric(value3)}/{convert_to_numeric(value4)}={security_code2}元。"
                        answer = f"{year}年{company_name}的每股净资产是{'{:.4f}'.format(security_code2)}元。"
            
            elif "资产总计" in question_text:
                value = replace_num_str(df.at[row_index, '资产总计'])
                if pd.isna(value):
                    value = replace_num_str(df.at[row_index, '总资产'])
                if pd.isna(value):
                    value = replace_num_str(df.at[row_index, '资产总额'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的资产总计是{convert_to_numeric(security_code)}元。"

            
            #####  费用类  #####
            elif "销售费用" in question_text and "管理费用" in question_text:
                value = replace_num_str(df.at[row_index, '销售费用'])
                value2 = replace_num_str(df.at[row_index, '管理费用'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    security_code2 = value2
                    answer = f"{year}年{company_name}的销售费用是{security_code}元，管理费用是{security_code2}元。"

            elif "研发费用" in question_text and "财务费用" in question_text:
                value = replace_num_str(df.at[row_index, '研发费用'])
                value2 = replace_num_str(df.at[row_index, '财务费用'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    security_code2 = value2
                    answer = f"{year}年{company_name}的研发费用是{security_code}元，财务费用是{security_code2}元。"

            elif "销售费用" in question_text:
                value = replace_num_str(df.at[row_index, '销售费用'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的销售费用是{security_code}元。"

            elif "管理费用" in question_text:
                value = replace_num_str(df.at[row_index, '管理费用']) 
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的管理费用是{security_code}元。"

            elif "研发费用" in question_text:
                value = replace_num_str(df.at[row_index, '研发费用'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的研发费用是{security_code}元。"

            elif "财务费用" in question_text:
                value = replace_num_str(df.at[row_index, '财务费用'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的财务费用是{security_code}元。"

            
            #####  研发投入 #####
            elif "研发人员数" in question_text:
                value = replace_num_str(df.at[row_index, '公司研发人员'])
                if '%' in str(value) or pd.isna(value):
                    value = replace_num_str(df.at[row_index, '研发人员的数量'])
                if '%' in str(value) or pd.isna(value):
                    value = replace_num_str(df.at[row_index, '研发人员数量'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    if pd.isna(value):
                        answer = ""
                    else:
                        security_code = int(float(value))
                        answer = f"{year}年{company_name}的研发人员数是{security_code}。"
                
            #####  员工数量、专业构成及教育程度  ##### 
            elif "职工总数" in question_text:
                value = replace_num_str(df.at[row_index, '在职员工的数量合计'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的职工总数是{security_code}。"

            elif "技术人员" in question_text:
                value = replace_num_str(df.at[row_index, '技术人员'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的技术人员数是{security_code}。"

            elif "博士" in question_text:
                value = replace_num_str(df.at[row_index, '博士'])
                if pd.isna(value):
                    value = replace_num_str(df.at[row_index, '博士及以上'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的博士及以上人数是{security_code}。"

            elif "硕士" in question_text:
                value = replace_num_str(df.at[row_index, '硕士'])
                if not pd.isna(value):
                    value = int(value)
                else:
                    value = replace_num_str(df.at[row_index, '硕士及以上'])
                answer = ""
                if year_match and company_name_match and not pd.isna(value):
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的硕士人数是{security_code}。"
                
            # 12-2-1 合并资产负债表
            elif "货币资金" in question_text:
                value = replace_num_str(df.at[row_index, '货币资金'])
                if not value or not is_numeric(value):
                    value2 = replace_num_str(df.at[row_index, '库存现金'])
                    value3 = replace_num_str(df.at[row_index, '银行存款'])
                    value4 = replace_num_str(df.at[row_index, '其他货币资金'])
                    value = convert_to_numeric(value2) + convert_to_numeric(value3) + convert_to_numeric(value4)
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的货币资金是{security_code}元。"
                

            elif "应收款项融资" in question_text:
                value = replace_num_str(df.at[row_index, '应收款项融资'])
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的应收款项融资是{security_code}元。"

            elif "衍生金融资产" in question_text and "其他非流动金融资产" in question_text:
                value = replace_num_str(df.at[row_index, '衍生金融资产'])
                value2 = replace_num_str(df.at[row_index, '其他非流动金融资产'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    security_code2 = value2
                    answer = f"{year}年{company_name}的衍生金融资产是{security_code}元，其他非流动金融资产是{security_code2}元。"

            elif "衍生金融资产" in question_text:
                value = replace_num_str(df.at[row_index, '衍生金融资产'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的衍生金融资产是{security_code}元。"

            elif "其他非流动金融资产" in question_text:
                value = replace_num_str(df.at[row_index, '其他非流动金融资产'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的其他非流动金融资产是{security_code}元。"

            elif "固定资产" in question_text and "无形资产" in question_text:
                value = replace_num_str(df.at[row_index, '固定资产'])
                value2 = replace_num_str(df.at[row_index, '无形资产'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    security_code2 = value2
                    answer = f"{year}年{company_name}的固定资产是{security_code}元，无形资产是{security_code2}元。"

            elif "固定资产" in question_text:
                value = replace_num_str(df.at[row_index, '固定资产'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的固定资产是{security_code}元。"

            elif "无形资产" in question_text:
                value = replace_num_str(df.at[row_index, '无形资产']) 
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的无形资产是{security_code}元。"

            elif "负债合计" in question_text:
                tmp1 = replace_num_str(df.at[row_index, '流动负债合计'])
                tmp2 = replace_num_str(df.at[row_index, '非流动负债合计'])
                value = add_two(tmp1, tmp2)
                # value = replace_num_str(df.at[row_index, '负债合计'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的负债合计是{security_code}元。"

            elif "应付职工薪酬" in question_text:
                value = replace_num_str(df.at[row_index, '应付职工薪酬'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的应付职工薪酬是{security_code}元。"

            
            ##### 12-2-3 合并利润表【570】 #####
            elif "营业成本" in question_text and "营业利润" in question_text:
                value = replace_num_str(df.at[row_index, '二、营业总成本'])
                value2 = replace_num_str(df.at[row_index, '三、营业利润'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    security_code2 = value2
                    answer = f"{year}年{company_name}的营业成本是{security_code}元，营业利润是{security_code2}元。"

            elif "营业成本" in question_text:
                value = replace_num_str(df.at[row_index, '二、营业总成本']) 
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的营业成本是{security_code}元。"

            elif "营业税金及附加" in question_text:
                value = replace_num_str(df.at[row_index, '税金及附加'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的营业税金及附加是{security_code}元。"

            
            elif "营业利润" in question_text:
                value = replace_num_str(df.at[row_index, '三、营业利润'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的营业利润是{security_code}元。"

            elif "利润总额" in question_text and "净利润" in question_text:
                value = replace_num_str(df.at[row_index, '四、利润总额'])
                value2 = replace_num_str(df.at[row_index, '五、净利润'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    security_code2 = value2
                    answer = f"{year}年{company_name}的利润总额是{security_code}元，净利润是{security_code2}元。"

            elif "利润总额" in question_text:
                value = replace_num_str(df.at[row_index, '四、利润总额'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的利润总额是{security_code}元。"

            elif "所得税费用" in question_text:
                value = replace_num_str(df.at[row_index, '减：所得税费用'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的所得税费用是{security_code}元。"

            elif "母公司所有者" in question_text and "净利润" in question_text:
                value = replace_num_str(df.at[row_index, '归属于母公司所有者的净利润'])
                if pd.isna(value):
                    value = replace_num_str(df.at[row_index, '归属于母公司股东的净利润'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的归属母公司所有者的净利润是{security_code}元。"
            
            elif "净利润" in question_text:
                value = replace_num_str(df.at[row_index, '五、净利润'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的净利润是{security_code}元。"

            elif "综合收益总额" in question_text:
                value = replace_num_str(df.at[row_index, '七、综合收益总额']) 
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的综合收益总额是{security_code}元。"

            elif "对联营企业和合营企业的投资收益" in question_text:
                value = replace_num_str(df.at[row_index, '其中：对联营企业和合营'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}对联营企业和合营企业的投资收益是{security_code}元。"

            elif "投资收益" in question_text:
                value = replace_num_str(df.at[row_index, '投资收益'])
                if pd.isna(value):
                    value = replace_num_str(df.at[row_index, '投资收益（损失以“-”号'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的投资收益是{security_code}元。"

            elif "公允价值变动收益" in question_text:
                value = replace_num_str(df.at[row_index, '公允价值变动收益'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的公允价值变动收益是{security_code}元。"
            
            
            #####  12-2-5 合并现金流量表【50】 ##### 
            elif "收回投资" in question_text:
                value = replace_num_str(df.at[row_index, '收回投资收到的现金'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的收回投资收到的现金是{security_code}元。"

                
            #####  12-66 财务费用【150】 ##### 
            elif "利息支出" in question_text and "利息收入" in question_text:
                value = replace_num_str(df.at[row_index, '利息支出'])
                value2 = replace_num_str(df.at[row_index, '利息收入'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    security_code2 = value2
                    answer = f"{year}年{company_name}的利息支出是{security_code}元，利息收入是{security_code2}元。"

            elif "利息支出" in question_text:
                value = replace_num_str(df.at[row_index, '利息支出'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的利息支出是{security_code}元。"

            elif "利息收入" in question_text:
                value = replace_num_str(df.at[row_index, '利息收入'])
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的利息收入是{security_code}元。"

            
            #####  12-79-4 现金和现金等 价物的构成【50】 ##### 
            elif "现金及现金等价物余额" in question_text:
                value = replace_num_str(df.at[row_index, '三、期末现金及现金等价物余额']) 
                answer = ""
                if year_match and company_name_match:
                    year = year_match
                    # year = year_match.group(1)
                    company_name = company_name_match
                    security_code = value
                    answer = f"{year}年{company_name}的期末现金及现金等价物余额是{security_code}元。"

            
            else:
                answer = ""
            
            
        ########
        
        if answer == "" or "nan" in answer:
            answer = "抱歉，经查询，无法回答问题"+question_text.split('？')[0].split('?')[0].split('。')[0].split('请问，')[-1].split('请问')[-1] + "。"
        
        answer_dict = {
            "id": question_id,
            "question": question_text,
            "answer": answer
        }
        answers.append(answer_dict)

            
    # 将回答保存为answers.json文件
    save_answers_to_json(answers, dataset_path + "/answers_data.json")
