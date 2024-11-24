import torch
from transformers import (
    AutoModelForSpeechSeq2Seq,
    AutoProcessor,
    pipeline,
)
from app.exam_helper.utils import get_device

model_id = "openai/whisper-large-v3-turbo"
processor = AutoProcessor.from_pretrained(model_id)


def get_whisper_pipe():
    device = get_device()

    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id,
        torch_dtype=torch_dtype,
        low_cpu_mem_usage=True,
        use_safetensors=True,
    )

    model.to(device)

    chunk_length_s = 30

    return pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        torch_dtype=torch_dtype,
        device=device,
        chunk_length_s=chunk_length_s,
    )


def transcribe_to_file(mp3_path: str, file_path: str, whisper_pipe):
    with open(file_path, "a+") as file:
        result = whisper_pipe(
            mp3_path,
            generate_kwargs={
                "language": "english",
            },
            return_timestamps=True,
        )
        file.write(result["text"])
