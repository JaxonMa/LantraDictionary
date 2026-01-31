#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""查询字典（词典）模块

针对要查询的字词，对原始数据进行处理，得到适当的查询结果并返回。

Author: Jaxon Ma
Date: 2026-1-30
"""

import ijson

DICTIONARY_PATH = {
    'zh': {
        'char_base': 'dictionary/chinese/char_base.json',
        'char_detail': 'dictionary/chinese/char_detail.json',
        'related': 'dictionary/chinese/related.json',
        'word': 'dictionary/chinese/word.json'
    }
}


def lookup(query,) -> dict[str, str]:
    """查询字典（词典）
    Args:
        query (str): 要查询的字词
    Returns:
        dict[str, str]: 查询结果
    """
    char_result = {
        "char": query,
        "pinyin": [],
        "radicals": "",
        "pronunciations": [],
        "related_char": []
    }
    word_result = {
        "word": query,
        "pinyin": "",
        "explanation": [],
    }

    lang = 'zh'  # 目前仅支持中文查询

    if len(query) == 1:
        # 查询单个汉字  
        with open(DICTIONARY_PATH[lang]['char_base'], 'r', encoding='utf-8') as f:
            # 获得汉字基本信息
            for item in ijson.items(f, 'item'):
                if item['char'] == query:
                    char_result['pinyin'] = item.get('pinyin', [])
                    char_result['radicals'] = item.get('radicals', [])
                    break

        with open(DICTIONARY_PATH[lang]['char_detail'], 'r', encoding='utf-8') as f:
            # 获得汉字详细解释
            for item in ijson.items(f, 'item'):
                if item['char'] == query:
                    pronunciations = item.get('pronunciations', [])
                    pinyin_explanation = {
                        "pinyin": "",
                        "explanation": []
                    }

                    for pron in pronunciations:
                        # 筛选原始数据中的信息
                        pinyin_explanation['pinyin'] = pron.get('pinyin', '')
                        explanations = pron.get('explanations', [])
                        for exp in explanations:
                            if "content" in exp:
                                pinyin_explanation['explanation'].append(exp['content'])
                                char_result['pronunciations'].append(pinyin_explanation)
                            pinyin_explanation = {
                                "pinyin": "",
                                "explanation": []
                            }
                    break

        with open(DICTIONARY_PATH[lang]['related'], 'r', encoding='utf-8') as f:
            # 获得相关汉字
            for item in ijson.items(f, 'item'):
                if item['char'] == query:
                    char_result['related_char'] = item.get('synonyms', [])
                    break
        return char_result
    
    else:
        # 查询词语
        with open(DICTIONARY_PATH[lang]['word'], 'r', encoding='utf-8') as f:
            for item in ijson.items(f, 'item'):
                if item['word'] == query:
                    pinyin = item.get('pinyin', '').split()
                    pinyin_processed = []

                    for p in pinyin:
                        # 处理拼音中的大写英文字母，在其之间添加空格，保证前端拼音显示正确
                        if p[0].isupper():
                            pinyin_processed.append(' '.join(list(p)))
                        else:
                            pinyin_processed.append(p)

                    word_result['pinyin'] = ' '.join(pinyin_processed)
                    word_result['explanation'] = item.get('explanation', [])
                    break
        return word_result


if __name__ == '__main__':
    char_query = lookup('蛇')
    print(char_query)

    polyphonic_char_query = lookup('行')
    print(polyphonic_char_query)

    word_query = lookup('蟒蛇')
    print(word_query)
