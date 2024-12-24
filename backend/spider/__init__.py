from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
driver = None
# 初始化 Chrome 浏览器
def init_browser():
    global driver
    if not driver:
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")  # 如果不需要界面，可以使用 headless 模式
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.page_load_strategy = 'eager'
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.set_page_load_timeout(300)
        desired_capabilities = DesiredCapabilities.CHROME
        desired_capabilities["pageLoadStrategy"] = "none"
    return driver