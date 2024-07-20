import sys
import re
import os
import subprocess
import threading
import time

def read_input():
    return input("请输入内容: ")

def extract_code(text):
    pattern = r"```(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    if matches:
        return "\n".join(matches[0].splitlines()[1:])
    return None

def write_code_to_file(code, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(code)

def run_code(filename):
    try:
        result = subprocess.run(['python', filename], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        return "程序无法正常运行"

def process_document(question, api):
    document_read = api.document_read(question)
    code = extract_code(document_read)
    if code:
        write_code_to_file(code, 'document/code.py')
        output = run_code('document/code.py')
        if output == "程序无法正常运行":
            print(output)
            return
        if not output:
            print("未读取到内容")
            return
        document_read = output
    else:
        print("未读取到内容")
        return

    if "--end----" in document_read:
        document_save = document_read
        segments = document_save.split("--end----")
        threads = []
        thread_count = 0

        def thread_task(segment, thread_id):
            document_read = segment
            modified_document = api.document_modify(document_read, question)
            code = extract_code(modified_document)
            if code:
                filename = f'document/code_{thread_id}.py'
                write_code_to_file(code, filename)
                output = run_code(filename)
                if output == "程序无法正常运行":
                    print(f"线程{thread_id}: 程序无法正常运行")
                else:
                    print(f"线程{thread_id}: 文件处理完成")
            else:
                print(f"线程{thread_id}: 未读取到内容")

        for segment in segments:
            if thread_count >= 64:
                for t in threads:
                    t.join()
                threads = []
                thread_count = 0
            thread = threading.Thread(target=thread_task, args=(segment, thread_count))
            threads.append(thread)
            thread.start()
            thread_count += 1
            time.sleep(0.05)

        for t in threads:
            t.join()
    else:
        modified_document = api.document_modify(document_read, question)
        code = extract_code(modified_document)
        if code:
            write_code_to_file(code, 'document/code.py')
            output = run_code('document/code.py')
            if output == "程序无法正常运行":
                print(output)
            else:
                print("文件处理完成")
        else:
            print("未读取到内容")

def main():
    if not os.path.exists('document'):
        os.makedirs('document')

    question = read_input()
    import api
    process_document(question, api)

main()