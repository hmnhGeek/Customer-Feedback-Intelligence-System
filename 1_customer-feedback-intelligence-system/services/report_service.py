import pandas as pd


class ReportService:
    def generate_summary(self, feedback_df: pd.DataFrame) -> dict:
        total_feedback = len(feedback_df)

        positive_feedback = len(
            feedback_df[
                feedback_df["sentiment"] == "POSITIVE"
            ]
        )

        negative_feedback = len(
            feedback_df[
                feedback_df["sentiment"] == "NEGATIVE"
            ]
        )

        positive_percentage = round(
            (positive_feedback / total_feedback) * 100,
            2
        )

        negative_percentage = round(
            (negative_feedback / total_feedback) * 100,
            2
        )

        return {
            "total_feedback": total_feedback,
            "positive_feedback": positive_feedback,
            "negative_feedback": negative_feedback,
            "positive_percentage": positive_percentage,
            "negative_percentage": negative_percentage
        }