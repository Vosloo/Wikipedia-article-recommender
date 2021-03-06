import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import config as cfg


class Recommender:
    def get_recommendations(
        self, database: pd.DataFrame, query: pd.DataFrame, no_recommendations: int,
    ) -> pd.DataFrame:
        """
        Recommends articles from the DB based on the cosine similarity of the query articles
        """

        vectorizer = TfidfVectorizer().fit(database[cfg.PD_TEXT])

        db_tfidf = TfidfVectorizer().fit_transform(database[cfg.PD_TEXT])
        query_tfidf = vectorizer.transform([" ".join(query[cfg.PD_TEXT])])

        cosine_similarities = cosine_similarity(query_tfidf, db_tfidf).flatten()
        bst_idx: np.ndarray = cosine_similarities.argsort()[-no_recommendations:][::-1]

        recommendations: pd.DataFrame = database.iloc[bst_idx]
        recommendations.insert(
            recommendations.shape[1], cfg.PD_SIMILARITY, cosine_similarities[bst_idx]
        )
        recommendations.reset_index(drop=True, inplace=True)

        if cfg.SAVE_RECOMMENDATIONS:
            self._save_recommendations(recommendations)

        return recommendations

    def _save_recommendations(self, recommendations):
        # For redability purposes dropping text column
        recommended = recommendations.drop(cfg.PD_TEXT, axis=1)
        recommended.to_csv(str(cfg.WIKI_RECOMMENDATIONS_CSV_PATH), sep="\t")
        print(
            f"Saving wikipedia articles recommendations to {cfg.WIKI_RECOMMENDATIONS_CSV_PATH}"
        )
