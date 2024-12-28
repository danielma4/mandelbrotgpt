from llama_cpp import Llama
from .models import Mathematician
from huggingface_hub import InferenceClient
from decouple import config
import random, requests, os
from huggingface_hub import InferenceClient
'''
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-hf"
headers = {"Authorization": "Bearer" + config('API_KEY')}

output = query({
	"inputs": "Can you please let us know more details about your ",
})
'''

client = InferenceClient(api_key=os.environ.get("API_KEY", config("API_KEY")))

#path = "/home/danielma/MathEQGPT/llama-2-7b.Q4_K_M.gguf"
#llama = Llama(model_path=path, n_threads=24)

def get_llama_response(prompt):
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.2-3B-Instruct", 
        messages=messages, 
        max_tokens=500,
        temperature=.3,
        top_p=.6
    )

    print(completion.choices[0].message.content)
    return completion.choices[0].message.content


def random_mathematician_ask_llama():
    mathematician = random.choice(Mathematician.objects.all())
    prompt = (f"Your name is MandelbrotGPT, and you are a math-based large language model. Tell me briefly about {mathematician.name}, who worked in {mathematician.fields}." 
    + "Make sure you split the answer into three sections: history, contributions, and fun facts. Please keep the answer under 500 tokens."
    + f"Please also do not preface the response with 'I couldnt find any information on {mathematician.name}...', rather, if this happens, simply start with a brief description of the mathematician")
    llama_response = get_llama_response(prompt)
    return mathematician.name, llama_response