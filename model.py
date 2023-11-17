import numpy as np
import pandas as pd
import nltk
import re
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from gensim.models import Word2Vec
from scipy import spatial
import networkx as nx
from gensim.models import Word2Vec
import numpy as np

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')


def summary(text):

    # TOKENIZATION (Spliting the whole paragraph into sentence)
    sentences = sent_tokenize(text)

    # Remove punctuations, special characters and numbers
    sentences_clean = [re.sub(r'[^\w\s]', '', sentence.lower())
                       for sentence in sentences]
    print(sentences_clean)

    # Removing stops words
    stop_words = stopwords.words('english')
    sentence_tokens = [[words for words in sentence.split(
        ' ') if words not in stop_words] for sentence in sentences_clean]
    sentences_clean[0:5]


    # WORD EMBEDDING (Then spliting the sentence into words using gLoVe)
    # Train Word2Vec model
    w2v = Word2Vec(sentence_tokens, min_count=1)

    # Create sentence embeddings
    sentence_embeddings = [
        # Check if the word is in the vocabulary
        [w2v.wv[word] for word in words if word in w2v.wv]
        for words in sentence_tokens
    ]

    # Find the maximum length of embeddings
    max_len = max(len(embedding) for embedding in sentence_embeddings)

    # Pad embeddings along the second dimension
    sentence_embeddings_padded = [
        np.pad(embedding, ((0, max_len - len(embedding)), (0, 0)),
               'constant', constant_values=0.0)
        for embedding in sentence_embeddings
    ]

    # Convert to NumPy array
    sentence_embeddings_array = np.array(sentence_embeddings_padded)

    # Assuming sentence_embeddings is a list of lists representing sentence embeddings
    max_len = max(len(embedding) for embedding in sentence_embeddings)

    # Pad the inner lists
    padded_embeddings = pad_sequences(
        sentence_embeddings, maxlen=max_len, padding='post', dtype='float32')

    # Flatten the padded embeddings
    flattened_embeddings = [embedding.flatten()
                            for embedding in padded_embeddings]

    # Calculate cosine similarity
    similarity_matrix = cosine_similarity(
        flattened_embeddings, flattened_embeddings)


    # Converting similarity matrix sim_mat into a graph
    nx_graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(nx_graph, tol=1.0e-3)

    # Summarization
    top_sentence = {sentence: scores[index]
                    for index, sentence in enumerate(sentences)}
    top = dict(sorted(top_sentence.items(),
               key=lambda x: x[1], reverse=True)[:4])

    return top
