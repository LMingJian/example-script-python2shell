import os

import requests

"""
A: 实现酷我音乐的搜索以及下载
PS: 由于网页端限制只能下载高品
"""


class KwMusic:
    _keyword = ''
    _headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70",
        "Cookie": "_ga=GA1.2.27154117.1626657535; "
                  "_gid=GA1.2.248511086.1626657535; "
                  "_gat=1;"
                  "Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1626657535;"
                  "Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1626657535;"
                  "kw_token=BY7LSG2I9F",
        "csrf": "BY7LSG2I9F",
        "Referer": "http://www.kuwo.cn/search/list?key=flag"
    }
    _searchUrl = "http://www.kuwo.cn/api/www/search/searchMusicBykeyWord"
    _searchParams = {
        "key": '',
        "pn": "1",
        "rn": "10",
        "httpsStatus": "1",
        "reqId": "51f0bad0-e82f-11eb-8394-4d31ba89580c",
    }
    _infoUrl = "http://www.kuwo.cn/api/www/music/musicInfo"
    _infoParams = {
        'mid': '',
        'httpsStatus': '1',
        'reqId': "89010bf0-e835-11eb-8394-4d31ba89580c",
    }
    _downloadGetUrl = "http://www.kuwo.cn/url"
    _downloadUrl = ''
    _downloadPath = 'D://ZMusic//'
    _downloadGetParams = {
        'format': 'mp3',
        'rid': '4266175',
        'response': 'url',
        'type': 'convert_url3',
        'br': '128kmp3',
        'from': 'web',
        't': '1626660219439',
        'httpsStatus': '1',
        'reqId': 'c4cb7f31-e83a-11eb-8394-4d31ba89580c',
    }

    def search(self):
        self._keyword = input('请输入音乐名称: ')
        self._searchParams['key'] = self._keyword
        result = requests.get(url=self._searchUrl, headers=self._headers, params=self._searchParams).json()
        print('已查找到结果: ' + result['data']['total'])
        print('============================')
        print('音乐 | 作者 | ID')
        for each in result["data"]["list"]:
            print(each["name"], end=' | ')
            print(each["artist"], end=' | ')
            print(each["rid"])
            print('----------------------------')

    def download(self):
        self._keyword = input('请输入要下载的音乐ID: ')
        self._infoParams['mid'] = self._keyword
        result = requests.get(url=self._infoUrl, headers=self._headers, params=self._infoParams).json()
        print('============================')
        print('音乐 | 作者 | VIP')
        print(result["data"]["name"], end=' | ')
        print(result["data"]["artist"], end=' | ')
        print(result["data"]["isListenFee"])
        print('============================')
        if not input('是否要下载(Enter进行下载): '):
            self._downloadUrl = requests.get(url=self._downloadGetUrl,
                                             headers=self._headers, params=self._downloadGetParams).json()['url']
            print('下载: ' + self._downloadUrl)
            if not os.path.exists(self._downloadPath):
                os.mkdir(self._downloadPath)
            try:
                content = requests.get(url=self._downloadUrl).content
                with open(self._downloadPath + "{}({}).mp3".format(result["data"]["name"], result["data"]["artist"]),
                          "wb") as file:
                    file.write(content)
                    print("下载成功, 请到D://ZMusic//查看")
            except BaseException as e:
                print('下载失败')
                print(e)
        else:
            print('退出系统')

    def start(self):
        print('=========欢迎进入=========')
        print('1.搜索')
        print('2.下载')
        print('========================')
        flag = input('请选择功能: ')
        try:
            if flag == '1':
                self.search()
            elif flag == '2':
                self.download()
            else:
                return 0
        except BaseException as e:
            print('系统错误')
            print(e)


if __name__ == "__main__":
    KwMusic().start()
