import spacy
from nltk.data import find


def is_nltk_data_downloaded(resource):
    try:
        find(f"tokenizers/{resource}")
        print(f"{resource} is already downloaded.")
        return True
    except LookupError:
        print(f"{resource} not found. Downloading now...")
        return False


def is_spacy_model_downloaded(model_name):
    try:
        spacy.load(model_name)
        print(f"{model_name} is already downloaded.")
        return True
    except OSError:
        print(f"{model_name} not found. Downloading now...")
        return False
