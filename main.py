from metadataextractor import MetadataExtractor
from flask import Flask

app = Flask(__name__)
if __name__ == "__main__":
    file_path = input("Ingrese el path del archivo: ")
    meta_data_extractor = MetadataExtractor(file_path)
    print(meta_data_extractor.extract())
