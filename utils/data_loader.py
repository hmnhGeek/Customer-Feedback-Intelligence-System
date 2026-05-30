import pandas as pd


class DataLoader:
    REQUIRED_COLUMNS = ["feedback"]

    def load_csv(self, uploaded_file) -> pd.DataFrame:
        try:
            df = pd.read_csv(uploaded_file)

        except Exception as error:
            raise ValueError(
                f"Failed to read CSV file: {error}"
            )

        self._validate_columns(df)

        self._remove_empty_feedback(df)

        return df

    def _validate_columns(self, df: pd.DataFrame) -> None:
        missing_columns = [
            column
            for column in self.REQUIRED_COLUMNS
            if column not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {missing_columns}"
            )

    def _remove_empty_feedback(self, df: pd.DataFrame) -> None:
        df.dropna(
            subset=["feedback"],
            inplace=True
        )

        df["feedback"] = (df["feedback"].astype(str).str.strip())

        df.drop(
            df[
                df["feedback"] == ""
            ].index,
            inplace=True
        )