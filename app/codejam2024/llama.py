import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from utils import ROOT_DIR
from os import path

device = "cuda:0" if torch.cuda.is_available() else "cpu"

print(f"Using {device} for processing!")

torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "Qwen/Qwen2.5-0.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch_dtype,
    low_cpu_mem_usage=True,
    use_safetensors=True,
)

model.to(device)

info = ""

with open(path.join(ROOT_DIR, "sample_audio", "sample1.txt")) as file:
    info = file.read()

messages = [
    {
        "role": "system",
        "content": 'You are a test maker. You will be given information and your task is to create a list of \
             exactly 3 questions based on the information. You must come up with an answer for each \
             question. Structure the question and answer as key-value pairs. \
             The key for the question must be a "Q" and the key for the answer must be a "A".',
    },
    {"role": "user", "content": info},
]

text = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)
model_inputs = tokenizer([text], return_tensors="pt").to(device)

generated_ids = model.generate(**model_inputs, max_new_tokens=1024, temperature=0.05)
generated_ids = [
    output_ids[len(input_ids) :]
    for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

print(response)
