#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""处理原始数据

对原始的字典数据进行处理，得到适合查询的格式。

Author: Jaxon Ma
Date: 2026-1-30
"""

import json
import time

import ijson
import dictionary

DICTIONARY_PATH = {
    'zh': {
        'char_base': 'dictionary/chinese/char_base.json',
        'char_detail': 'dictionary/chinese/char_detail.json',
        'related': 'dictionary/chinese/related.json',
        'word': 'dictionary/chinese/word.json'
    }
}


PROCESSED_DICTIONARY_PATH = {
    'zh': {
        'char': 'processed/chinese/char.json',
        'word': 'processed/chinese/word.json'
    }
}


def load_data():
    """Load all dictionary data into memory for fast access"""
    print("Loading dictionary data...")
    char_base_data = {}
    char_detail_data = {}
    related_data = {}
    word_data = {}
    
    with open(DICTIONARY_PATH['zh']['char_base'], 'r', encoding='utf-8') as f:
        for item in ijson.items(f, 'item'):
            char_base_data[item['char']] = item
    
    with open(DICTIONARY_PATH['zh']['char_detail'], 'r', encoding='utf-8') as f:
        for item in ijson.items(f, 'item'):
            char_detail_data[item['char']] = item
    
    with open(DICTIONARY_PATH['zh']['related'], 'r', encoding='utf-8') as f:
        for item in ijson.items(f, 'item'):
            related_data[item['char']] = item
    
    with open(DICTIONARY_PATH['zh']['word'], 'r', encoding='utf-8') as f:
        for item in ijson.items(f, 'item'):
            word_data[item['word']] = item
    
    return char_base_data, char_detail_data, related_data, word_data


def process_char_data(char_base_data, char_detail_data, related_data):
    """Process character data"""
    results = []
    for char, base_item in char_base_data.items():
        char_result = {
            "char": char,
            "pinyin": base_item.get('pinyin', []),
            "radicals": base_item.get('radicals', ''),
            "pronunciations": [],
            "related_char": []
        }
        
        # Add pronunciations from detail
        if char in char_detail_data:
            detail_item = char_detail_data[char]
            pronunciations = detail_item.get('pronunciations', [])
            for pron in pronunciations:
                pinyin_explanation = {
                    "pinyin": pron.get('pinyin', ''),
                    "explanation": []
                }
                explanations = pron.get('explanations', [])
                for exp in explanations:
                    if "content" in exp:
                        pinyin_explanation['explanation'].append(exp['content'])
                char_result['pronunciations'].append(pinyin_explanation)
        
        # Add related chars
        if char in related_data:
            char_result['related_char'] = related_data[char].get('synonyms', [])
        
        results.append(char_result)
    
    return results


def process_word_data(word_data):
    """Process word data"""
    results = []
    for word, item in word_data.items():
        pinyin = item.get('pinyin', '').split()
        pinyin_processed = []
        
        for p in pinyin:
            if p and p[0].isupper():
                pinyin_processed.append(' '.join(list(p)))
            else:
                pinyin_processed.append(p)
        
        word_result = {
            "word": word,
            "pinyin": ' '.join(pinyin_processed),
            "explanation": item.get('explanation', [])
        }
        results.append(word_result)
    
    return results


def process():
    """处理原始数据，生成适合查询的格式"""
    char_base_data, char_detail_data, related_data, word_data = load_data()
    
    print("Processing Chinese characters...")
    t1 = time.time()
    char_results = process_char_data(char_base_data, char_detail_data, related_data)
    with open(PROCESSED_DICTIONARY_PATH['zh']['char'], 'w', encoding='utf-8') as f:
        json.dump(char_results, f, ensure_ascii=False, indent=2)
    t2 = time.time()
    print(f"Time taken: {t2 - t1:.2f} seconds")
    print("Done.")
    
    print("Processing Chinese words...")
    t3 = time.time()
    word_results = process_word_data(word_data)
    with open(PROCESSED_DICTIONARY_PATH['zh']['word'], 'w', encoding='utf-8') as f:
        json.dump(word_results, f, ensure_ascii=False, indent=2)
    t4 = time.time()
    print(f"Time taken: {t4 - t3:.2f} seconds")
    print("Done.")


if __name__ == '__main__':
    process()
