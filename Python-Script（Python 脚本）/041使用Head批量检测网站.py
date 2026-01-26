import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


def check_website_accessibility(url):
    try:
        response = requests.head(url, timeout=1)  # 发送HEAD请求检查可访问性
        status_code = response.status_code
        accessible = status_code == 200
        return {'status_code': status_code, 'accessible': accessible}
    except requests.exceptions.RequestException as e:
        # 处理请求异常
        return {'status_code': None, 'accessible': False, 'error': str(e)}


def check_websites_accessibility_multithreaded(urls, max_threads):
    with ThreadPoolExecutor(max_workers=max_threads) as executor, tqdm(total=len(urls), desc="检查网站可访问性") as pbar:
        futures = {executor.submit(check_website_accessibility, url): url for url in urls}
        results = {}
        for future in tqdm(futures.keys(), desc="等待结果", leave=False):
            try:
                result = future.result()
                url = futures[future]
                results[url] = result
            except Exception as e:
                print(f"Error processing {url}: {e}")
            pbar.update()  # 更新进度条
    return results


if __name__ == '__main__':

    """with open('F://example.txt', 'r') as file:
        url_list = [each.strip() for each in file.readlines()]  # 去除每行末尾的换行符"""

    url_list = [
        'https://www.baidu.com',
        'https://www.bing.com',
        'https://www.google.com'
    ]

    # 设置最大线程数，根据你的机器性能调整这个值
    threads = 1

    # 检查网站可访问性并打印结果
    accessibility_results = check_websites_accessibility_multithreaded(url_list, threads)

    # 打印结果
    for u, res in accessibility_results.items():
        if not res['accessible']:
            try:
                print(f"{u} 不可访问，错误信息：{res['error']}")
            except KeyError:
                print(f"{u} 不可访问，错误信息：{res['status_code']}")
        else:
            print(f"{u} 支持访问，状态信息：{res['status_code']}")
