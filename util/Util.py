#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/26 17:01
# @Author  : name
# @File    : Util.py
import json
from string import digits


class Util:
    def __init__(self):
        self.name = "工具类"

    # 生成流水号
    @staticmethod
    def product_no(prefix):
        # 流水号获取逻辑，待补充
        pass

    # 读取配置文件
    @staticmethod
    def load_setting():
        setting_path = "ini/setting.json"
        with open(setting_path, 'r', encoding='utf-8') as setting_file:
            return json.load(setting_file)

    # 提取文件名
    @staticmethod
    def get_file_name(full_name):
        return full_name.split('\\').pop().split('/').pop().rsplit('.', 1)[0]

    # 移除字符串中的指定字符
    @staticmethod
    def remove_char(content, char_list):
        if not content or len(content) <= 0 or not char_list or len(char_list) <= 0:
            return content
        for char in char_list:
            if char == '@num':
                content = Util.remove_num(content)
                continue
            if len(char) > 2 and '@@' == char[0:2]:
                char = char[1:]
            content = content.replace(char, '')
        return content

    @staticmethod
    def remove_num(content):
        if not content or len(content) <= 0:
            return content
        table = content.maketrans('', '', digits)
        return content.translate(table)

    # 判断是否是数字
    @staticmethod
    def is_number(str_number):
        if (str_number.split(".")[0]).isdigit() or str_number.isdigit() or (str_number.split('-')[-1]).split(".")[-1].isdigit():
            return True
        else:
            return False
