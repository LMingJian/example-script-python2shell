import builtins as __builtin__
import copy
import os.path
import time
from typing import IO

import multitasking
import requests
from retrying import retry
from tqdm import tqdm


def print(*args, **kwargs): # noqa
    """重写 print 以输出时间"""
    return __builtin__.print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), *args, **kwargs)


class LinkDownload:

    @staticmethod
    def get_file_size(url: str, header: dict) -> int:
        """获取文件大小"""
        # 发起 head 请求，即只会获取响应头部信息
        head = requests.head(url, headers=header)
        # 文件大小，以 B 为单位
        file_size = head.headers.get('Content-Length')
        if file_size is not None:
            file_size = int(file_size)
        else:
            file_size = 0
        print(f'File size: {file_size} B')
        return file_size

    @staticmethod
    def split_in_size(length: int, step: int) -> list[tuple[int, int]]:
        """
        根据分块大小分割文件

        :param length: 源文件大小
        :param step: 分块文件大小
        """
        # 分多块
        parts = []
        for each in range(0, length, step):
            parts.append((each, min(each + step, length)))
        # print(parts)
        return parts

    @staticmethod
    def split_in_thread(length: int, number: int) -> list[tuple[int, int]]:
        """
        根据线程多少分割文件

        :param length: 源文件大小
        :param number: 线程数
        """
        parts = []
        step = int(length / number) - 5
        flag = 1
        for each in range(0, length, step):
            if flag < number:
                parts.append((each, each + step))
            else:
                parts.append((each, length-1))
                break
            flag += 1
        # print(parts)
        return parts

    @staticmethod
    @retry
    def download(url: str, header: dict, file_name: str) -> int:
        """单线程链接下载"""
        time.sleep(1)
        headers = copy.deepcopy(header)
        # 发起 head 请求，即只会获取响应头部信息
        head = requests.head(url, headers=headers)
        # 文件大小，以 B 为单位
        file_size = head.headers.get('Content-Length')
        if file_size is not None:
            file_size = int(file_size)
            print(f'File size: {file_size} B')
        else:
            print('File is not exist')
            return 0
        temp_size = 0
        if os.path.exists(f'{file_name}'):
            temp_size = os.path.getsize(file_name)
            if temp_size == file_size:
                print('File already exist')
                return 0
            print(f'Downloaded：{temp_size} B')
            headers['Range'] = f'bytes={temp_size}-'
        response = requests.get(url, headers=headers, stream=True, timeout=60)
        # 一块文件的大小 B
        chunk_size = 1024
        bar = tqdm(total=file_size-temp_size, desc=f'Download: {file_name}')
        with open(file_name, mode='ab') as file:
            # 写入分块文件
            for chunk in response.iter_content(chunk_size=chunk_size):
                file.write(chunk)
                bar.update(chunk_size)
        # 关闭进度条
        bar.close()
        return 0

    result = []

    @multitasking.task
    def seg_download(self, url: str, header: dict, start: int, end: int) -> int:
        """分段下载"""
        file_name = f'{start}.CRDOWNLOAD'
        if os.path.exists(file_name):
            # 已下载内容跳过
            temp_size = os.path.getsize(file_name)
            print(f'Downloaded: {file_name}')
            start = start + temp_size
        # 必须对请求头 header 使用深复制以避免多线程运行时数据错位
        headers = copy.deepcopy(header)
        # 请求头标注下载起始和终点
        headers['Range'] = f'bytes={start}-{end}'
        head = requests.head(url, headers=headers)
        # 判断远端服务器是否支持分段下载
        if head.status_code not in [200, 206]:
            print(f'Status: {head.status_code}')
            print('Error! Unable to download')
            self.result.append(file_name)
            return 0
        response = requests.get(url, headers=headers, stream=True, timeout=60)
        print('Target: ' + response.headers.get('Content-Range'))
        # 一块文件的大小
        chunk_size = 1024
        with open(file_name, mode='ab') as file:
            # 写入分块文件
            for chunk in response.iter_content(chunk_size=chunk_size):
                file.write(chunk)
        print(f'Finish: {file_name}')
        # 记录分段缓存文件
        self.result.append(file_name)
        return 0

    def download_multi(self, number: int, url: str, header: dict, file_name: str) -> int:
        """
        多线程链接下载

        :param number: 预估线程数，最大 5，受限于 multitasking
        :param url: 链接
        :param header: 请求头
        :param file_name: 下载文件名
        """
        if number > 5:
            print('Error! Too many threads')
            return 0
        size = self.get_file_size(url, header)
        split_list = self.split_in_thread(size, number)
        for each in split_list:
            # 除第一段外，后续所有下载起始节点，为前一段终点加 1
            # 文件分割为(0, 1024),(1024, 2048), 下载时分段内容为(0, 1024),(1025, 2048)
            if split_list.index(each) == 0:
                self.seg_download(url, header, each[0], each[1])
            else:
                self.seg_download(url, header, each[0] + 1, each[1])
        # 等待线程执行
        multitasking.wait_for_tasks()
        # 合并文件
        self.merge_files(self.result, file_name)
        return 0

    def merge_files(self, file_list: list, file_name: str) -> int:
        """
        合并输入文件

        :param file_list: 缓存文件列表
        :param file_name: 输出文件名
        """
        file_number = []
        for each in file_list:
            file_number.append(int(each.replace('.CRDOWNLOAD', '')))
        file_number.sort()
        with open(file_name, mode='wb') as complete_file:
            for each in file_number:
                with open(f'{each}.CRDOWNLOAD', mode='rb') as temp_file:
                    for chunk in self.read_in_chunks(temp_file):
                        complete_file.write(chunk)
        print(f'Finish: {file_name}')
        for each in file_list:
            os.remove(each)
        return 0

    @staticmethod
    def read_in_chunks(file_object: IO, chunk_size: int = 1024 * 1024):
        """
        Lazy function (generator) to read a file piece by piece.
        Default chunk size: 1M
        You can set your own chunk size

        Usage::

            filePath = './path/filename'
            for chunk in read_in_chunks(filePath):
                process(chunk) # <do something with chunk>
        """
        while True:
            chunk_data = file_object.read(chunk_size)
            if not chunk_data:
                break
            yield chunk_data


if "__main__" == __name__:
    h = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE ',
    }
    u = 'https://download.jetbrains.com.cn/python/pycharm-community-2023.1.exe'
    n = 'pycharm-community-2023.1.exe'
    # certutil -hashfile pycharm-community-2023.1.exe SHA256
    # 6e35d2a846153bb89210a2f6febefe9ceba39871006041fa72aa2edbb4d932d7 *pycharm-community-2023.1.exe
    ld = LinkDownload()
    ld.download(u, h, n)
