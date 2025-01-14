# backend/agents/data_ingestion/processor.py
import pandas as pd
import PyPDF2
from docx import Document
import json

class DataProcessor:
    def __init__(self):
        self.supported_formats = {
            'csv': self._process_csv,
            'xlsx': self._process_excel,
            'pdf': self._process_pdf,
            'docx': self._process_docx
        }

    def process_file(self, file_path, file_type):
        if file_type.lower() not in self.supported_formats:
            raise ValueError(f"Unsupported file type: {file_type}")

        return self.supported_formats[file_type.lower()](file_path)

    def _process_csv(self, file_path):
        df = pd.read_csv(file_path)
        return df.to_dict(orient='records')

    def _process_excel(self, file_path):
        df = pd.read_excel(file_path)
        return df.to_dict(orient='records')

    def _process_pdf(self, file_path):
        text_content = []
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text_content.append(page.extract_text())
        return {'content': '\n'.join(text_content)}

    def _process_docx(self, file_path):
        doc = Document(file_path)
        content = []
        for paragraph in doc.paragraphs:
            if paragraph.text:
                content.append(paragraph.text)
        return {'content': '\n'.join(content)}