#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Setup the MongoDB database for the dictionary application.
This script connects to a MongoDB server, creates a database and collection.
"""

from pymongo import MongoClient
import ijson

DICTIONARY_PATH = {
    'zh': {
        'char': 'processed/chinese/char.json',
        'word': 'processed/chinese/word.json'
    }
}


def load_zh_data() -> tuple[dict, dict]:
    print("Loading original Chinese dictionary data...")
    char_original_data = {}
    word_original_data = {}

    with open(DICTIONARY_PATH['zh']['char'], 'r', encoding='utf-8') as f:
        for item in ijson.items(f, 'item'):
            char_original_data[item['char']] = item

    with open(DICTIONARY_PATH['zh']['word'], 'r', encoding='utf-8') as f:
        for item in ijson.items(f, 'item'):
            word_original_data[item['word']] = item

    return char_original_data, word_original_data

def insert_data_to_mongodb(char_data: dict, word_data: dict, uri: str, lang: str='zh',):
    match lang:
        case 'zh':
            print("Inserting Chinese dictionary data into MongoDB...")

            with MongoClient(uri) as client:
                db = client['dictionary_chinese']
                char_collection = db['char']
                word_collection = db['word']

                # Insert character data
                char_docs = list(char_data.values())
                if char_docs:
                    char_collection.insert_many(char_docs)
                    print(f"Inserted {len(char_docs)} character documents into MongoDB.")

                # Insert word data
                word_docs = list(word_data.values())
                if word_docs:
                    word_collection.insert_many(word_docs)
                    print(f"Inserted {len(word_docs)} word documents into MongoDB.")
    


def main():
    uri = 'URI_TO_YOUR_MONGODB_SERVER'  # Replace with your MongoDB URI
    char_data, word_data = load_zh_data()
    insert_data_to_mongodb(char_data, word_data, lang='zh', uri=uri)        


if __name__ == '__main__':
    main()