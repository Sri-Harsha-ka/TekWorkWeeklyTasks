# WordMood

WordMood is a small learning project that demonstrates a One-to-One RNN: one word goes in, one emotion label comes out. It is designed as a companion to a One-to-Many RNN project called MoodTale so the architecture difference is easy to compare.

## Architecture

The model reads each word as a character sequence rather than as a single token lookup. A character embedding layer converts the sequence into vectors, an LSTM processes the sequence, and a Dense softmax layer predicts one of five emotions: joy, anger, sadness, fear, or neutral.

This is One-to-One at the word level because one input sequence produces one output label. It does not generate a new sequence over time.

## Project Structure

```text
WordMood/
├── data/
│   └── word_emotion_dataset.csv
├── model/
│   ├── train.py
│   └── wordmood_model.h5
├── app.py
├── requirements.txt
└── README.md
```

## Setup

Install the dependencies:

```bash
pip install -r requirements.txt
```

Train the model and save the artifacts:

```bash
python model/train.py
```

Launch the Streamlit app:

```bash
streamlit run app.py
```

## Notes

- The dataset in `data/word_emotion_dataset.csv` is custom-made for this demo and is roughly balanced across the five classes.
- The app loads the saved model, tokenizer, and label encoder so new input is preprocessed the same way as training data.
- This project is part of an RNN architecture demonstration series alongside the One-to-Many project MoodTale.