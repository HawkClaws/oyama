<div align="center">
 <img alt="ollama" height="200px" src="https://raw.githubusercontent.com/HawkClaws/oyama/main/icon.jpg">
</div>

# Ollama

An improved wrapper for ollama that allows for one-shot launching of local models with URL specification.
It runs on Linux and GoogleColab.
It will not work on Windows or Mac...

# How to use


## Install

`pip install git+https://github.com/HawkClaws/oyama.git ollama`

## Code
```python
from oyama import oyama
import ollama

# Hugging Face Model Path
model_name = oyama.run("https://huggingface.co/mmnga/cyberagent-calm2-7b-chat-gguf/resolve/main/cyberagent-calm2-7b-chat-q4_0.gguf?download=true")

response = ollama.chat(model=model_name, messages=[
  {
    'role': 'user',
    'content': '日本でお薦めの観光地を5つあげてください。',
  },
])
print(response['message']['content'])
```

