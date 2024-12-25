import time
import json
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from spider.webdriver_manage_extend_tb import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
import urllib.parse
from urllib.parse import quote

def init_browser():
    # global driver
    # if not driver:
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # 如果不需要界面，可以使用 headless 模式
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()

    driver.set_page_load_timeout(300)
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"
    # chrome_options = Options()
    # chrome_options.page_load_strategy = 'eager'
    # driver = webdriver.Chrome(options=chrome_options)
    return driver


# 保存登录 Cookie 到本地文件
def save_cookies(driver, filename="taobao_cookies.json"):
    cookies = driver.get_cookies()
    with open(filename, "w") as f:
        json.dump(cookies, f)

# 从文件加载 Cookie
def load_cookies(driver, filename="taobao_cookies.json"):
    with open(filename, "r") as f:
        cookies = json.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)

# 淘宝登录和保存 Cookie
def login_and_save_cookies():
    driver = init_browser()

    driver.get("https://login.taobao.com/")
    print("请手动登录淘宝账户...")
    time.sleep(30)  # 给用户足够时间手动登录

    save_cookies(driver)
    print("登录成功，Cookie 已保存。")
    # driver.quit()

def extract_first_float(data):
    # 按照 '\n' 分割字符串
    elements = data.split('\n')
    for element in elements:
        # 检查元素是否只由数字和 '.' 组成
        if element.replace('.', '', 1).isdigit():  # 允许一个小数点
            return float(element)
    return None  # 如果未找到返回 None

# 使用保存的 Cookie 自动登录并进行商品查询
def search_product(keyword):
    driver = init_browser()
    encoded_keyword = quote(keyword)
    search_url = f"https://s.taobao.com/search?page=1&q={encoded_keyword}&tab=all"
    driver.get(search_url)

    # 加载已保存的 Cookie
    load_cookies(driver)
    driver.refresh()  # 刷新页面以应用 Cookie
    time.sleep(1)  # 等待页面加载

    login_symbol = driver.find_elements(By.CLASS_NAME, 'site-nav-login-info-nick')
    while len(login_symbol) == 0:
        login_and_save_cookies()
        login_symbol = driver.find_elements(By.CLASS_NAME, 'site-nav-login-info-nick')


    time.sleep(3)
    # 抓取商品名称和价格
    driver.execute_script('window.scrollTo(0,1000)')  # 横坐标不变，纵坐标 滚动到1000像素点
    time.sleep(2)  # 等待一段时间，方便查看滚动的效果
    product_elements = driver.find_elements(By.XPATH, '//*[@id="content_items_wrapper"]/div[*]')
    results = []
    for product in product_elements[:10]:  # 获取前10个商品
        try:
            text = product.text
            title = text.split('\n')[0]
            price_match = re.search(r'¥\n([\d.]+)', text)
            price = float(price_match.group(1)) if price_match else  extract_first_float(text)
            url = product.find_element(By.XPATH, './a').get_attribute('href')
            id_str = product.find_element(By.XPATH, './a').get_attribute('id').replace("item_id_", "")
            if id_str:
                id = int(id_str)
            img = product.find_element(By.XPATH, './a/div/div/div/img').get_attribute('src')
            if(img != None):
                results.append((title, price, url, img, id))
                print(f"{title} - ¥{price}")
        except Exception as e:
            print("解析商品信息时出错:", e)

    # 打印结果
    # print("淘宝上的商品价格：")
    # for title, price in results:
    #     print(f"{title} - ¥{price}")

    driver.quit()
    return results

# 程序主入口
# if __name__ == "__main__":


def get_price_from_tb(keyword):
    import os
    # 判断 Cookie 文件是否存在
    if not os.path.exists("taobao_cookies.json"):
        login_and_save_cookies()  # 首次运行时手动登录并保存 Cookie

    return search_product(keyword)

if __name__ == "__main__":
    keyword = "iPhone 14"
    results = get_price_from_tb(keyword)
    print("淘宝价格：")
    for name, price in results[:10]:  # 只显示前10个结果
        print(f"{name} - ¥{price}")