# -*- coding: utf-8 -*-
import datetime


def format_timestamp_time(timestamp):
    """unix 时间戳 转换为 年-月-日 时:分:秒 字符串"""
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime("%Y-%m-%d %H:%M:%S")


def format_timestamp_day(timestamp):
    """unix 时间戳 转换为 年-月-日 字符串"""
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime("%Y-%m-%d")