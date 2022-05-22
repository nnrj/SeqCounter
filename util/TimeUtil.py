#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/27 22:49
# @Author  : name
# @File    : TimeUtil.py
import math


class TimeUtil:

    # 秒转秒
    @staticmethod
    def to_seconds(seconds):
        return seconds

    # 秒转分钟
    @staticmethod
    def to_minutes(seconds):
        return math.ceil(seconds / 60.00)

    # 秒转小时
    @staticmethod
    def to_hour(seconds):
        return math.ceil((TimeUtil.to_minutes(seconds)) / 60.00)

