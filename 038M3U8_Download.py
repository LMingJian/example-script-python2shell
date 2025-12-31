import math
import re
import threading
import time
from os import path, mkdir

import requests
from Cryptodome.Cipher import AES


class M3U8:

    _ivx16 = b'0000000000000000'  # 钥匙
    _threads_number = 50

    def _aes(self, key: bytes, data: bytes):
        """AES 解密"""
        # 获取 aes 对象
        cipher_key = AES.new(key, AES.MODE_CBC, self._ivx16)
        # 解密
        decrypt_data = cipher_key.decrypt(data)
        return decrypt_data

    def download(self, base_url: str, ts_list: list, file_name: str, key=None):
        """
        根据 ts 链接列表下载

        Args:
          base_url: 路径前缀，比如 http://example.com/
          ts_list: ts 文件路径列表，比如 123456.ts
          file_name: 输出文件名
          key: 解密钥匙
        """
        error = ''
        for each in ts_list:
            while True:
                try:
                    content = requests.get(base_url + each, timeout=5).content
                    break
                except BaseException as e:
                    if e != error:
                        error = e
                        print(e)
            if key:
                content = self._aes(key, content)
            with open(file_name, 'ab+') as file:
                file.write(content)
            time.sleep(1)
        return 0

    def multi_download(self, base_url: str, ts_list: list, key=None):
        """根据 ts 文件列表多线程下载"""
        if not path.exists('./m3u8_report'):
            mkdir('./m3u8_report')
        threads = []
        length = len(ts_list)
        number = self._threads_number
        if length < number:
            print('File is too small')
            return 0
        for i in range(number):
            one_list = ts_list[math.floor(i / number * length):math.floor((i + 1) / number * length)]
            if key:
                p = threading.Thread(target=self.download, args=(base_url, one_list, f'./m3u8_report/{i}.ts', key))
            else:
                p = threading.Thread(target=self.download, args=(base_url, one_list, f'./m3u8_report/{i}.ts'))
            threads.append(p)
        for t in threads:
            t.setDaemon(True)
            t.start()
        print('Wait.......')
        for t in threads:
            t.join()
        print('End, Wait Process Recycling')
        return 0

    @staticmethod
    def read(file_path: str):
        """读取标准格式的 M3U8 文件"""
        with open(file_path, 'r') as file:
            data = file.readlines()
        result = []
        for each in data:
            link = each.strip()
            if not re.match('#', link) and link:
                result.append(link)
        return result

    @staticmethod
    def merge_ts(ts_path_file: str, result_file: str):
        """
        根据 ts 路径文件里的排列顺序合并 ts 文件

        Args:
          ts_path_file: ts 文件路径文件(已排序)
                        在文件管理器中打开 ts 所在文件夹，
                        排序，Shift + 右键，找到复制所有文件地址，
                        新建一个 txt 文本，粘贴内容
          result_file: 输出文件路径
        """
        with open(ts_path_file, 'r', encoding='UTF-8') as file:
            ts_list = file.readlines()
        with open(result_file, 'wb+') as f:
            for each in ts_list:
                ts_path = each.strip().replace('"', '')
                content = open(ts_path, 'rb').read()
                f.write(content)
        print("合并完成")
        return 0


if __name__ == "__main__":
    m3u8 = M3U8()
