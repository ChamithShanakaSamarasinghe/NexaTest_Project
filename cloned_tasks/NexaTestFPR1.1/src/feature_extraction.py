from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

def extract_ohe(texts, max_features=1000):
    vectorizer = CountVectorizer(
        stop_words="english",
        binary=True,
        max_features=max_features
    )
    return vectorizer.fit_transform(texts), vectorizer


def extract_ows(texts, max_features=1000):
    vectorizer = CountVectorizer(
        stop_words="english",
        max_features=max_features
    )
    return vectorizer.fit_transform(texts), vectorizer


def extract_ocbo(ohe_matrix):
    return (ohe_matrix.sum(axis=0) > 0).astype(int)