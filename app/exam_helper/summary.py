from exam_helper.qwen import initialize_summary_maker_chat


def generate_summary_for_info(info: str, pipe):
    chat = initialize_summary_maker_chat()
    chat.append({"role": "user", "content": f"Summarize the following text: {info}"})
    response = pipe(chat, max_new_tokens=100, temperature=0.3)
    return response[0]["generated_text"][-1]["content"]
