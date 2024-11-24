import torch
from os import path

ROOT_DIR = path.dirname(path.abspath(__file__))


def read_file_into_string(file_path: str) -> str:
    contents = ""
    with open(file_path) as file:
        contents = file.read()
    return contents


def get_device() -> str:
    return "cuda:0" if torch.cuda.is_available() else "cpu"
