cd code
# 将问题与公司年报进行匹配
python match_txt.py

# 根据公司年报生成金融数据库
python txt_to_table_data.py

# 回答type3-2的问题
python answer_chatglm.py

# 回答type3-1的问题
cd ../langchain-ChatGLM-master
python answer_langchain.py

# 回答type1和type2的问题
cd ../code
python answer.py

# 将所有回答合并
python merge_answer.py