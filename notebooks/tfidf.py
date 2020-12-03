
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def create_tfidf_features(df, txt_col, tokenizer=None, max_features=None, min_df=2, max_df=0.9, ngram_range=(1,1)):
    """
    Converts documents to document-term matrix using Scikit-learns TF-IDF Vectorizer
    """
    if tokenizer is not None:
        tokenizer = tokenizer.tokenize
    
    tfidf_vectorizor = TfidfVectorizer(
        decode_error='replace', 
        strip_accents='unicode', 
        tokenizer=tokenizer,
        ngram_range=ngram_range, 
        max_features=max_features,
        norm='l2',
        use_idf=True,
        smooth_idf=True,
        sublinear_tf=True,
        max_df=max_df,
        min_df=min_df
    )
    X_tfidf = tfidf_vectorizor.fit_transform(df[txt_col])
    return X_tfidf, tfidf_vectorizor

def calculate_similarity(X, vectorizor, query, top_k=None):
    """ Vectorizes the `query` via `vectorizor` and calculates the cosine similarity of
    the `query` and `X` (all the documents) and returns the `top_k` similar documents."""
    # Vectorize the query to the same length as documents
    query_vec = vectorizor.transform(query)
    # Compute the cosine similarity between query_vec and all the documents
    cosine_similarities = cosine_similarity(X,query_vec).flatten()
    # Sort the similar documents from the most similar to less similar and return the indices
    most_similar_doc_indices = np.argsort(cosine_similarities, axis=0)[:-top_k-1:-1]
    return (most_similar_doc_indices, cosine_similarities)
