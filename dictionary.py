#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ijson

DICTIONARY_PATH = {
    'chinese': {
        'char': 'dictionary/chinese/char.json',
        'polyphone': 'dictionary/chinese/polyphone.json',
        'related': 'dictionary/chinese/related.json',
        'word': 'dictionary/chinese/word.json'
    }
}


def get_target_data(query: str, lang: str, dict_name: str) -> dict[str, str]:
    """
    获得目标字典中指定的数据
    :param query: 要查询的字词
    :param lang: 字词的语言，可选值为 'chinese', 'english'
    :param dict_name: 词典的名字。根据lang的不同，其对应的可选的词典名也会发生变化
    :return: 指定字词的数据。
        e.g: {'index': 6, 'char': '厂', 'strokes': 2, 'pinyin': ['chǎng', 'ān', 'hàn'], 'frequency': 0}
    """
    dict_path = DICTIONARY_PATH[lang]
    target_data = {}
    with open(dict_path[dict_name], 'r', encoding='utf-8') as f:
        parser = ijson.items(f, 'item')
        for item in parser:
            # 尝试在字典中查询，如出现KeyError，则说明传入的dict_name不是字典，则改用词典的判断逻辑
            try:
                if item['char'] == query:
                    target_data = item
                    break
            except KeyError:
                if item['word'] == query:
                    target_data = item
                    break

    return target_data


def lookup(query: str, lang: str) -> dict[str, str]:
    char_explanation = {
        'char': query,
        'pinyin': [],
        'pronunciations': [],
        'related_char': [],
    }
    word_explanation = {
        'word': query,
        'pinyin': '',
        'explanation': ''
    }

    match lang:
        case 'chinese':
            # 输入内容为单字，查询字典
            if len(query) == 1:
                # 查询多音字字典，获得所有发音
                polyphone_data = get_target_data(query, 'chinese', 'polyphone')
                char_explanation['pinyin'] = polyphone_data['pinyin']

                # 查询释义字典，获得词语解释
                pronunciations_data = get_target_data(query, 'chinese', 'char')
                char_explanation['pronunciations'] = pronunciations_data['pronunciations']

                # 查询同义词词典，获得同义词列表
                related_char_data = get_target_data(query, lang, 'related')
                char_explanation['related_char'] = related_char_data['synonyms']
                return char_explanation

            # 输入内容为词语，查询词典
            else:
                word_data = get_target_data(query, 'chinese', 'word')
                word_explanation['pinyin'] = word_data['pinyin']
                word_explanation['explanation'] = word_data['explanation']
                return word_explanation
        case 'english':
            pass

    raise Exception('Failed to look up')


if __name__ == '__main__':
    char_query = lookup('厂', 'chinese')
    print(char_query)

    word_query = lookup('工厂', 'chinese')
    print(word_query)
