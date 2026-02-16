#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""查询字典（词典）模块

针对要查询的字词，对原始数据进行处理，得到适当的查询结果并返回。

Author: Jaxon Ma
Date: 2026-1-30
"""

from pymongo import MongoClient


def lookup(query: str, uri: str) -> dict[str, str]:
    """查询字典（词典）
    Args:
        query (str): 要查询的字词
    Returns:
        dict[str, str]: 查询结果
    """
    language = 'zh'  # 目前仅支持中文查询，后续可根据需要添加其他语言的支持

    match language:
        case 'zh':
            if len(query) == 1:
                # 查询单个汉字
                with MongoClient(uri) as client:
                    db = client['dictionary_chinese']
                    char_collection = db['char']
                    result = char_collection.find_one({'char': query})
                    if result:
                        result.pop('_id', None)  # 删除 MongoDB 自动生成的 _id 字段
                        return result
            else:
                # 查询汉字词语
                with MongoClient(uri) as client:
                    db = client['dictionary_chinese']
                    word_collection = db['word']
                    result = word_collection.find_one({'word': query})
                    if result:
                        result.pop('_id', None)  # 删除 MongoDB 自动生成的 _id 字段
                        return result

    raise ValueError(f"未找到查询结果: {query}")


if __name__ == '__main__':
    uri = 'mongodb://localhost:27017'
    char_query = lookup('蛇', uri)
    print(char_query)

    polyphonic_char_query = lookup('行', uri)
    print(polyphonic_char_query)

    word_query = lookup('蟒蛇', uri)
    print(word_query)
