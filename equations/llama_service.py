from llama_cpp import Llama
from .models import Mathematician
import random

path = "/home/danielma/MathEQGPT/llama-2-7b.Q4_K_M.gguf"
llama = Llama(model_path=path, n_threads=24)

def get_llama_response(prompt):
    response = llama(prompt, max_tokens=300, temperature=.3, top_p=.6) #probabilistic sampling
    print(prompt + "\n")
    print(response)
    return response['choices'][0]['text']

def random_mathematician_ask_llama():
    mathematician = random.choice(Mathematician.objects.all())
    prompt = f"Tell me briefly about {mathematician.name}, who worked in {mathematician.fields}. Mention topics such as {mathematician.name}'s history, contributions, fun facts, etc."
    llama_response = get_llama_response(prompt)
    return mathematician.name, llama_response