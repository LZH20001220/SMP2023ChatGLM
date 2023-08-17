from transformers import AutoTokenizer, AutoModel
import json

# 加载模型和tokenizer
tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm2-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/chatglm2-6b", trust_remote_code=True).half().cuda()
model = model.eval()

# 从JSON文件中读取问题数据
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

def check_type3(question_text):
    if "2019" in question_text:
        return False
    if "2020" in question_text:
        return False
    if "2021" in question_text:
        return False
    else:
        return True
    
if __name__ == '__main__':
    # 从test_questions.jsonl中读取问题
    test_questions = read_questions_from_json("../dataset/test_questions.jsonl")

    # 使用模型回答问题并保存回答
    answers = []
    
    cnt = 0
    for item in test_questions:
        
        question_id = item["id"]
        question_text = item["question"]
        
        flag = check_type3(question_text)
        
        if flag == False:
            response = ""
        
        else:
            # 调用模型进行回答
            response, _ = model.chat(tokenizer, question_text, history=[])
            response = response.replace("\n\n", "")

        # 将问题和回答保存为字典格式
        answer_dict = {
            "id": question_id,
            "question": question_text,
            "answer": response
        }
        answers.append(answer_dict)
    
    
    # 将回答保存为answer.json文件
    save_answers_to_json(answers, "../dataset/answers.json")
