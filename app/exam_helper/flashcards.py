from exam_helper.qwen import initialize_flashcard_maker_chat


def generate_flashcard_for_info(info: str, pipe):
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
    return f"{question}; {answer}".replace("\n", " ")


def generate_n_flashcards_for_info(n, info, pipe):
    return "\n".join(
        generate_flashcard_for_info(
            info[int(len(info) * i / n) : int(len(info) * (i + 1) / n)], pipe
        )
        for i in range(n)
    )
