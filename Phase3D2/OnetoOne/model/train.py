from pathlib import Path
import os
import pickle
import warnings

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
os.environ.setdefault("GLOG_minloglevel", "3")
os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", message=r".*tf\.reset_default_graph.*")
warnings.filterwarnings("ignore", category=FutureWarning)

import tensorflow as tf

tf.get_logger().setLevel("ERROR")
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT_DIR / "data" / "word_emotion_dataset.csv"
MODEL_DIR = ROOT_DIR / "model"
MODEL_PATH = MODEL_DIR / "wordmood_model.h5"
TOKENIZER_PATH = MODEL_DIR / "tokenizer.pkl"
LABEL_ENCODER_PATH = MODEL_DIR / "label_encoder.pkl"


def load_dataset():
    frame = pd.read_csv(DATA_PATH)
    frame["word"] = frame["word"].astype(str).str.strip().str.lower()
    frame["emotion"] = frame["emotion"].astype(str).str.strip().str.lower()
    return frame


def build_tokenizer(words):
    unique_characters = sorted({character for word in words for character in word})
    char_to_index = {character: index + 2 for index, character in enumerate(unique_characters)}
    index_to_char = {index: character for character, index in char_to_index.items()}
    return {
        "char_to_index": char_to_index,
        "index_to_char": index_to_char,
        "pad_index": 0,
        "unknown_index": 1,
    }


def encode_words(words, tokenizer, max_length):
    char_to_index = tokenizer["char_to_index"]
    unknown_index = tokenizer["unknown_index"]
    sequences = []

    for word in words:
        encoded = [char_to_index.get(character, unknown_index) for character in word[:max_length]]
        sequences.append(encoded)

    return pad_sequences(sequences, maxlen=max_length, padding="post", truncating="post", value=tokenizer["pad_index"])


def build_model(vocab_size, max_length, emotion_count):
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=16, mask_zero=True),
            tf.keras.layers.LSTM(48),
            tf.keras.layers.Dense(emotion_count, activation="softmax"),
        ]
    )
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    return model


def main():
    tf.random.set_seed(42)
    np.random.seed(42)

    dataset = load_dataset()
    emotions = sorted(dataset["emotion"].unique())
    emotion_to_index = {emotion: index for index, emotion in enumerate(emotions)}
    index_to_emotion = {str(index): emotion for emotion, index in emotion_to_index.items()}

    tokenizer = build_tokenizer(dataset["word"].tolist())
    max_length = max(dataset["word"].str.len()) + 2

    x = encode_words(dataset["word"].tolist(), tokenizer, max_length)
    y = dataset["emotion"].map(emotion_to_index).to_numpy(dtype=np.int32)
    y_one_hot = to_categorical(y, num_classes=len(emotions))

    x_train, x_test, y_train, y_test, y_train_indices, y_test_indices = train_test_split(
        x,
        y_one_hot,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    vocab_size = len(tokenizer["char_to_index"]) + 2
    model = build_model(vocab_size, max_length, len(emotions))

    callbacks = [EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)]
    model.fit(
        x_train,
        y_train,
        validation_data=(x_test, y_test),
        epochs=80,
        batch_size=16,
        callbacks=callbacks,
        verbose=1,
    )

    train_loss, train_accuracy = model.evaluate(x_train, y_train, verbose=0)
    test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)

    predictions = model.predict(x_test, verbose=0)
    predicted_indices = np.argmax(predictions, axis=1)
    true_indices = np.argmax(y_test, axis=1)

    print(f"Train accuracy: {train_accuracy:.4f}")
    print(f"Test accuracy: {test_accuracy:.4f}")
    print("Classification report:")
    print(classification_report(true_indices, predicted_indices, target_names=emotions, zero_division=0))

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    model.save(MODEL_PATH)

    tokenizer_payload = {
        "char_to_index": tokenizer["char_to_index"],
        "index_to_char": tokenizer["index_to_char"],
        "pad_index": tokenizer["pad_index"],
        "unknown_index": tokenizer["unknown_index"],
        "max_length": int(max_length),
    }
    with TOKENIZER_PATH.open("wb") as file_handle:
        pickle.dump(tokenizer_payload, file_handle)

    label_encoder_payload = {
        "emotion_to_index": emotion_to_index,
        "index_to_emotion": index_to_emotion,
    }
    with LABEL_ENCODER_PATH.open("wb") as file_handle:
        pickle.dump(label_encoder_payload, file_handle)

    print(f"Saved model to {MODEL_PATH}")
    print(f"Saved tokenizer to {TOKENIZER_PATH}")
    print(f"Saved label encoder to {LABEL_ENCODER_PATH}")


if __name__ == "__main__":
    main()