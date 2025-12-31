import html

import requests
from bs4 import BeautifulSoup


class Source:

    url = 'https://igg-games.com'


class IGG:

    _source = Source()

    def get_page(self):
        response = requests.get(self._source.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        tm_header = soup.find('body').find('div', class_='tm-header-mobile')
        title_a = tm_header.find_all('a')
        page = {}
        for each in title_a:
            if each.string and each.get('href'):
                page[each.string] = each.get('href')
        for key, value in page.items():
            print(f'{key} | {value}')
        """
        ['Home', 'Torrent Site', 'Action', 'Adult', 'Adventure', 'Anime', 'Building', 
        'Casual', 'Eroge', 'Hack and Slash', 'Hidden Object', 'Horror', 'Management', 
        'Mature', 'Nudity', 'Open World / Sandbox', 'Point & Click', 'Puzzle', 'Racing', 
        'RPG', 'RTS', 'Sci-fi', 'Shooter', 'Simulation', 'Sport', 'Strategy', 'Survival', 
        'Text-Based', 'Tower Defense', 'Turn-Based', 'Visual Novel', 'Download VR Games Torrent', 
        'VR Games', 'Random', 'FAQ', 'GAME LIST', 'GAME REQUEST']
        """

    @staticmethod
    def get_game():
        link = input('请输入链接：')
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        tm_main = soup.find('body').find('div', id='tm-main')
        article = tm_main.find_all('article')
        print('----------------------------')
        for each in article:
            img = each.find('img').get('src')
            title = each.find('h2').string
            link = each.find('h2').find('a').get('href')
            time = each.find('time').string
            describe = html.unescape(each.find('div', class_='uk-margin-medium-top').find('p').string)
            print(img)
            print(title)
            print(link)
            print(time)
            print(describe)
            print('----------------------------')

    @staticmethod
    def get_download():
        link = input('请输入链接：')
        response = requests.get(link)
        sour = BeautifulSoup(response.text, 'html.parser')
        content = sour.find('div', class_='uk-margin-medium-top').find_all('a')
        print('-------------------------------------')
        for each in content:
            if each.string and 'Download' in each.string:
                print(each.get('href'))
        print('-------------------------------------')

    def menu(self):
        print("====================")
        print("欢迎进入系统")
        print("====================")
        print('1.获取分类')
        print('2.分类主页')
        print('3.下载链接')
        print('6.退出')
        print("====================")
        while True:
            flag = input('请选择功能: ')
            if flag == '1':
                self.get_page()
            elif flag == '2':
                self.get_game()
            elif flag == '3':
                self.get_download()
            elif flag == '6':
                break
            else:
                print('无此功能')
                continue
        print('退出系统')


if __name__ == '__main__':
    IGG().menu()
