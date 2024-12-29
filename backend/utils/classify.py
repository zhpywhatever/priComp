from transformers import pipeline
def classify(keyword):
    # 使用 Hugging Face 提供的预训练模型（例如，facebook/bart-large-mnli）
    classifier = pipeline('zero-shot-classification', model='./model')

    # 商品描述
    description = "这款蓝牙耳机音质极佳，适合运动和日常使用"

    candidate_labels = [
        '电子',  # 电子产品
        '家居',  # 家居用品
        '运动',  # 运动用品
        '衣物',  # 衣物
        '食品',  # 食品
        '化妆品',  # 化妆品和护肤品
        '玩具',  # 玩具
        '书籍',  # 书籍
        '家具',  # 家具
        '家电',  # 家用电器
        '汽车配件',  # 汽车配件
        '音乐',  # 音乐与音响
        '宠物用品',  # 宠物用品
        '母婴',  # 母婴用品
        '健康',  # 健康与个人护理
        '办公用品',  # 办公用品
        '工具',  # 工具与设备
        '户外',  # 户外用品
        '珠宝',  # 珠宝饰品
        '旅行',  # 旅行用品
        '艺术品',  # 艺术品
        '手表',  # 手表与配饰
        '食品饮料',  # 饮料和小食品
        '手机',  # 手机
        '计算机',  # 计算机与配件
        '美容',  # 美容产品
        '鞋类',  # 鞋类
        '健身器材',  # 健身器材
        '科技',  # 科技产品
    ]

    # 进行分类
    result = classifier(description, candidate_labels)

    # 打印预测结果
    return(result['labels'][0])
