from . import batdongsan_crawler
from . import hanoimoi_crawler
from . import thanhnien_crawler
from . import vietnamnet_crawler
from . import laodong_crawler
from . import vtvnews_crawler
from . import vnexpress_crawler
import sys
import threading

sys.path.append('./')

from common.queue_client import QueueClient

CRAWLER_NEWS_TASK_QUEUE_NAME = 'crawler-news-task-queue'

articles_queue = QueueClient(CRAWLER_NEWS_TASK_QUEUE_NAME)

list_task = [vnexpress_crawler.vnexpress_crawler_api,
             vtvnews_crawler.vtvnews_crawler,
             laodong_crawler.laodong_crawler,
             vietnamnet_crawler.vietnamnet_crawler,
             thanhnien_crawler.thanhnien_crawler,
             hanoimoi_crawler.hanoimoi_crawler,
             batdongsan_crawler.batdongsan_thitruong_crawler,
             batdongsan_crawler.batdongsan_phantich_crawler,
             batdongsan_crawler.batdongsan_chinhsach_crawler,
             batdongsan_crawler.batdongsan_quyhoach_crawler,
             batdongsan_crawler.batdongsan_thegioi_crawler
             ]


def start_crawler():
    for task in list_task:
        print("Start task crawler {}...........".format(task.__name__))
        try:
            task(articles_queue)
        except Exception as e:
            print("Error task {}: {}".format(task.__name__, e.__str__()))
        # threading.Thread(target=task,args=(articles_queue,)).start()


def get_news_from_crawler():
    articles = articles_queue.get_all_message()
    if len(articles) > 0:
        print("Get {} news from crawler...........".format(len(articles)))
    return articles


start_crawler()
