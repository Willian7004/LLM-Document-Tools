import sys
import re
import os
import subprocess
import threading
import time

def read_input():
    return input("Please enter your content: ")

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
        return "The program does not work properly"

def process_document(question, api_en):
    document_read = api_en.document_read(question)
    code = extract_code(document_read)
    if code:
        write_code_to_file(code, 'document/code.py')
        output = run_code('document/code.py')
        if output == "The program does not work properly":
            print(output)
            return
        if not output:
            print("Content not read")
            return
        document_read = output
    else:
        print("Content not read")
        return

    if "--end----" in document_read:
        document_save = document_read
        segments = document_save.split("--end----")
        threads = []
        thread_count = 0

        def thread_task(segment, thread_id):
            document_read = segment
            modified_document = api_en.document_modify(document_read, question)
            code = extract_code(modified_document)
            if code:
                filename = f'document/code_{thread_id}.py'
                write_code_to_file(code, filename)
                output = run_code(filename)
                if output == "The program does not work properly":
                    print(f"Thread{thread_id}: The program is not functioning properly")
                else:
                    print(f"Thread{thread_id}: File processing complete")
            else:
                print(f"Thread{thread_id}: Content not read")

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
        modified_document = api_en.document_modify(document_read, question)
        code = extract_code(modified_document)
        if code:
            write_code_to_file(code, 'document/code.py')
            output = run_code('document/code.py')
            if output == "The program does not work properly":
                print(output)
            else:
                print("The file processing is complete")
        else:
            print("Content not read")

def main():
    if not os.path.exists('document'):
        os.makedirs('document')

    question = read_input()
    import api_en
    process_document(question, api_en)

main()