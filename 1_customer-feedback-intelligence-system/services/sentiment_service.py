# library from Hugging Face that provides access to pretrained NLP models.
from transformers import pipeline


class SentimentService:
    """
    Service responsible for performing sentiment analysis on customer feedback.

    This service uses a pretrained Hugging Face Transformer model to classify
    text as POSITIVE or NEGATIVE along with a confidence score.

    The model is loaded once during service initialization and reused for
    subsequent predictions to avoid the overhead of repeatedly loading the
    model into memory.

    NLP Concepts Demonstrated:
        - Transfer Learning
        - Pretrained Models
        - Text Classification

    Example:
        >>> service = SentimentService()
        >>> service.analyze("Customer support was very helpful")

        {
            "label": "POSITIVE",
            "score": 0.998
        }
    """
    def __init__(self):
        self.classifier = pipeline(task = "sentiment-analysis")

    def analyze(self, text):
        """
        Analyze the sentiment of a single text input.

        Args:
            text (str):
                Customer feedback text to analyze.

        Returns:
            dict:
                Dictionary containing:
                    - label (str): POSITIVE or NEGATIVE
                    - score (float): Model confidence score

        Example:
            >>> analyze("The application crashes frequently")

            {
                "label": "NEGATIVE",
                "score": 0.999
            }
        """
        result = self.classifier(text)
        result = result[0]
        return {
            "label": result["label"],
            "score": round(result["score"], 3)
        }