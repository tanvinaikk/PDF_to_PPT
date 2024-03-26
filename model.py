from sklearn.metrics.pairwise import cosine_similarity
from keras.preprocessing.sequence import pad_sequences
from sklearn.feature_extraction.text import TfidfVectorizer
import networkx as nx
from gensim.models import Word2Vec
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import re
# import pandas as pd
import numpy as np
import nltk

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')


def summary(text):
    # TOKENIZATION (Splitting the whole paragraph into sentences)
    sentences = sent_tokenize(str(text))

    # Remove punctuations, special characters and numbers
    sentences_clean = [re.sub(r'[^\w\s]', '', str(sentence).lower()) for sentence in sentences]

    # Removing stops words
    stop_words = stopwords.words('english')
    sentence_tokens = [
        [words for words in sentence.split(' ') if words not in stop_words and words.isalpha() and len(words) > 1]
        for sentence in sentences_clean
    ]
    # Remove empty strings
    sentence_tokens = [words for words in sentence_tokens if words]

    # TF-IDF Vectorization
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([' '.join(words) for words in sentence_tokens])

    # Filter out words with frequency less than min_word_frequency
    min_word_frequency=20
    flat_tokens = [word for sublist in sentence_tokens for word in sublist]
    word_frequency = nltk.FreqDist(flat_tokens)
    filtered_tokens = [
        [word for word in words if word_frequency[word] >= min_word_frequency]
        for words in sentence_tokens
    ]

    # WORD EMBEDDING (Then splitting the sentence into words using Word2Vec)
    # Train Word2Vec model
    w2v = Word2Vec(sentence_tokens, min_count=1)

    # Create sentence embeddings
    sentence_embeddings = []
    for index, words in enumerate(filtered_tokens):
        embedding = []
        for word in words:
            if word in w2v.wv.index_to_key and word in tfidf_vectorizer.vocabulary_:
                embedding.append(w2v.wv.get_vector(word) * tfidf_matrix[index, tfidf_vectorizer.vocabulary_[word]])
            else:
                print(f"Word not found in Word2Vec or TF-IDF vocabulary: {word}")
        sentence_embeddings.append(embedding)

    # Find the maximum length of embeddings
    max_len = max(len(embedding) for embedding in sentence_embeddings)

    # Pad embeddings along the second dimension
    sentence_embeddings_padded = []

    for embedding in sentence_embeddings:
        if len(embedding) > 0:
            # Reshape the embedding to (length_of_embedding, dimensionality, 1)
            embedding_reshaped = np.reshape(embedding, (len(embedding), -1, 1))
            # Pad along the second dimension
            padded_embedding = np.pad(embedding_reshaped, ((0, max_len - len(embedding)), (0, 0), (0, 0)),
                                    'constant', constant_values=0.0)
            # Remove the added dimension
            padded_embedding = np.squeeze(padded_embedding, axis=-1)
            sentence_embeddings_padded.append(padded_embedding)

        else:
            # print("Skipping padding for embedding with length:", len(embedding))
            sentence_embeddings_padded.append(embedding[:max_len])

    # Convert to NumPy array with dtype=object
    # sentence_embeddings_array = np.array(sentence_embeddings_padded, dtype=object)

    # Assuming sentence_embeddings is a list of lists representing sentence embeddings
    max_len = max(len(embedding) for embedding in sentence_embeddings)

    # Pad the inner lists
    padded_embeddings = pad_sequences(sentence_embeddings, maxlen=max_len, padding='post', dtype='float32')

    # Flatten the padded embeddings
    flattened_embeddings = [embedding.flatten() for embedding in padded_embeddings]

    # Calculate cosine similarity
    similarity_matrix = cosine_similarity(flattened_embeddings, flattened_embeddings)

    # Converting similarity matrix sim_mat into a graph
    nx_graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(nx_graph, tol=1.0e-3)

    # Calculate PageRank scores
    scores = [0] * len(sentences)
    top_sentence = {sentence: score for index, (sentence, score) in enumerate(zip(sentences, scores))}
    top = dict(sorted(top_sentence.items(), key=lambda x: x[1], reverse=True)[:40])

    final_text = ""

    for sent in sentences:
        if sent in top.keys():
            final_text += sent
    # print(final_text)

    return final_text

