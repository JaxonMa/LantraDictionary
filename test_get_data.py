#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import dictionary


def main():
    res = dictionary.lookup('厂', 'chinese')
    print(res)

if __name__ == '__main__':
    main()