<div align="center">
 <img alt="oyama" height="200px" src="https://raw.githubusercontent.com/HawkClaws/oyama/main/icon.jpg">
</div>

# Oyama

An improved wrapper for ollama that allows for one-shot launching of local models with URL specification.  
It runs on Linux and GoogleColab.  
It will not work on Windows or Mac...  

<a href="https://colab.research.google.com/github/HawkClaws/oyama/blob/main/oyama.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# How to use

## Install

`pip install git+https://github.com/HawkClaws/oyama.git ollama`

## Code

```python
from oyama import oyama
import ollama

# Hugging Face Model Path
model_name = oyama.run("https://huggingface.co/mmnga/cyberagent-calm2-7b-chat-gguf/resolve/main/cyberagent-calm2-7b-chat-q8_0.gguf?download=true")

response = ollama.chat(model=model_name, messages=[
  {
    'role': 'user',
    'content': '日本でお薦めの観光地を5つあげてください。',
  },
])
print(response['message']['content'])
```

## Other examples

```python
## ollama model name
model_name = oyama.run("llama3")
```

## Get model link
<div align="center">
 <img alt="get_mopdel_link" src="https://raw.githubusercontent.com/HawkClaws/oyama/main/get_model_link.jpg">
</div>