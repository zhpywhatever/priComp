from transformers import pipeline
def classify(keyword):
    # 使用 Hugging Face 提供的预训练模型（例如，facebook/bart-large-mnli）
    classifier = pipeline('zero-shot-classification', model='./utils/model')

    # 商品描述
    description = keyword

    candidate_labels = [
        '电子',  # 电子产品
        '家居',  # 家居用品
        '运动',  # 运动用品
        '衣物',  # 衣物
        '食品',  # 食品
    ]

    # 进行分类
    result = classifier(description, candidate_labels)

    # 打印预测结果
    return(result['labels'][0])

if __name__ == '__main__':
    print(classify("苏泊尔保温杯大容量水杯2024新款杯子316L不锈钢焖茶杯随行杯男款"))