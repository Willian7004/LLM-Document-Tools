import api

def main():
    try:
        with open('book.txt', 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print("Error: 'book.txt' file not found in the current directory.")
        return
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return

    while True:
        question = input("Please enter your question (or type 'exit' to quit): ")
        if question.lower() == 'exit':
            break

        try:
            response = api.question(content, question)
            print(response)
        except Exception as e:
            print(f"An error occurred while processing the question: {e}")

main()