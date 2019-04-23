# coding:utf-8
# @Time : 2019-04-23 11:02 
# @Author : Andy.Zhang
# @Desc : A sample for high-concurrency in python3

from gevent.pool import Pool
import urllib.request
from gevent import monkey
monkey.patch_all()


visiting_times = 0


def run_task(url):
    global visiting_times
    visiting_times += 1
    print("Visiting times: %s，url:%s" % (visiting_times, url))
    try:
        response = urllib.request.urlopen(url)
        url_data = response.read()
        print("%d bytes received from %s" % (len(url_data), url))
    except Exception as e:
        print(e)

    return("%s read finished.." % url)


if __name__ == "__main__":
    url = "http://httpbin.org/"  # 默认指定抓取的url
    visit_times = 3  # 指定共抓取多少次，默认为3
    concurrency_pools = 2  # 指定并发任务数量，默认为2

    urls = [url for i in range(visit_times)]
    pool = Pool(concurrency_pools)
    results = pool.map(run_task, urls)  # 等待所有抓取任务完成后返回
    print(results)


