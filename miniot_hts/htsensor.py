# -*- coding: utf-8 -*-
"""
Raspberry Piに接続したDHT11温湿度センサーから温度と湿度を読み取る
Raspberry Piがない場合は，東京都の現在の温度，湿度を取得する

Author:  Atsushi Shibata
         shibata@m-info.co.jp
Licence: MIT

Copyright (c) 2017 Atsushi Shibata
"""

from urllib.request import urlopen
import re



class Hts_rpy():
    """
    Raspberry Piに接続した温湿度センサーから情報を得るクラス
    """

    def __init__(self):
        """
        クラスインスタンスを初期化
        """
        import RPi.GPIO as GPIO
        from . import dht
        # GPIOを初期化
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()

        # ピン番号14からセンサーの情報を得る
        self.sensor = instance = dht.DHT11(pin=14)
        # センサーから読み込んだデータ
        self.t = 0
        self.h = 0

    def read(self):
        """
        センサーとシリアル通信して情報を得る
        """
        result = self.sensor.read()
        if result.is_valid():
            self.t = result.temperature
            self.h = result.humidity
        else:
            # センサーからのデータが正しくないので
            # 現在の東京の気温，湿度を得る
            self.t, self.h = get_th_from_web()


class Hts_tokyo():
    """
    気象庁のWebからスクレイピングした結果を元に
    東京の現在の気温，湿度を得る
    """
    
    def __init__(self):
        """
        クラスインスタンスを初期化
        """
        self.t = 0
        self.h = 0

    def read(self):
        """
        Webから現在の気温，湿度を得る
        """
        self.t, self.h = get_th_from_web()


def get_th_from_web():
    """
    気象庁のWebから東京の現在の気温，湿度を得る関数
    """
    url = 'http://www.jma.go.jp/jp/amedas_h/today-44132.html'

    # Webページを取得，文字列(urf-8)に変換
    body = urlopen(url).read()
    body = body.decode('utf-8')

    # 正規表現のフラグ
    rg_flag =  re.S | re.M
    # データのテーブルを取得するための正規表現パターン
    dt_pat = re.compile(r'id="tbl_list".+?>(.+)</table>', rg_flag)
    # データテーブルを取得
    data_table = ''.join(dt_pat.findall(body))
    # 行(tr)，列(td)を取得する正規表現パターン
    tr_pat = re.compile(r'<tr>(.+?)</tr>', rg_flag)
    td_pat = re.compile(r'<td class=".+?">(.+?)</td>', rg_flag)
    # 最新の気温，湿度を初期化
    cur_temp = 0
    cur_hum = 0
    # trごとにループを回す
    for tr in tr_pat.findall(data_table):
        # tdの中のテキストを取得
        tds = td_pat.findall(tr)
        if len(tds) <= 7:
            # tdの要素数が8つなかったら，ループの先頭に戻る
            continue
        try:
            # tdの中の気温，湿度を数値に変換する
            if len(tds) == 9:
                # 冬期，積雪深データがある場合
                cur_temp = float(tds[1])
                cur_hum = int(tds[7])
            else:
                # 積雪深データがない場合
                cur_temp = float(tds[1])
                cur_hum = int(tds[6])
        except:
            # tdの中のテキストが数値に変換できなかった
            pass
    return cur_temp, cur_hum


