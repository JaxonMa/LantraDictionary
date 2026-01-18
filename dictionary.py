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


def _get_target_data(query: str, lang: str, dict_name: str) -> dict[str, str | list[dict]]:
    """获得目标字典（词典）中指定的原始数据

    :param query: 要查询的字词
    :param lang: 字词的语言，可选值为 'zh', 'en'
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


def lookup(query: str, lang: str) -> dict[str, str | list[dict]]:
    """在字典（词典）中查询指定的字词

    :param query: 要查询的字词
    :param lang: 字词的语言，可选值为 'chinese', 'english'

    :return: 指定字词的查询数据
    """
    char_explanation = {
        'char': query,
        'pinyin': [],
        'radicals': '',
        'pronunciations': [],
        'related_char': [],
    }
    word_explanation = {
        'word': query,
        'pinyin': '',
        'explanation': ''
    }

    match lang:
        case 'zh':
            # 输入内容为单字，查询字典
            if len(query) == 1:
                # 查询基本字典，获得所有发音及偏旁部首
                char_base_data = _get_target_data(query, lang, 'char_base')
                char_explanation['pinyin'] = char_base_data['pinyin']
                char_explanation['radicals'] = char_base_data['radicals']

                # 查询释义字典，获得词语解释
                pronunciations_data = _get_target_data(query, lang, 'char_detail')
                explanations = pronunciations_data['pronunciations']
                # 仅保留原始数据中的'content'一项
                for expl in explanations:
                    expl_data = {'pinyin': expl['pinyin'],
                                 'explanation': []}
                    for single_expl in expl['explanations']:
                        # noinspection PyTypeChecker
                        # 此处是根据原始数据的特征编写的，每一个释义中都包含content键，因此这样书写不会有问题
                        expl_data['explanation'].append(single_expl['content'])
                    char_explanation['pronunciations'].append(expl_data)

                # 查询同义词词典，获得同义词列表
                try:
                    related_char_data = _get_target_data(query, lang, 'related')
                    char_explanation['related_char'] = related_char_data['synonyms']
                # 同义词词典中没有数据
                except KeyError:
                    char_explanation['related_char'] = []

                return char_explanation

            # 输入内容为词语，查询词典
            else:
                try:
                    word_data = _get_target_data(query, lang, 'word')
                    word_explanation['pinyin'] = word_data['pinyin']
                    word_explanation['explanation'] = word_data['explanation']
                    return word_explanation
                # 数据库中没有要查询的字词
                except KeyError as e:
                    raise Exception('Word not found', e)

        case 'en':
            raise Exception('English is not supported yet.')

        case _:
            raise Exception('Failed to look up')


if __name__ == '__main__':
    char_query = lookup('蛇', 'zh')
    print(char_query)

    word_query = lookup('蟒蛇', 'zh')
    print(word_query)
