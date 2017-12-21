# -*- coding: utf-8 -*-
"""
Author:  Atsushi Shibata
         shibata@m-info.co.jp
Licence: MIT

Copyright (c) 2017 Atsushi Shibata
"""

__all__ = ['read', 'get_temp', 'get_humid', 'calc_hi',
           'calc_dindex', 'get_dindex_advice',
           'get_heatstroke_advice', 'get_virus_advice',
           'get_thinfo' ]

from datetime import datetime
from .htsensor import Hts_rpy, Hts_tokyo


def prepare():
    """
    環境に応じて，センサーのインスタンスを生成する
    """

    # 環境を判別，Raspberry Piかそれ以外か
    
    try:
        # Raspberry Piにプリインストールされているモジュールをインポート
        import RPi
        is_rpy = True
    except:
        is_rpy = False
    
    if is_rpy:
        sensor = Hts_rpy()
    else:
        sensor = Hts_tokyo()

    return sensor

sensor = prepare()

def read():
    """
    センサーから現在の気温，湿度を読み込む
    """
    sensor.read()


def get_temp():
    """
    読み込んだ温度を返す
    """
    return sensor.t


def get_humid():
    """
    読み込んだ湿度を返す
    """
    return sensor.h


# 紙面に掲載した関数

def calc_hi(t, h):
    # 気温と湿度からヒートインデックスを計算して返す
    ft = (t*9.0/5.0)+32.0  # 気温を摂氏から華氏に変換

    hs = h**2
    ts = ft**2

    # 計算用の係数
    c = [None, -42.379, 2.04901523, 10.14333127, -0.22475541,
        -6.83783*10.0**(-3.0), -5.481717*10.0**(-2.0),
        1.22874*10.0**(-3.0), 8.5282*10.0**(-4.0),
        -1.99*10.0**(-6.0)]
    
    heat_index = (c[1]+(c[2]*ft)+(c[3]*h)+(c[4]*ft*h)+
                  (c[5]*ts)+(c[6]*hs)+
                  (c[7]*ts*h)+(c[8]*ft*hs)+
                  (c[9]*ts*hs))

    # round to one decimal place and return in celsius
    return round(((heat_index-32.0)*5.0/9.0), 1)


def calc_dindex(t, h):
    # 不快指数を計算する
    dindex = 0.81*t+0.01*h*(0.99*t-14.3)+46.3
    return int(dindex)  # 計算した不快指数を整数にして返す


def get_dindex_advice(d):
    # 不快指数から体感とアドバイスを文字列で返す関数
    if d <= 60:
        return "寒くないですか？ 暖房をつける/強めるか，クーラーを弱くしましょう。"
    if d > 60 and d <= 75:
        return "快適です。"
    if d > 75 and d <= 80:
        return "ちょっと暑いですね。クーラーを強めるか，暖房を弱くしましょう。"
    if d > 80:
        return "かなり暑いです。クーラーをつけましょう。"


def get_heatstroke_advice(hi):
    # ヒートインデックスから熱中症のアドバイスを返す関数
    if hi >= 32 and hi < 41:
        return "長時間屋外に出るときには日射病に注意してください。"
    if hi >= 41 and hi < 54:
        return "屋外での日射病に注意。長時間同じ状態が続くと熱中症にかかります。"
    if hi >= 54:
        return "熱中症に注意してください。"
    return ""


def get_virus_advice(h):
    # 湿度を受け取って風邪やインフルエンザのアドバイスを返す関数
    if h < 20:
        return "風邪やインフルエンザの危険性が高まっています。加湿をして湿度を上げてください。"
    if h < 40:
        return ("湿度が低く，風邪やインフルエンザにかかりやすい状態になりつつあるようです。"
                "外から帰ったら，うがいや手洗いをするように習慣づけましょう。")
    return ""


def get_thinfo(t, h):
    # 温度と湿度から，不快指数などの情報を文字列として返す
    s = ''   # 返り値として返す文字列
    n = datetime.now()  # 現在の時刻
    # 日時を文字列に変換する
    s = s+"%d月%d日%d時%d分，" % (n.month, n.day, n.hour, n.minute)
    # 不快指数の情報を追加
    dindex = calc_dindex(t, h)
    s = s+get_dindex_advice(dindex)
    # 熱中症の情報を追加
    hi = calc_hi(t, h)
    s = s+get_heatstroke_advice(hi)   # 熱中症のアドバイスを得る
    # 風邪，インフルエンザの情報を追加
    s = s+get_virus_advice(h)
    return s

