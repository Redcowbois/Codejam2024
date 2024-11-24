import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from utils import get_device

device = get_device()


model_id = "Qwen/Qwen2.5-3B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)

MULTIPLE_CHOICE_MAKER_PROMPT = "You create multiple choice tests. You will be given information by the user that you will use to \
to create the multiple choice questions. Your tasks include creating questions based on the given information, come up with \
the correct answers to questions, and come up with intentionally wrong answers to questions for added difficulty. \
You will perform the specific task at the request of the user. Do not add any text to your response that is not absolutely \
necessary to the question or answer you are creating."

FLASHCARD_MAKER_PROMPT = "You create questions that are useful for studying. You will be given information by the user that you will use to \
to create questions. Your tasks include creating questions based on the given information, and come up with the correct answers to questions. \
You will perform the specific task at the request of the user. Do not add any text to your response that is not absolutely \
necessary to the question or answer you are creating."

PODCAST_MAKER_PROMPT = "You act out conversations between two people. You will be given information by the user that you will use as \
the primary topic for a conversation "


def get_qwen_pipe():

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype="auto",
        low_cpu_mem_usage=True,
        use_safetensors=True,
    )

    model.to(device)
    return pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        torch_dtype="auto",
        device=device,
    )


def initialize_multi_choice_maker_chat():
    return [
        {
            "role": "system",
            "content": MULTIPLE_CHOICE_MAKER_PROMPT,
        },
    ]


def initialize_flashcard_maker_chat():
    return [
        {
            "role": "system",
            "content": FLASHCARD_MAKER_PROMPT,
        },
    ]


def format_chat_for_model_input(model_chat):

    text = tokenizer.apply_chat_template(
        model_chat, tokenize=False, add_generation_prompt=True
    )
    return tokenizer([text], return_tensors="pt").to(device)


def generate_responses(model, inputs, max_tokens, temperature):
    generated_ids = model.generate(
        **inputs, max_new_tokens=max_tokens, temperature=temperature
    )
    generated_ids = [
        output_ids[len(input_ids) :]
        for input_ids, output_ids in zip(inputs.input_ids, generated_ids)
    ]

    return tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
