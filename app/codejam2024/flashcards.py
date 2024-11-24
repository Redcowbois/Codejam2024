from qwen import initialize_flashcard_maker_chat


def generate_flashcards_for_info(info: str, pipe):
    chat = initialize_flashcard_maker_chat()
    chat.append(
        {"role": "user", "content": f"This is the information you will use: {info}"}
    )
    cards_contents = []
    for _ in range(5):
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

        cards_contents.append(f"{question}; {answer}")
    return "\n".join(cards_contents)
