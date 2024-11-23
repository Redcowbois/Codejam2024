import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from utils import ROOT_DIR
from os import path

device = "cuda:0" if torch.cuda.is_available() else "cpu"

print(f"Using {device} for processing!")

torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "openai/whisper-large-v3-turbo"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id,
    torch_dtype=torch_dtype,
    low_cpu_mem_usage=True,
    use_safetensors=True,
)

model.to(device)


processor = AutoProcessor.from_pretrained(model_id)

chunk_length_s = 30

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    torch_dtype=torch_dtype,
    device=device,
    chunk_length_s=chunk_length_s,
)

generate_kwargs = {
    "language": "english",
}


def transcribe_to_file(mp3_path: str, file_path: str):
    with open(file_path, "a+") as file:
        result = pipe(
            mp3_path,
            generate_kwargs=generate_kwargs,
            return_timestamps=True,
        )
        file.write(result["text"])


transcribe_to_file(
    path.join(ROOT_DIR, "sample_audio", "sample1.mp3"),
    path.join(ROOT_DIR, "sample_audio", "sample1.txt"),
)
