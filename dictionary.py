#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: 查词功能。先查询polyphone.json, 如果是单字，再查询char_detail.json,并且查询related_char.json。如果是词语，则查询word.json
# TODO: 放弃Vibe Coding提供的代码逻辑，先完成后端的数据处理。可以直接查到数据之后丢给前端
import ijson

DICTIONARY_PATH = {
    'chinese': {
        'char': 'dictionary/chinese/char.json',
        'polyphone': 'dictionary/chinese/polyphone.json',
        'related_char': 'dictionary/chinese/related_char.json',
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
            if item['char'] == query:
                target_data = item
                break

    return target_data


def lookup(query: str, lang: str) -> dict[str, str]:
    dict_path = DICTIONARY_PATH[lang]
    char_explanation = {
        'char': query,
        'pinyin': [],
        'pronunciations': [],
        'related_char': [],
    }
    word_explanation = {
        'char': query,
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
                explanation_data = get_target_data(query, 'chinese', 'char')
                print(explanation_data)

                # 查询同义词词典，获得同义词列表
                with open(dict_path['related_char'], 'r', encoding='utf-8') as f:
                    related_char_data = json.load(f)
                    related_char_list = [rc for rc in related_char_data if rc['char'] == query][0]
                    char_explanation['related_char'] = related_char_list

                return char_explanation

            # 输入内容为词语，查询词典
            else:
                with open(dict_path['word'], 'r', encoding='utf-8') as f:
                    ...

    raise Exception('Failed to look up')
