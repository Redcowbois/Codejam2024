from transformers import AutoModelForCausalLM, AutoTokenizer

device = "cpu"
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2-7B-Instruct", low_cpu_mem_usage = True)
from accelerate import disk_offload
disk_offload(model = model, offload_dir="offload")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-7B-Instruct")

prompt = "Give me a short introduction to large language model."

messages = [{"role": "user", "content": prompt}]

text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

model_inputs = tokenizer([text], return_tensors="pt").to(device)

generated_ids = model.generate(model_inputs.input_ids, max_new_tokens=512, do_sample=True)

generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

print(response)