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
    language = 'zh'

    if query == 1:
        # 查询单个汉字
        with open(DICTIONARY_PATH[language]['char_base'], 'r', encoding='utf-8') as f:
            for item in ijson.items(f, 'item'):
                if item['char'] == query:
                    return item
        
    else:
        # 查询汉字词语
        with open(DICTIONARY_PATH[language]['word'], 'r', encoding='utf-8') as f:
            for item in ijson.items(f, 'item'):
                if item['word'] == query:
                    return item
                
    raise ValueError(f"Query '{query}' not found in the dictionary.")


if __name__ == '__main__':
    char_query = lookup('蛇')
    print(char_query)

    polyphonic_char_query = lookup('行')
    print(polyphonic_char_query)

    word_query = lookup('蟒蛇')
    print(word_query)
