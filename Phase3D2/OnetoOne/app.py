from pathlib import Path
import os
import pickle
import re
import warnings

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
os.environ.setdefault("GLOG_minloglevel", "3")
os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")

import numpy as np
import pandas as pd
import streamlit as st

warnings.filterwarnings("ignore", message=r".*tf\.reset_default_graph.*")
warnings.filterwarnings("ignore", category=FutureWarning)

import tensorflow as tf

tf.get_logger().setLevel("ERROR")


ROOT_DIR = Path(__file__).resolve().parent
MODEL_DIR = ROOT_DIR / "model"
MODEL_PATH = MODEL_DIR / "wordmood_model.h5"
TOKENIZER_PATH = MODEL_DIR / "tokenizer.pkl"
LABEL_ENCODER_PATH = MODEL_DIR / "label_encoder.pkl"

EMOTION_EMOJIS = {
    "joy": "😊",
    "anger": "😠",
    "sadness": "😢",
    "fear": "😨",
    "neutral": "😐",
}

EMOTION_COLORS = {
    "joy": "#f6b93b",
    "anger": "#e55039",
    "sadness": "#4a69bd",
    "fear": "#7f8fa6",
    "neutral": "#60a3bc",
}


@st.cache_resource(show_spinner=False)
def load_artifacts():
    if not MODEL_PATH.exists() or not TOKENIZER_PATH.exists() or not LABEL_ENCODER_PATH.exists():
        return None

    model = tf.keras.models.load_model(MODEL_PATH, compile=False)

    with TOKENIZER_PATH.open("rb") as file_handle:
        tokenizer = pickle.load(file_handle)

    with LABEL_ENCODER_PATH.open("rb") as file_handle:
        label_encoder = pickle.load(file_handle)

    return {"model": model, "tokenizer": tokenizer, "label_encoder": label_encoder}


def clean_word(word: str) -> str:
    return word.strip().lower()


def contains_multiple_words_or_numbers(word: str) -> bool:
    return bool(re.search(r"\s|\d", word))


def encode_word(word: str, tokenizer: dict) -> np.ndarray:
    char_to_index = tokenizer["char_to_index"]
    max_length = int(tokenizer["max_length"])
    unknown_index = int(tokenizer.get("unknown_index", 1))

    sequence = [char_to_index.get(character, unknown_index) for character in word[:max_length]]
    if len(sequence) < max_length:
        sequence.extend([0] * (max_length - len(sequence)))

    return np.asarray([sequence], dtype=np.int32)


def predict_emotion(word: str, model, tokenizer: dict, label_encoder: dict):
    processed_word = clean_word(word)
    encoded_word = encode_word(processed_word, tokenizer)

    probabilities = model.predict(encoded_word, verbose=0)[0]
    predicted_index = int(np.argmax(probabilities))
    predicted_emotion = label_encoder["index_to_emotion"][str(predicted_index)]

    return predicted_emotion, probabilities


def main():
    st.set_page_config(page_title="WordMood", page_icon="💬", layout="centered")

    artifacts = load_artifacts()
    if artifacts is None:
        st.title("WordMood - One Word, One Emotion")
        st.error("Model artifacts are missing. Run `python model/train.py` from the project root first.")
        st.stop()

    model = artifacts["model"]
    tokenizer = artifacts["tokenizer"]
    label_encoder = artifacts["label_encoder"]

    emotions = [label_encoder["index_to_emotion"][str(index)] for index in range(len(label_encoder["index_to_emotion"]))]

    st.sidebar.title("How it works")
    st.sidebar.write("One word is treated as a short character sequence.")
    st.sidebar.write("The LSTM reads that sequence and predicts one emotion label.")
    st.sidebar.write("This is a One-to-One RNN: one input, one output.")

    st.title("WordMood")
    st.caption(
        "One word in, one emotion out. A small One-to-One RNN demo built for contrast with One-to-Many generators."
    )

    word_input = st.text_input("Enter a single word", placeholder="e.g. joyful")

    if st.button("Predict emotion"):
        if not word_input.strip():
            st.info("Enter a single word to get a prediction.")
            st.stop()

        if contains_multiple_words_or_numbers(word_input):
            st.warning("Please enter a single word without spaces or numbers.")
            st.stop()

        predicted_emotion, probabilities = predict_emotion(word_input, model, tokenizer, label_encoder)
        emoji = EMOTION_EMOJIS.get(predicted_emotion, "")

        st.subheader(f"{emoji} {predicted_emotion.title()}")

        probabilities_df = pd.DataFrame({"emotion": emotions, "confidence": probabilities}).set_index("emotion")
        st.bar_chart(probabilities_df)


if __name__ == "__main__":
    main()
