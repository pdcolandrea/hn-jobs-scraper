import pandas as pd
from pathlib import Path


class FileHelper:
    def __init__(self):
        self.output_dir = "output"
        self.filename = "hn_jobs.csv"
        self.filepath = Path(self.output_dir) / self.filename

    def open_last_output_file(self):
        """
        Opens hn_jobs.csv from the output directory
        Returns a pandas DataFrame of the file contents
        """
        if not self.filepath.exists():
            return None
            raise FileNotFoundError(f"File not found: {self.filepath}")

        # Read the CSV file into a DataFrame
        df = pd.read_csv(self.filepath)

        print(f"Loaded {len(df)} rows from {self.filename}")
        return df

    def save_new_listings(self, new_listings: list[dict]):
        """
        Saves a new list of listings to the CSV file
        """
        df = pd.DataFrame(new_listings)
        df.to_csv(self.filepath, index=False)
