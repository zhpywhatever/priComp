import concurrent.futures
from tb import get_price_from_tb
from jd import get_price_from_jd

# 比较价格的函数
def get_lowest(keyword):
    # 使用线程池并行运行两个获取价格的函数
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_jd = executor.submit(get_price_from_jd, keyword)
        future_tb = executor.submit(get_price_from_tb, keyword)

        # 获取结果
        jd_products = future_jd.result()
        tb_products = future_tb.result()

    # 打印京东价格
    print("京东价格：")
    lowest_in_jd = jd_products[0]
    lowest_in_tb = tb_products[0]
    for product in jd_products[:10]:  # 只显示前10个结果
        if product[1] < lowest_in_jd[1]:
            lowest_in_jd = product
        print(f"{product[0]} - ¥{product[1]}")

    # 打印淘宝价格
    print("\n淘宝价格：")
    for product in tb_products[:10]:  # 只显示前10个结果
        if product[1] < lowest_in_jd[1]:
            lowest_in_jd = product
        print(f"{product[0]} - ¥{product[1]}")

    return lowest_in_jd, lowest_in_tb

# get_product(keyword):



if __name__ == '__main__':
    # 使用示例
    keyword = "iPhone 14"
    get_lowest(f"'{keyword}'")
