import os
from fastapi import Body, FastAPI, HTTPException,Request
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

nltk.download('punkt')
nltk.download('stopwords')
# Use the current directory as the base path for the file
base_path = os.path.dirname(__file__)

# Construct the path to the VERTORIZED.pkl file
vectorized_path = os.path.join(base_path, 'VERTORIZED.pkl')
vectorized = joblib.load(vectorized_path)
app = FastAPI()

stopwords_set = set(stopwords.words('english'))
stemmer = PorterStemmer()


    
@app.get("/")
def root():
    return {"message": "This is my api"}

@app.get("/api/genvec")
async def gen_vec(data:Request):
    try:
        json=await data.json()
        text_data=json["text_data"]
        # Tokenization
        words = word_tokenize(text_data)

        # Stopword removal and stemming
        filtered_words = [stemmer.stem(word) for word in words if word.lower() not in stopwords_set]
        # Convert to vector using TF-IDF
        
        vector = vectorized.transform([" ".join(filtered_words)]).toarray()
        return {"VECTOR" : vector.tolist()}
        
    except Exception as e:
        print("Error:", str(e)) 
        raise HTTPException(status_code=500, detail="Error")