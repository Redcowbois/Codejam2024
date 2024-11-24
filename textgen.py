import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

device = "cuda:0" if torch.cuda.is_available() else "cpu"

print(f"Using {device} for processing!")

torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "HuggingFaceTB/SmolLM2-1.7B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch_dtype,
    low_cpu_mem_usage=True,
    use_safetensors=True,
)

model.to(device)

messages = [
    {
        "role": "system",
        "content": "You are a test maker. You will be given information and your task is to create a list of \
             3 questions based on the information with an answer for each.",
    },
    {
        "role": "user",
        "content": "Kangaroos are marsupials from the family Macropodidae. In common use the term is used \
        to describe the largest species from this family, the red kangaroo, as well as the antilopine kangaroo, \
        eastern grey kangaroo, and western grey kangaroo. Kangaroos are indigenous to Australia and New Guinea.",
    },
]

input_text = tokenizer.apply_chat_template(messages, tokenize=False)
inputs = tokenizer.encode(input_text, return_tensors="pt").to(device)
outputs = model.generate(
    inputs, max_new_tokens=50, temperature=0.2, top_p=0.9, do_sample=True
)
print(tokenizer.decode(outputs[0]))