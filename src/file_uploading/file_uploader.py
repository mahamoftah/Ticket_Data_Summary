import pandas as pd
import os
import logging

class FileUploader:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def upload_file(self, file):
        self.uploaded_file = file
        self.filename = file.name
        self.extension = self.filename.split('.')[-1]

    def is_valid_format(self):
        self.logger.info(f"File extension: {self.extension}")
        return self.extension in ['csv', 'txt']


    def convert_txt_to_csv(self, output_csv_path):
        try:
            df = pd.read_csv(self.uploaded_file, encoding='utf-8')
            df.to_csv(output_csv_path, index=False, header=True)
            return df
        except Exception as e:
            raise ValueError(f"Error during TXT to CSV conversion: {e}")

    def load_csv(self):
        try:
            return pd.read_csv(self.uploaded_file, encoding='utf-8')
        except Exception as e:
            raise ValueError(f"Error loading CSV: {e}")
