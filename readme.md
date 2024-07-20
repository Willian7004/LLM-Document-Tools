 本项目用于调用LLM对文档进行读取、修改和提问。
“api.py”中通过api调用一个逻辑能力优秀的LLM和一个在本地通过Ollama运行的对长上下文支持较好的LLM。在使用前应当在相应位置填写自己用的符合需求的LLM的api地址和api key。
把需要提问文档内容的文件保存到当前目录的book.txt后，运行“提问内容.py”可以进行提问，应当确保book.txt字符数不超过LLM的上下文长度限制。为了避免多轮对话影响回答稳定性，程序中不使用多轮对话。
“修改文件.py”实现了通过程序对文件排版进行修改的功能。在当前目录创建“document”文件夹并把需要修改的文件放到这个文件夹，运行程序并输入修改要求，LLM将编程并运行程序实现对文件的修改，修改后的文件保存到“modified”文件夹。
本项目使用LLM辅助制作，提示词在与相应程序同名的txt文件。“api.py”则包含运行程序时调用LLM输出的提示词。
本项目提供中文和英文版本，分别使用对应语言的作为文件名，但“api.py”用于中文版本，“api_en.py”用于英文版本。

 This project is used to invoke LLMs to read, modify, and ask questions about documents.
In "api.py", an LLM with excellent logical ability is invoked through the API and an LLM with good support for long contexts is run locally through Ollama. Before use, you should fill in the API address and API key of the LLM that meets your needs.
After saving the file to the book.txt of the current directory, run the asking_about_content.py to ask the question, and make sure that the number of characters in the book.txt does not exceed the context length limit of the LLM. In order to avoid multiple rounds of dialogue affecting the stability of the answer, multiple rounds of dialogue are not used in the program.
"modify_document.py" implements the function of modifying the layout of documents through the program. Create a "document" folder in the current directory and put the files that need to be modified into this folder, run the program and enter the modification requirements, the LLM will program and run the program to modify the file, and save the modified file to the "modified" folder.
This project is made with LLM assistance, and the prompt words are in a txt file with the same name as the corresponding program. "api.py" contains a prompt that invokes the LLM output when the program is run.
The project is available in Chinese and English, with the corresponding language as the file name, but "api.py" for the Chinese version and "api_en.py" for the English version.


