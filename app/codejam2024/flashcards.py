from qwen import initialize_flashcard_maker_chat, get_qwen_pipe
from utils import ROOT_DIR, read_file_into_string
from os import path


def generate_flashcards_for_info(info: str, pipe):
    chat = initialize_flashcard_maker_chat()
    chat.append(
        {"role": "user", "content": f"This is the information you will use: {info}"}
    )
    chat.append(
        {
            "role": "user",
            "content": "Create a new, unique question. Only give the question, no answer.",
        }
    )
    response = pipe(chat, max_new_tokens=100, temperature=0.2)

    question = response[0]["generated_text"][-1]["content"]

    chat = response[0]["generated_text"]

    chat.append(
        {
            "role": "user",
            "content": "Now give the correct answer to the last question.",
        }
    )

    response = pipe(chat, max_new_tokens=100, temperature=0.2)

    answer = response[0]["generated_text"][-1]["content"]
    return f"{question}; {answer}"


info = read_file_into_string(path.join(ROOT_DIR, "sample_audio", "sample1.txt"))

pipe = get_qwen_pipe()

print(
    "\n".join(
        generate_flashcards_for_info(
            info[int(len(info) * i / 3) : int(len(info) * (i + 1) / 3)], pipe
        )
        for i in range(3)
    )
)
