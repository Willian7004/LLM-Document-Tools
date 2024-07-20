#This program contains prompt words for each task, if it is called by other programs in the project, you need to fill in the API address and API key of the model you are using in the send function before using it.
#question() function calls the model in Ollama and needs to be replaced with an installed model that supports long text well.
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
    output=put("Answer the questions that follow according to the content of the document："+content+"Question content:"+question)
    return(output)

def document_read(question):
    prompt='''Please write a Python program that runs in the current directory according to the following requirements：
1. According to the following question, read the files that need to be processed in the "document" folder in the current directory through the program.
2. When reading the file, the default is UTF-8 encoding, and the first 4000 characters of the file (the file is less than 4000 characters, the whole file is read) is output to the command line.
3. If multiple files need to be read according to the question, and the question states that the file form is the same or the processing method is the same, only the first file is read, and if the file form or processing method is not stated in the question, then read all the files mentioned in the question, and add parentheses at the beginning of each file, and add the file name of the corresponding file in the parentheses; Wrap lines at the end of each file and add the "--end----" character.
4. Note that the program to be written this time only includes the function of reading and outputting files, and the processing requirements mentioned in the question should be implemented in the next program.'''
    output=send(prompt,"The questions are as follows："+question)
    return(output)

def document_modify(document_read,question):
    prompt='''Please write a Python program that runs in the current directory according to the following requirements：
1.According to the content of the first part of the file in the "document" folder in the current directory that is read later (the last set of elements may be truncated due to the word limit, the last group of elements is ignored during analysis), determine the processing method and write a program to implement the processing requirements in the following question.
2. If multiple files need to be processed according to the problem, only the files with the corresponding file names will be processed in the written program if the file contains parentheses at the beginning and the file name is included in the parentheses. If the file does not contain a file name at the beginning, you need to do the same for all files mentioned in the question.
3. If not otherwise stated in the question, the processed file will be saved to the "modified" folder in the current directory with the same file name, and the folder will be created if the current directory does not have a "modified" folder.'''
    output=send(prompt+"The contents of the file that are read are as follows："+document_read,"The questions are as follows："+question)
    return(output)

