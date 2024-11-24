from exam_helper.qwen import (
    initialize_multi_choice_maker_chat,
)


def generate_question_for_info(info: str, pipe):

    chat = initialize_multi_choice_maker_chat()

    chat.append(
        {"role": "user", "content": f"This is the information you will use: {info}"}
    )
    chat.append(
        {
            "role": "user",
            "content": "Create a new question. Only give the question, no answers.",
        }
    )

    response = pipe(chat, max_new_tokens=100, temperature=0.2)

    question = response[0]["generated_text"][-1]["content"]

    chat = response[0]["generated_text"]

    chat.append(
        {
            "role": "user",
            "content": "Now give the correct answer to the last question. Do not explain the answer.",
        }
    )

    response = pipe(chat, max_new_tokens=100)

    correct = response[0]["generated_text"][-1]["content"]

    incorrect_answers = []

    chat.append(
        {
            "role": "user",
            "content": "Now give an incorrect answer to the last question. Do not explain the answer.",
        }
    )

    response = pipe(chat, max_new_tokens=100)

    incorrect_answers.append(response[0]["generated_text"][-1]["content"])

    chat.append(
        {
            "role": "user",
            "content": "Now give another incorrect answer to the last question. Do not explain the answer.",
        }
    )

    response = pipe(chat, max_new_tokens=100)

    incorrect_answers.append(response[0]["generated_text"][-1]["content"])

    return {
        "question": question, #str
        "right_answer": correct, #str
        "wrong_answer": incorrect_answers, #arr
    }


def generate_n_questions_for_info(n, info, pipe):
    return [].extend(
        generate_question_for_info(
            info[int(len(info) * i / n) : int(len(info) * (i + 1) / n)], pipe
        )
        for i in range(n)
    )
