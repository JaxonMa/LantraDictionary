#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""处理原始数据

对原始的字典数据进行处理，得到适合查询的格式。

Author: Jaxon Ma
Date: 2026-1-30
"""

import ijson
import json
import dictionary


TARGET_PATH = {
    'zh': {
        'char': 'processed/chinese/char.json',
        'word': 'processed/chinese/word.json'
    }
}


def process():
    """处理原始数据，生成适合查询的格式"""
    print("Processing Chinese characters...")
    with open(dictionary.DICTIONARY_PATH['zh']['char_base'], 'r', encoding='utf-8') as char_file:
        parser = ijson.items(char_file, 'item.char')
        with open(TARGET_PATH['zh']['char'], 'a', encoding='utf-8') as target_file:
            target_file.write("[\n")  
            for item in parser:
                result = dictionary.lookup(item)
                json_obj = ''.join((str(result), ',\n'))
                json.dump(json_obj, target_file, ensure_ascii=False)
            target_file.write("]\n")
    print("Done.")

    print("Processing Chinese words...")
    with open(dictionary.DICTIONARY_PATH['zh']['word'], 'r', encoding='utf-8') as word_file:
        parser = ijson.items(word_file, 'item.word')
        with open(TARGET_PATH['zh']['word'], 'a', encoding='utf-8') as target_file:
            target_file.write("[\n")
            for item in parser:
                result = dictionary.lookup(item)
                json_obj = ''.join((str(result), ',\n'))
                json.dump(json_obj, target_file, ensure_ascii=False)
            target_file.write("]\n")
    print("Done.")


if __name__ == '__main__':
    process()
