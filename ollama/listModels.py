from ollama import list
from ollama import ListResponse

response: ListResponse = list()

for model in response.models:
    print(f'Name: {model.model}')
    print(f'\tSize (MB):\t{(model.size.real / 1024 / 1024):.2f}')
    if model.details:
        print(f'\tFormat:\t{model.details.format}')
        print(f'\tFamily:\t{model.details.family}')
        print(f'\tParameter Size:\t{model.details.parameter_size}')
        print(f'\tQuantization Level:\t{model.details.quantization_level}')
    print('#######################################\n')