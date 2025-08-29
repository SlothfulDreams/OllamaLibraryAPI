from typing import Union
from fastapi import FastAPI
from scrapper import Ollama

ollama = Ollama(cache_hours=12)

app = FastAPI()


@app.get("/")
def read_root():
    return "API for fetching Ollama Models!"


@app.get("/get_models")
def get_models():
    return ollama.get_models()


@app.get("/get_models_json")
def get_models_json():
    return ollama.get_models_json()


@app.get("/get_model_by_name")
def get_model_by_name(name: str):
    return ollama.get_model_by_name(name)


@app.get("/get_model_by_capability")
def get_models_by_capability(capability: str):
    return ollama.get_models_by_capability(capability)


@app.get("/get_models_size")
def get_models_by_size(size: str):
    return ollama.get_models_by_size(size)


@app.get("/cache_status")
def cache_status():
    return ollama.get_cache_status()
