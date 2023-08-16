## 项目文件说明

- **code**
  - answer_chatglm.py：回答type3-2问题
  - answer.py：回答type1和type2问题
  - match_txt.py：将问题中的公司名称和年份映射到对应的年报文件
  - merge_answer.py：将所有类型的问题答案汇总到一个文件中
  - txt_to_table_data.py：提取年报txt中的关键金融字段到表格中
- **langchain-ChatGLM-master**
  - 依托开源项目https://github.com/chatchat-space/Langchain-Chatchat/tree/master
  - answer_langchain.py：回答type3-1问题
- **data**
  - 存放年报txt数据
- **dataset**
  - vector_files：存放年报txt对应的向量文件
  - answer.json：存放answer_chatglm.py回答的问题答案
  - answer_data.json：存放answer.py回答的问题答案
  - answers_lang.json：存放answer_langchain.py回答的问题答案
  - answer_total.json：存放汇总之后的问题答案，最高分答案
  - custom_dict.txt：jieba词典，用来生成match_test.json
  - match_test.json：存储包括问题，年份，及问题对应的年报txt文件名的词典
  - question_table_data.xlsx：存储txt_to_table_data.py提取出的年报数据
  - table_new.txt：定义重要的金融字段，作为question_table_data的列名
  - test_question.jsonl：比赛问到的问题



## 代码运行方式

```shell
cd code
```

#### 将问题与公司年报进行匹配
```shell
python match_txt.py
```

#### 根据公司年报生成金融数据库
```shell
python txt_to_table_data.py
```

#### 回答type3-2的问题
```shell
python answer_chatglm.py
```

#### 回答type3-1的问题

```shell
cd ../langchain-ChatGLM-master
python answer_langchain.py
```

#### 回答type1和type2的问题

```shell
cd ../code
python answer.py
```

#### 将所有回答合并

```shell
python merge_answer.py
```
