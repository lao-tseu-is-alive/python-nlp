import sys

import ollama
from ollama import chat
from ollama import ChatResponse





if __name__ == '__main__':
    cmd = sys.argv[0]
    GoDEBUG = False
    UserQuestion="How to make the world a better place ?"
    print(f"Welcome to {cmd}")
    print("list of LLM models:", ollama.list())
    # check
    modelName="mistral-nemo"
    if len(sys.argv) > 1:
        if sys.argv[1] == "-d":
            GoDEBUG = True
        if sys.argv[1] == "-h":
            print(f"Usage: python {cmd} [-d] [-h] \"{UserQuestion}\" ")
            sys.exit(0)
        if len(sys.argv) > 2:
            UserQuestion=sys.argv[len(sys.argv)-1]
        else:
            UserQuestion = sys.argv[1]

    print(f"User Question: {UserQuestion}")

    response: ChatResponse = chat(model=modelName, messages=[
        {"role": "user", "content": UserQuestion}
    ])
    print(f"Response: \n{response.message.content}\n")

