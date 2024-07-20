#本程序包含用于各项任务的提示词，由项目内其它程序调用，使用前需要在send函数填写自己使用的模型的api地址和api key。
#question()函数调用Ollama中的模型，需要更换为已安装的对长文本支持较好的模型。
# python3
# Please install OpenAI SDK first：`pip3 install openai`
from openai import OpenAI
import requests
import json

def put(text):
    url = "http://localhost:11434/api/generate"
    data = {"model": "internlm2:latest", "prompt":text}

    response = requests.post(url, json=data, stream=True)
    output_string = ""

    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            json_line = json.loads(decoded_line)
            if "created_at" in json_line and "done" in json_line:
                response_content = json_line.get("response", "")
                if response_content:
                    output_string += response_content

    return(output_string)

def send(system,user):
    client = OpenAI(api_key=" ", base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-coder",
        messages=[
            {"role": "system", "content":system},
            {"role": "user", "content":user},
        ],
        stream=False
    )

    return(response.choices[0].message.content)

def question(content,question):
    output=put("根据文档内容回答后面的问题："+content+"问题内容:"+question)
    return(output)

def document_read(question):
    prompt='''请根据以下要求，写一个在当前目录运行的Python程序：
1.根据后面的问题，通过程序读取当前目录下“document”文件夹中需要处理的文件。
2.读取文件时默认采用utf-8编码，把文件开头4000字符（文件不足4000字符则读取整个文件）输出到命令行。
3.如果根据问题需要读取多个文件，问题中说明文件形式相同或处理方式相同则只读取第一个文件，问题中未说明文件形式或处理方式是否相同则读取问题中提到的所有文件并每个文件开头添加括号，在括号中添加相应文件的文件名；在每个文件末尾换行并添加“--end----”字符。
4.注意本次要编写的程序只包括读取和输出文件的功能，问题中提到的处理要求应当在下一个程序实现。'''
    output=send(prompt,"问题如下："+question)
    return(output)

def document_modify(document_read,question):
    prompt='''请根据以下要求，写一个在当前目录运行的Python程序：
1.根据后面读取的当前目录下“document”文件夹中的文件开头部分内容（最后一组元素可能因字数限制被截断，分析时忽略最后一组元素）确定处理方法并编写程序实现后面的问题中的处理要求。
2.如果根据问题需要处理多个文件，在读取的文件开头包含括号且括号中包含文件名的情况下，在编写的程序中只处理相应文件名的文件；文件开头不包含文件名则需要对问题中提到的所有文件进行相同的处理。
3.如果问题中没有另做说明，处理后的文件以相同文件名保存到当前目录下的“modified”文件夹，如果当前目录没有“modified”文件夹则创建该文件夹。'''
    output=send(prompt+"读取到的文件内容如下："+document_read,"问题如下："+question)
    return(output)

