from typing import Union
from fastapi import FastAPI
from scrapper import Ollama

ollama = Ollama()

app = FastAPI()
