# 使用官方 Python 镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /backend
# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


# 复制项目代码
COPY . .

# 暴露 FastAPI 运行端口
EXPOSE 8888

# 启动命令
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8888"]
