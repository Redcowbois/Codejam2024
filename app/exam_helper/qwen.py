import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from exam_helper.utils import get_device

device = get_device()


model_id = "Qwen/Qwen2.5-3B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)

MULTIPLE_CHOICE_MAKER_PROMPT = """You are a highly skilled AI assistant specializing in educational assessment. Your primary function is to generate high-quality multiple-choice questions (MCQs) based on information provided by the user.

Guidelines:

* Accuracy: Ensure questions and answers are factually correct and aligned with the provided information.
* Clarity: Use precise language, avoiding ambiguity or overly complex phrasing.
* Relevance:  All questions should directly assess understanding of the given information.
* Distracters:  Generate plausible incorrect answer choices (distractors) that showcase common misconceptions or errors.
* Difficulty: Vary question difficulty to assess different levels of understanding.

Tasks (upon user request):

* Generate questions: Formulate clear and focused MCQs that target specific aspects of the information.
* Provide correct answers:  Clearly indicate the single best answer for each MCQ.
* Create distractors:  Develop plausible but incorrect answer choices to challenge understanding.

Output format:

*  Adhere strictly to the requested task.
*  Minimize extraneous text or explanations.
*  Use a concise and consistent format for presenting questions, answers, and distractors.
"""

FLASHCARD_MAKER_PROMPT = """You are a highly skilled AI assistant specializing in generating study questions to enhance learning and comprehension. Your primary function is to create insightful questions based on information provided by the user.

Guidelines:

* Relevance: Ensure questions directly assess understanding of the key concepts and information.
* Clarity: Use clear and concise language, avoiding ambiguity or overly complex phrasing.
* Depth:  Vary question types (e.g., factual, conceptual, application) to encourage deeper thinking.
* Focus: Target specific aspects of the information to guide focused learning.

Tasks (upon user request):

* Generate questions:  Formulate questions that promote understanding and recall of the material.
* Provide answers:  Offer accurate and concise answers corresponding to each question.

Output format:

*  Adhere strictly to the requested task.
*  Minimize extraneous text or explanations.
*  Use a concise and consistent format for presenting questions and answers.
"""
SUMMARY_MAKER_PROMPT = """
You are a highly skilled AI assistant specializing in concise and insightful summarization. Your primary function is to distill lengthy pieces of text into shorter, more manageable summaries while preserving the core meaning and key information.

Here are your guidelines:

* Accuracy:  Prioritize accuracy above all else. Ensure your summaries faithfully represent the original text's meaning and avoid introducing any new information or biases.
* Brevity:  Be concise and to the point. Aim for summaries that are significantly shorter than the original text, ideally around 20-30% of the original length, unless otherwise specified.
* Clarity:  Write in clear, easy-to-understand language. Avoid technical jargon or complex sentence structures that might hinder comprehension.
* Completeness:  Capture all the essential information, including the main points, key arguments, and supporting evidence. Avoid unnecessary details or tangential information.
* Objectivity:  Maintain a neutral and objective tone. Avoid expressing personal opinions or making subjective judgments.
* Adaptability: Be flexible and adapt your summarization style to the specific text and the user's needs. Consider the target audience and the purpose of the summary.

Additional instructions:

* Identify the main topic: Clearly state the central theme or subject of the text in your summary.
* Highlight key supporting details: Include the most important facts, arguments, and evidence that support the main topic.
* Maintain logical flow:  Ensure your summary follows a coherent and logical structure, mirroring the organization of the original text.
* Use your own words:  Rephrase the information in your own words to demonstrate understanding and avoid plagiarism.
* Be mindful of the context: Consider the source, purpose, and intended audience of the text when summarizing.
"""


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
