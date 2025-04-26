import pandas as pd

class FileProcessor:
    def __init__(self):
        self.original_data = None
        self.filtered_data = None
        self.category_product_mapper = {}
        self.valid_categories = []
        self.required_columns = []


    def validate_required_columns(self, df, required_columns) -> bool:
        """
        Ensure the input DataFrame has all the required columns.
        """
        self.required_columns = required_columns
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        return True


    def process_file(self, data, mapper: dict[str, str], valid_categories: list[str]) -> pd.DataFrame:
        self.original_data = data
        self.category_product_mapper = mapper
        self.valid_categories = valid_categories

        self.filter_category()
        self.prepare_required_columns()
        self.map_category_to_product()

        return self.filtered_data


    def filter_category(self):
        self.filtered_data = self.original_data[self.original_data['SERVICE_CATEGORY'].isin(self.valid_categories)].copy()


    def map_category_to_product(self):
        self.filtered_data['PRODUCT'] = self.filtered_data['SERVICE_CATEGORY'].map(self.category_product_mapper)
        cols = list(self.filtered_data.columns)
        cols.insert(2, cols.pop(cols.index('PRODUCT')))
        self.filtered_data = self.filtered_data[cols]


    def prepare_required_columns(self):
        self.filtered_data = self.filtered_data[self.required_columns]

    