#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/26 17:01
# @Author  : name
# @File    : Util.py
import json
from TimeUtil import TimeUtil


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
        setting_path = "resources/setting.json"
        with open(setting_path, 'r') as setting_file:
            return json.load(setting_file)

    # 获取任务执行时间间隔
    # timer_id : 要读取的定时器之ID（zhihu：知乎，weibo：微博）
    # unit: 返回结果的单位（seconds：秒，minutes：分钟，hour：小时）
    @staticmethod
    def read_timer(timer_id, unit):
        log_msg = "Util-->read_interval:"
        if timer_id is None:
            print(log_msg + "未指定时器ID，将返回默认值：3")
            return 3
        if unit is None or ("seconds" != unit and "minutes" != unit and "hour" != unit):
            print(log_msg + "未指定输出单位，或单位有误，将使用默认值：seconds")
            unit = "seconds"
        # 读取配置文件
        timer = Util.load_setting()["timers"][timer_id]
        origin_interval = str(timer["interval"])
        origin_unit = str(timer["unit"])
        print("定时器间隔：", origin_interval)
        # 检查配置是否正确
        # if origin_interval is None or not origin_interval.isdigit():
        if origin_interval is None or not Util.is_number(origin_interval):
            print(log_msg + "定时器时间间隔配置有误，将返回默认值：3")
            return 3
        if origin_unit is None or ("seconds" != origin_unit and "minutes" != origin_unit and "hour" != origin_unit):
            print(log_msg + "定时器时间单位配置有误，将返回默认值：3")
            return 3
        seconds = float(origin_interval)
        if "seconds" == origin_unit:
            seconds = origin_interval
        elif "minutes" == origin_unit:
            seconds = seconds * 60
        elif "hour" == origin_unit:
            seconds = seconds * 60 * 60
        if "seconds" == unit:
            return seconds
        elif "minutes" == unit:
            print("1")
            return TimeUtil.to_minutes(seconds)
        elif "hour" == unit:
            return TimeUtil.to_hour(seconds)
        else:
            return seconds

    # 判断是否是数字
    @staticmethod
    def is_number(str_number):
        if (str_number.split(".")[0]).isdigit() or str_number.isdigit() or (str_number.split('-')[-1]).split(".")[-1].isdigit():
            return True
        else:
            return False
