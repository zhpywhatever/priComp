# 使用官方 Node.js 镜像
FROM node:22.12.0

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY package.json yarn.lock ./

# 设置 Yarn 的国内镜像（可以根据需要使用官方源）
RUN yarn config set registry https://registry.npmmirror.com

# 安装依赖
RUN yarn install

# 复制项目代码
COPY . .

# 构建前端项目
RUN yarn build



# 暴露前端默认端口
EXPOSE 3000

CMD ["yarn", "start"]
