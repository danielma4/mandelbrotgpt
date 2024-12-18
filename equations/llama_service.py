from llama_cpp import Llama

path = "/home/danielma/MathEQGPT/llama-2-7b.Q4_K_M.gguf"
llama = Llama(model_path=path, n_threads=24)

def get_llama_response(prompt):
    response = llama(prompt, max_tokens=300, temperature=.3, top_p=.6) #probabilistic sampling
    print(prompt + "\n")
    print(response)
    return response['choices'][0]['text']