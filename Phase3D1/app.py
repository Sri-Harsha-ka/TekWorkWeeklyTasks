
# This is a code for completly RNN Project based learing ( yaping a bit ig)


import os 
import re 
import pickle 
import pandas as pd 
import streamlit as st

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report , confusion_matrix

from tensorflow.keras.models import Sequential , load_model
from tensorflow.keras.layers import Embedding , SimpleRNN , Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences 


# Config 
MODEL = "spam_model.keras"
TOKENIZER = "tokenizer.pkl"

MAX_WORDS = 5000
MAX_LEN = 50

def clean_text(text):
    text = str(text).lower()
    
    text = re.sub(r"[^a-z0-9]" , " " , text)
    
    text = re.sub(r"\s+" , " ",text)
    
    return text.strip()

def train_model():
    print("Tringing Dataset ... ...")
    
    df = pd.read_csv("spam.csv" , encoding="latin-1")
    
    df = df[['v1' , 'v2']]
    
    df.columns = ['label' , 'text']

    print(df.head())
    
    print(df['label'].value_counts())

    df['label'] = df['label'].map({
        "ham":0 , 
        "spam" : 1
    })
    
    df['message'] = df['message'].apply(clean_text)
     
    tokenizer = Tokenizer(
        num_words = MAX_WORDS,
        
        oov_token = '<OOV>'
    )
    
    tokenizer.fit_on_texts(df['message'])
    
    sequences = tokenizer.texts_to_sequences(df['message'])
    
    
    X = pad_sequences(
        sequences , 
        maxlen = MAX_LEN,
        padding = 'post'
    )
    
    y = df['label']
    
    with open(TOKENIZER , "wb") as f:
        pickle.dump(tokenizer , f)
        
    x_train, x_test , y_train , y_test = train_test_split(x, y , test_size=0.2 )
    
    model = Sequential()
    
    model.add(
        Embedding(
            input_dim=MAX_WORDS , 
            output_dim= 32 , 
            input_length=MAX_LEN
        )
    )
    
    # Simple RNN layer 
    
    model.add(
        SimpleRNN(
            128
        )
    )
    
    model.add(Dense(32 , activation = 'relu'))
    model.add(Dense(1, activation='sigmoid'))
    
    model.summary()
    
    history = model.fit(x_train , y_train , validation_split = 0.2 , epochs = 10 , batch_size = 32)    
    
    model.save(MODEL)
    
    loss , accuracy = model.evaluate(x_test , y_test)
    
    y_preds = model.predict(x_test)
    
    predictions = (
        model.predict(x_test) >0.5 
    ).astype(int)
    
    print(
        classification_report(
            y_test , 
            predictions
        )
    )
    
def predict_sms(message):
    model = load_model(MODEL)
    
    with open(TOKENIZER , "rb") as f :
        tokenizer = pickle.load(f)
    message = clean_text(message)
    
    sequences = tokenizer.texts_to_sequences(
        [message]
    )
    
    sequences = pad_sequences(
        sequences,
        maxlen = MAX_LEN, 
        padding = 'post'
    )
    
    probalility = model.predict(
        sequences , 
        verbose = 0
    )[0][0]
    
    if probalility >0.5:
        return "Spam" 
    
    return "HAM"
    
if not os.path.exists(MODEL):
    train_model()
    



# Stramlit UI 

st.title("SMS Spam Detector")

st.write("Many to one RNN Example ")

message = st.text_area(
    "Enter SMS message :  "
)

if st.button("predict"):
    
    prediction , probability = predict_sms(message)
    
    st.success(prediction)
    
    st.write(
        "Confidence : ", 
        round(probability*100, 2 ),
        "%"
    )


    