import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

device = "cuda:0" if torch.cuda.is_available() else "cpu"

print(f"Using {device} for processing!")

torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

attn_implementation = "flash_attention_2" if torch.cuda.is_available() else "sdpa"

model_id = "openai/whisper-large-v3-turbo"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id,
    torch_dtype=torch_dtype,
    low_cpu_mem_usage=True,
    use_safetensors=True,
    attn_implementation=attn_implementation,
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
