import numpy as np
from tqdm.auto import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer

class BM25:
    def __init__(self, b=0.75, k1=1.6):
        self.vectorizer = TfidfVectorizer(norm=None, smooth_idf=False, dtype=np.float32)
        self.b = b
        self.k1 = k1

    def fit(self, docs):
        self.vect_docs = self.vectorizer.fit_transform(docs).tocsc()
        self.avdl = self.vect_docs.sum(1).mean()
        self.len_X = self.vect_docs.sum(1).A1

    def get_relevance(self, queries):
        queries = self.vectorizer.transform(queries).tocsc()

        results = np.empty((queries.shape[0], self.vect_docs.shape[0]), dtype=np.float32)
        shared_denom = (self.k1 * (1 - self.b + self.b * self.len_X / self.avdl))[:, None]

        for idx, query in enumerate(tqdm(queries, total=queries.shape[0], desc="BM25")):
            X = self.vect_docs[:, query.indices]
            idf = self.vectorizer._tfidf.idf_[None, query.indices] - 1.
            denom = X + shared_denom
            numer = X.multiply(np.broadcast_to(idf, X.shape)) * (self.k1 + 1)                                                          
            results[idx] = (numer / denom).sum(1).A1
        
        
        return results