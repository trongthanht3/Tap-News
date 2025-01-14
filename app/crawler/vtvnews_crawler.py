from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import sys
from common.queue_client import QueueClient

sys.path.append('../')
from utils import convert_not_timestamp, scroll_page, news_to_json, get_driver

driver = get_driver()



def vtvnews_crawler(articles_queue:QueueClient):
    num_of_page=2
    url = "https://vtv.vn/kinh-te/bat-dong-san.htm"
    driver.get(url)
    wait = WebDriverWait(driver, 3)

    # Handle infinitive load
    for i in range(int(num_of_page)*2):
        driver.execute_script("""$('div[class="loadmore"] a[rel="nofollow"]').click()""")
        time.sleep(2)

    # Loading to end to prevent error
    for i in range(5):
        scroll_page(driver)

    # crawling
    top_articles = driver.find_elements(By.XPATH, '//div[@class="focus_left equalheight"]')
    raw_articles = top_articles + driver.find_elements(By.CLASS_NAME, 'tlitem')
    print("Fetching VTVNews: {} news.".format(len(raw_articles)))
    for article in raw_articles[:-1]:
        try:
            title = article.find_element(By.XPATH, './/a').get_attribute('title')
            description = article.find_element(By.XPATH, './/p[@class="sapo"]').text
            url = article.find_element(By.XPATH, './/a').get_attribute('href')
            urlToImage = article.find_element(By.XPATH, './/a//img').get_attribute('src')
            publishedAt = ''
            try:
                publishedAt = article.find_element(By.XPATH, './/div//p[@class="icon_clock"]').text
            except:
                publishedAt = article.find_elements(By.XPATH, './/p[@class="time"]//span')[1].get_attribute('title')
            publishedAt = convert_not_timestamp(publishedAt)
            # parse to json
            new_article_format = news_to_json("VTVNews", title, description, url,
                                              urlToImage, publishedAt,
                                              description, "vtv.vn", "VTV.vn")
            articles_queue.sendMessage(new_article_format)
        except:
            pass
    driver.execute_script("window.close()")