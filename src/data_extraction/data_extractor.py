import pandas as pd
from typing import List

class DataExtractor:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def extract_for_category(self, category: str, columns: List[str]) -> pd.DataFrame:
        """
        Returns the filtered DataFrame for the given category and selected columns.
        """
        filtered = self.df[self.df["SERVICE_CATEGORY"] == category]
        return filtered[columns].dropna(how="all")
