import json


def read_questions_from_json(json_file_path):
    questions = []
    with open(json_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            question = json.loads(line)
            questions.append(question)
    return questions

# 将问题和回答保存为JSON文件
def save_answers_to_json(answers, json_file_path):
    with open(json_file_path, 'w', encoding='utf-8') as file:
        for answer in answers:    
            json.dump(answer, file, ensure_ascii=False, indent=None)
            print("", file=file)


if __name__ == '__main__':
    
    # 读取JSON文件
    dataset_path = "../dataset"
    src_path = dataset_path +"/answers_lang.json"
    des_path = dataset_path +"/answers.json"

    srcs = read_questions_from_json(src_path)
    dests = read_questions_from_json(des_path)

    # 提取包含"情况"的"id"字段并保存在列表中
    ids_with_keyword = []
    answers = []
    for dest in dests:
        dest_id = dest["id"]
        dest_question = dest["question"]
        dest_answer = dest["answer"]
        # print(dest_answer)
        if dest_answer == "":
            for src in srcs:
                src_id = src["id"]
                src_question = src["question"]
                src_answer = src["answer"]
                # print(dest_answer)
                if src_id == dest_id and src_answer != "":
                    dest_answer = src_answer
                    dest["answer"] = dest_answer
                    # print(dest["answer"] )
        answers.append(dest)
        

    save_answers_to_json(answers, dataset_path +"/answers_total.json")
    
    
    
    src_path = dataset_path +"/answers_data.json"
    des_path = dataset_path +"/answers_total.json"

    srcs = read_questions_from_json(src_path)
    dests = read_questions_from_json(des_path)

    # 提取包含"情况"的"id"字段并保存在列表中
    ids_with_keyword = []
    answers = []
    for dest in dests:
        dest_id = dest["id"]
        dest_question = dest["question"]
        dest_answer = dest["answer"]
        # print(dest_answer)
        if dest_answer == "":
            for src in srcs:
                src_id = src["id"]
                src_question = src["question"]
                src_answer = src["answer"]
                # print(dest_answer)
                if src_id == dest_id and src_answer != "":
                    dest_answer = src_answer
                    dest["answer"] = dest_answer
                    # print(dest["answer"] )
        answers.append(dest)
        

    save_answers_to_json(answers, dataset_path +"/answers_total.json")

    