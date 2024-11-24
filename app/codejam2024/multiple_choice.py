from utils import read_file_into_string, ROOT_DIR
from os import path
from qwen import (
    get_qwen_pipe,
    initialize_multi_choice_maker_chat,
)

info = read_file_into_string(path.join(ROOT_DIR, "sample_audio", "sample1.txt"))

pipe = get_qwen_pipe()

chat = initialize_multi_choice_maker_chat()

chat.append(
    {"role": "user", "content": f"This is the information you will use: {info}"}
)
chat.append({"role": "user", "content": "Create a new question. Only give the question, no answers."})

response = pipe(chat, max_new_tokens=100, temperature=0.2)

print(response[0]["generated_text"][-1]["content"])

chat = response[0]["generated_text"]

chat.append(
    {
        "role": "user",
        "content": "Now give the correct answer to the last question. Do not explain the answer.",
    }
)

response = pipe(chat, max_new_tokens=100)

print(response[0]["generated_text"][-1]["content"])

chat.append({
        "role": "user",
        "content": "Now give an incorrect answer to the last question. Do not explain the answer.",
    })

response = pipe(chat, max_new_tokens=100)

print(response[0]["generated_text"][-1]["content"])


chat.append({
        "role": "user",
        "content": "Now give another incorrect answer to the last question. Do not explain the answer.",
    })


response = pipe(chat, max_new_tokens=100)

print(response[0]["generated_text"][-1]["content"])

chat.append({"role": "user", "content": "Create a new question. Only give the question, no answers."})

response = pipe(chat, max_new_tokens=100)

print(response[0]["generated_text"][-1]["content"])
chat = response[0]["generated_text"]

chat.append(
    {
        "role": "user",
        "content": "Now give the correct answer to the last question. Do not explain the answer.",
    }
)

response = pipe(chat, max_new_tokens=100)

print(response[0]["generated_text"][-1]["content"])

chat.append({
        "role": "user",
        "content": "Now give an incorrect answer to the last question. Do not explain the answer.",
    })

response = pipe(chat, max_new_tokens=100)

print(response[0]["generated_text"][-1]["content"])


chat.append({
        "role": "user",
        "content": "Now give another incorrect answer to the last question. Do not explain the answer.",
    })


response = pipe(chat, max_new_tokens=100)

print(response[0]["generated_text"][-1]["content"])