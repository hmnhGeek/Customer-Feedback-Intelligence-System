from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np


class TopicService:
    def discover_topics(self, feedback_list, num_topics=3):
        vectorizer = TfidfVectorizer(stop_words="english")

        feature_matrix = vectorizer.fit_transform(feedback_list)

        model = KMeans(
            n_clusters=num_topics,
            random_state=42,
            n_init=10
        )

        labels = model.fit_predict(feature_matrix)

        # ---------------------------
        # Convert clusters → names
        # ---------------------------
        terms = vectorizer.get_feature_names_out()
        cluster_names = {}

        for cluster_id in range(num_topics):

            # Get all rows in this cluster
            cluster_indices = np.where(labels == cluster_id)[0]

            # Average TF-IDF score per word in cluster
            cluster_center = feature_matrix[cluster_indices].mean(axis=0)

            # Flatten and get top words
            top_indices = np.argsort(cluster_center.A1)[-3:][::-1]

            top_words = [terms[i] for i in top_indices]

            # Create human-readable name
            cluster_names[cluster_id] = " / ".join(top_words).title()

        # Replace numeric labels with names
        topic_names = [
            cluster_names[label] for label in labels
        ]

        return topic_names