import re
import csv
from PyPDF2 import PdfReader
import pandas as pd
from typing import List

class CallRecordsExtractor:
    """
    Extract call records from PDF(s) and return as CSV or DataFrame.
    """

    def __init__(self):
        self.pattern = re.compile(
            r'(\d{1,3})\s+'                 
            r'(\d{2}-[A-Z]{3}-\d{2})\s+'    
            r'(\d{2}:\d{2}:\d{2})\s+'       
            r'(\d{11,15})\s+'               
            r'(\d+)\s+'                     
            r'(\d+)\s+'                     
            r'(\d+)\s+'                     
            r'(\d+)\s+'                     
            r'(\d+\.\d{2})'                 
        )
        self.headers = [
            "No.", "Date", "Time", "Number", 
            "Used Usage", "Billed Usage", "Free Usage", 
            "Chargeable Usage", "Amount"
        ]

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        reader = PdfReader(pdf_path)
        extracted_text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text += page_text + "\n"
        return extracted_text

    def extract_records_from_text(self, text: str) -> List[tuple]:
        return self.pattern.findall(text)

    def process_pdfs(self, pdf_paths: List[str]) -> pd.DataFrame:
        all_records = []
        for path in pdf_paths:
            text = self.extract_text_from_pdf(path)
            records = self.extract_records_from_text(text)
            all_records.extend(records)
        df = pd.DataFrame(all_records, columns=self.headers)
        df["Used Usage"] = pd.to_numeric(df["Used Usage"], errors="coerce")
        df["Number"] = df["Number"].astype(str)
        return df

    def save_to_csv(self, df: pd.DataFrame, csv_path: str):
        df.to_csv(csv_path, index=False, encoding="utf-8")

