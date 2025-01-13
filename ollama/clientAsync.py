from ollama import Client
from ollama import ps, pull, chat
from ollama import ProcessResponse

modelName="mistral-nemo"
# Ensure at least one model is loaded
response = pull(modelName, stream=True)
progress_states = set()
for progress in response:
  if progress.get('status') in progress_states:
    continue
  progress_states.add(progress.get('status'))
  print(progress.get('status'))

print('\n')

print('Waiting for model to load... \n')
chat(model=modelName, messages=[{'role': 'user', 'content': 'Why is the sky blue?'}])


response: ProcessResponse = ps()
for model in response.models:
  print('Model: ', model.model)
  print('  Digest: ', model.digest)
  print('  Expires at: ', model.expires_at)
  print('  Size: ', model.size)
  print('  Size vram: ', model.size_vram)
  print('  Details: ', model.details)
  print('\n')

# Chat with the model
client = Client(
    host='http://localhost:11434',
    headers={'x-some-header': 'some-value'}
)
response = client.chat(model=modelName, messages=[
    {
        'role': 'user',
        'content': 'Why is the sky blue?',
    },
])
print(response.message.content)