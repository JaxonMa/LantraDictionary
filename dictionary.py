#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: 查词功能。先查询polyphone.json, 如果是单字，再查询char_detail.json,并且查询related_char.json。如果是词语，则查询word.json
# TODO: 放弃Vibe Coding提供的代码逻辑，先完成后端的数据处理。可以直接查到数据之后丢给前端
import json

DICTIONARY_PATH = {
    'chinese': {
        'char': 'dictionary/chinese/char.json',
        'polyphone': 'dictionary/chinese/polyphone.json',
        'related_char': 'dictionary/chinese/related_char.json',
        'word': 'dictionary/chinese/word.json'
    }
}


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
                with open(dict_path['polyphone'], 'r', encoding='utf-8') as f:
                    polyphone_data = json.load(f)
                    word_polyphone = [p for p in polyphone_data if p['char'] == query][0]  # 要的是字典而非列表，而这些列表必定只有一项，因此直接取[0]即可
                    char_explanation['pinyin'] = word_polyphone['pinyin']

                # 查询释义字典，获得词语解释
                with open(dict_path['char'], 'r', encoding='utf-8') as f:
                    char_data = json.load(f)
                    char_explanation_data = [e for e in char_data if e['char'] == query][0]
                    char_explanation['pronunciations'] = [e for e in char_explanation_data['pronunciations']]

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
