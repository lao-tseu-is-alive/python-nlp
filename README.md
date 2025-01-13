# python-nlp
python nlp experiments


### Install requirements and virtualenv using [pyenv](https://github.com/pyenv/pyenv)
go to the project directory and run the following commands:
```bash
sudo apt-get install hunspell libhunspell-dev hunspell-fr default-jdk
pyenv install 3.12.4
pyenv virtualenv 3.12.4 python-nlp
pyenv local python-nlp
./install_requirements.sh
```




### tools and libs used
- [spaCy](https://spacy.io/) for NLP
- [ollama](https://github.com/ollama/ollama) A Golang way to interact with LLM 
- [ollama-python](https://github.com/ollama/ollama-python)
- [Langchain](https://python.langchain.com/) 
- [LLamaIndex](https://docs.llamaindex.ai/en/stable/)