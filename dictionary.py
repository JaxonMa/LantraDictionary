#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""查询字典（词典）模块

针对要查询的字词，对原始数据进行处理，得到适当的查询结果并返回。

Author: Jaxon Ma
Date: 2026-1-17
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


def lookup(query, lang='zh') -> dict[str, str]:
    """查询字典（词典）
    Args:
        query (str): 要查询的字词
        lang (str, optional): 语言代码. 默认为 'zh'.
    Returns:
        dict[str, str]: 查询结果
    """
    char_result = {
        "query": query,
        "pinyin": [],
        "radicals": "",
        "pronunciations": [],
        "related_char": []
    }
    word_result = {
        "query": query,
        "pinyin": "",
        "explanation": [],
    }

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
                    pronunciations = item.get('pronunciations', [])[0]
                    pinyin_explanation = {
                        "pinyin": "",
                        "explanations": []
                    }

                    for pron in pronunciations:
                        if pron == "pinyin":
                            pinyin_explanation["pinyin"] = pronunciations[pron]
                        elif pron == "explanations":
                            for explanation in pronunciations[pron]:
                                pinyin_explanation["explanations"].append(explanation["content"])
                    char_result['pronunciations'].append(pinyin_explanation)
                    break
        return char_result
    
    else:
        # 查询词语
        with open(DICTIONARY_PATH[lang]['word'], 'r', encoding='utf-8') as f:
            for item in ijson.items(f, 'item'):
                if item['word'] == query:
                    word_result['pinyin'] = item.get('pinyin', '')
                    word_result['explanation'] = item.get('explanation', [])
                    break
        return word_result



if __name__ == '__main__':
    char_query = lookup('蛇', 'zh')
    print(char_query)

    word_query = lookup('蟒蛇', 'zh')
    print(word_query)
