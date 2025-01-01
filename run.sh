#!/bin/bash

# 安装前端依赖并启动前端
echo "安装前端依赖..."
cd ./frontend

# 使用 Yarn 安装前端依赖
yarn install --registry https://registry.npmmirror.com

# 构建前端项目
yarn build

# 启动前端开发服务器
echo "启动前端开发服务器..."
yarn start &

# 获取前端启动的进程ID
frontend_pid=$!

# 安装后端依赖并启动后端
echo "安装后端依赖..."
cd ../backend

# 使用 pip 安装后端依赖
pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 启动后端服务
echo "启动后端 FastAPI 服务..."
uvicorn server:app --host 0.0.0.0 --port 8888 &

# 获取后端启动的进程ID
backend_pid=$!

# 打印进程信息
echo "前端服务正在运行，访问地址: http://localhost:3000"
echo "后端服务正在运行，访问地址: http://localhost:8888"

# 等待前后端服务的结束
wait $frontend_pid
wait $backend_pid
