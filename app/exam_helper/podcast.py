from exam_helper.qwen import initialize_podcast_maker_chat

def generate_podcast_string_for_info(info: str, pipe):
    chat = initialize_podcast_maker_chat()
    chat.append({"role": "user", "content": f"""
Podcast Topic: {info}

Based on the topic above, create a podcast conversation between two people. 

Co-Host Differentiation:

* Host: Always starts the conversation and introduces the topic. Identified by "Host:" at the beginning of their dialogue.
* Co-Host: Provides additional commentary, asks questions, and plays off the Host's points. Identified by "Co-Host:" at the beginning of their dialogue.

Conversation Style:

* Casual and Engaging: Use natural language, contractions, and conversational fillers (like "um," "you know," etc.) to simulate a real conversation.
* Informative: Ensure the discussion accurately reflects the information provided in the topic, offering insights and explanations where appropriate.
* Dynamic: The conversation should flow naturally, with the Host and Co-Host building on each other's points and exploring different angles of the topic.

Output Format:

Each speaker's lines should begin with their identifier ("Host:" or "Co-Host:") to allow for easy parsing and analysis. Maintain clear distinctions between the speakers throughout the conversation.
"""})
    response = pipe(chat, max_new_tokens=100, temperature=0.4)
    return response[0]["generated_text"][-1]["content"]