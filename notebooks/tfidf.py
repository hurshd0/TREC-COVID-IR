
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def create_tfidf_features(df, txt_col, tokenizer=None, max_features=None, min_df=2, max_df=0.9, ngram_range=(1,1)):
    """
    Converts documents to document-term matrix using Scikit-learns TF-IDF Vectorizer
    """
    if tokenizer is not None:
        tokenizer = tokenizer.tokenize
    
    tfidf_vectorizer = TfidfVectorizer(
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
    X_tfidf = tfidf_vectorizer.fit_transform(df[txt_col])
    return X_tfidf, tfidf_vectorizer

def calculate_similarity(X_tfidf, tfidf_vectorizer, query, top_k=5):
    """ Vectorizes the `query` via `tfidf_vectorizer` and calculates the cosine similarity of
    the `query` and `X_tfidf` (all the documents) and returns the `top_k` similar documents."""
    # Vectorize the query to the same length as documents
    if not isinstance(query, list):
        query = [query]
    query_vec = tfidf_vectorizer.transform(query)
    # Compute the cosine similarity between query_vec and all the documents
    scores = cosine_similarity(X_tfidf,query_vec).flatten()
    indices = np.argsort(scores)[-top_k:][::-1]
    scores = scores[indices]
    return list(zip(indices, scores))

def get_ranked_lists(query, qid, run_name, corpus_df, X_tfidf, tfidf_vectorizer, top_k):
    template = "{} Q0 {} {} {:.6f} tfidf_baseline_{}\n"
    similar_docs = calculate_similarity(X_tfidf, tfidf_vectorizer, query, top_k)
    return [template.format(qid, corpus_df.iloc[idx]['cord_uid'], rank+1, score, run_name) for rank, (idx, score) in enumerate(similar_docs)]

def write_results(out_fpath, corpus_df, query_df, query_id_col, query_txt_col, X_tfidf, tfidf_vectorizer, run_name, top_k=1000):
    with open(out_fpath, 'w', encoding='utf-8') as writer:
        for idx, topic in query_df.iterrows():
            qid = topic[query_id_col]
            query = topic[query_txt_col]
            ranked_lists = get_ranked_lists(query, qid, run_name, corpus_df, X_tfidf, tfidf_vectorizer, top_k=top_k)
            writer.writelines(ranked_lists)
    print(f"Wrote file @ {out_fpath}\n")
