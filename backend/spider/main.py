import concurrent.futures
from tb import get_price_from_tb
from jd import get_price_from_jd

# 比较价格的函数
def compare_prices(keyword):
    # 使用线程池并行运行两个获取价格的函数
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_jd = executor.submit(get_price_from_jd, keyword)
        future_tb = executor.submit(get_price_from_tb, keyword)

        # 获取结果
        jd_prices = future_jd.result()
        tb_prices = future_tb.result()

    # 打印京东价格
    print("京东价格：")
    for name, price in jd_prices[:10]:  # 只显示前5个结果
        print(f"{name} - ¥{price}")

    # 打印淘宝价格
    print("\n淘宝价格：")
    for name, price in tb_prices[:10]:  # 只显示前5个结果
        print(f"{name} - ¥{price}")

if __name__ == '__main__':
    # 使用示例
    keyword = "iPhone 14"
    compare_prices(keyword)
