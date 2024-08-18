import re
import pandas as pd
import requests
from .constants import tables_url, site_encoding


class sophisthse:
    def __init__(
        self,
        verbose: bool = True,
    ):
        self.verbose = verbose
        self.tables_url = tables_url

    def get_table_url(self, series_name: str) -> str:
        return f"{tables_url}{series_name}.htm"

    def list_tables(self) -> pd.DataFrame:
        pattern = r"([0-9\/]+\s+[0-9:]+\s+[A,P]M)\s+(?:[0-9]+)\s+[^>]+>([^<]+)<"
        content = requests.get(self.tables_url).text
        content_list = content.split("<br>")[2:]
        rows = []
        for item in content_list:
            rows.extend(re.findall(pattern, item.strip()))
        df = pd.DataFrame(rows, columns=["date", "name"])
        df["date"] = pd.to_datetime(df["date"])
        df["name"] = df["name"].str.replace(r"\.htm$", "", regex=True)
        return df
