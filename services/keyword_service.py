from sklearn.feature_extraction.text import TfidfVectorizer


class KeywordService:
    def extract(self, feedback_list, top_n=10):
        vectorizer = TfidfVectorizer(
            stop_words="english"
        )
        
        # learn vocabulary and transform to vectors
        matrix = vectorizer.fit_transform(feedback_list)

        scores = matrix.sum(axis=0)
        words = vectorizer.get_feature_names_out()
        
        keyword_scores = []

        # get the score of each word
        for idx, word in enumerate(words):
            keyword_scores.append(
                (
                    word,
                    round(scores[0, idx], 3)
                )
            )

        # sort the scores in descending order
        keyword_scores.sort(
            key=lambda item: item[1],
            reverse=True
        )

        return keyword_scores[:top_n]