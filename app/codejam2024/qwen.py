import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from utils import ROOT_DIR, get_device
from os import path

device = get_device()


model_id = "Qwen/Qwen2.5-3B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)

TEST_MAKER_PROMPT = 'You are a test maker. You will be given information and your task is to create a list of \
             exactly 3 questions based on the information. You must come up with an answer for each \
             question. Structure the question and answer as key-value pairs. \
             The key for the question must be a "Q" and the key for the answer must be a "A".'

MULTIPLE_CHOICE_MAKER_PROMPT = "You create multiple choice tests. You will be given by the user information that you will use to \
to create the multiple choice questions. Your tasks include creating questions based on the given information, come up with \
the correct answers to questions, and come up with intentionally wrong answers to questions for added difficulty. \
You will perform the specific task at the request of the user. Only ever respond with exactly what is requested."


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
