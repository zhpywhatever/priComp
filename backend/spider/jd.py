import time
import json
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re

# 初始化 Chrome 浏览器
def init_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # 如果不需要界面，可以使用 headless 模式
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# 保存登录 Cookie 到本地文件
def save_cookies(driver, filename="jd_cookies.json"):
    cookies = driver.get_cookies()
    with open(filename, "w") as f:
        json.dump(cookies, f)

# 从文件加载 Cookie
def load_cookies(driver, filename="jd_cookies.json"):
    with open(filename, "r") as f:
        cookies = json.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)

# 京东登录和保存 Cookie
def login_and_save_cookies():
    driver = init_browser()
    driver.get("https://passport.jd.com/new/login.aspx")
    print("请手动登录京东账户...")
    time.sleep(30)  # 给用户足够时间手动登录

    save_cookies(driver)
    print("登录成功，Cookie 已保存。")
    driver.quit()

# 使用保存的 Cookie 自动登录并进行商品查询
def search_product(keyword):
    driver = init_browser()
    driver.get("https://www.jd.com/")

    # 加载已保存的 Cookie
    load_cookies(driver)
    driver.refresh()  # 刷新页面以应用 Cookie

    try:
        # 搜索商品
        search_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "key"))
        )
        # search_box = driver.find_element(By.ID, "J_searchbg")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)  # 使用回车键来触发搜索
        # search_box.submit()
    except Exception as e:
        print("搜索框不可交互:", e)
        driver.quit()
        return
    time.sleep(5)  # 等待页面加载

    # 抓取商品名称和价格
    product_elements = driver.find_elements(By.XPATH, '//*[@id="J_goodsList"]/ul/li')
    results = []
    for product in product_elements[:10]:  # 获取前10个商品
        try:
            title = product.find_element(By.CSS_SELECTOR, "div.p-name em").text
            price_text = product.find_element(By.CSS_SELECTOR, "div.p-price strong i").text
            price = float(price_text.replace(',', ''))
            results.append((title, price))
        except Exception as e:
            print("解析商品信息时出错:", e)

    # 打印结果
    # print("京东上的商品价格：")
    # for title, price in results:
    #     print(f"{title} - ¥{price}")

    driver.quit()
    return results

# 程序主入口
# if __name__ == "__main__":


def get_price_from_jd(keyword):
    import os
    # 判断 Cookie 文件是否存在
    if not os.path.exists("jd_cookies.json"):
        login_and_save_cookies()  # 首次运行时手动登录并保存 Cookie

    return search_product(keyword)