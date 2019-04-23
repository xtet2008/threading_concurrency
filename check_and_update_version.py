# coding:utf-8
# @Time : 2019-04-23 13:14
# @Author : Andy.Zhang
# @Desc : Check and update labstack version from github in python3

import os
import requests
import sqlite3


def get_url(url):
    """封装 http网络get请求 (以便两个函数重复利用一个请求结果，这样不用请求两次浪费网络io)"""
    result = None

    try:
        res = requests.request("GET", url=url)
        result = res.json()
    except Exception as e:
        print(e)  # 增加网络异常处理（万一down掉了请求失败的情况下给个日志提示）

    return result


def check_version(res, v):
    """判断 echo的特定版本是否存在"""
    for i in range(len(res)):
        if v == res[i]["tag_name"]:
            print("version: %s already exists!" % v)
            break
    else:
        print("version: %s not exists" % v)


def save_version(res):
    """保存echo 的所有版本号"""
    version_value = [res[i]["tag_name"] for i in range(len(res))]

    db_exists = os.path.exists('/tmp/versions.db')
    db = sqlite3.connect('/tmp/versions.db')
    if db_exists:
        # update table
        db.execute('update versions set  version="%s" where repo="echo"' % version_value)
    else:
        # create table if not exists
        db.execute('CREATE TABLE if not exists versions (repo text, version text)')
        db.execute('insert into versions values ("echo","%s")' % version_value)
    db.commit()
    db.close()


if __name__ == "__main__":
    res_data = get_url(url="https://api.github.com/repos/labstack/echo/releases")
    if res_data:  # 增加异常判断：只有在正确请求得到数据时才处理，否则github down掉了，或者网络请求失败就不做处理
        check_version(res_data, "v3.3.3")
        save_version(res_data)
