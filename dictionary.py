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
    result = {}
    return result


if __name__ == '__main__':
    char_query = lookup('蛇', 'zh')
    print(char_query)

    word_query = lookup('蟒蛇', 'zh')
    print(word_query)
