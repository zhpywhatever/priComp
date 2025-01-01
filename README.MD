### 项目简介

#### 项目名称：`Pricomp`

`Pricomp` 是一个旨在帮助用户进行价格比较的系统，提供一个集中平台，用户可以在此平台上进行多种商品的价格对比。该系统通过集成后端服务与前端用户界面，使用户能够快速获取不同商家的价格信息，同时也能查看商品的详细信息。平台支持前端交互、动态数据加载及后端计算，力求为用户提供直观、便捷的购物体验。

项目包括前端（基于 React）、后端（基于 Node.js 和 Express）、数据库（Sqlite）等多个模块，采用微服务架构进行开发。整个系统通过 Docker 容器化，确保了各个服务的独立性与便捷的部署流程。

------

### 文档介绍

#### 1. **项目架构**

项目采用前后端分离的架构模式。主要组件包括：

- **前端**：前端使用 React 框架开发，提供响应式用户界面，支持各种设备访问。通过 Axios 与后端进行数据交互。
- **后端**：后端基于 FastAPI 开发，提供 API 供前端调用。使用 Sqlite 数据库存储商品与价格信息。
- **数据库**：使用 Sqlite 存储商品信息和价格数据。商品信息包括商品的描述、图片、价格、商家等信息。
- **容器化**：前端与后端服务都通过 Docker 容器化，保证了开发环境与生产环境的一致性。通过 Docker Compose 进行容器管理，方便部署与管理。

------

#### 2. **技术栈**

- **前端**：React, Axios, Webpack, Yarn
- **后端**：FastAPI, Sqlite
- **容器化**：Docker, Docker Compose
- **开发工具**：VS Code, Git, Postman

------

#### 3. **主要功能**

- **商品价格比较**：用户可以查看不同商家的同一商品价格，支持多条件筛选。

![image-20250101171512669](C:\Users\ZHPY\AppData\Roaming\Typora\typora-user-images\image-20250101171512669.png)

- **动态数据加载**：前端通过异步请求获取最新的商品数据，展示在用户界面。

![image-20250101171533947](C:\Users\ZHPY\AppData\Roaming\Typora\typora-user-images\image-20250101171533947.png)

- **商品信息展示**：用户可以查看商品的详细信息，包括描述、价格、商家等。

![image-20250101171632572](C:\Users\ZHPY\AppData\Roaming\Typora\typora-user-images\image-20250101171632572.png)

![image-20250101171726819](C:\Users\ZHPY\AppData\Roaming\Typora\typora-user-images\image-20250101171726819.png)

- **用户反馈**：用户可以对商品和商家进行评价，帮助其他用户做出选择。

  ![image-20250101171646816](C:\Users\ZHPY\AppData\Roaming\Typora\typora-user-images\image-20250101171646816.png)

------

#### 4. **部署与运行**

项目通过 Docker 容器化部署，使用 Docker Compose 进行前端与后端服务的管理。具体步骤如下：

1. **安装 Docker 和 Docker Compose**：确保本地环境已安装 Docker 和 Docker Compose。

2. 构建 Docker 镜像：运行以下命令构建前端和后端的 Docker 镜像。

   ```bash
   docker build -t pricomp-frontend ./frontend
   docker build -t pricomp-backend ./backend
   ```

3. 启动服务：运行以下命令启动前后端服务。

   ```bash
   docker-compose up
   ```

4. **访问应用**：服务启动后，可以通过浏览器访问 `http://localhost:3000` 查看前端页面，后端 API 监听 `http://localhost:5000`。

5. 备用运行方案：

​	运行根目录下的`run.sh`以非docker的方式运行

```bash
./run.sh
```

------

#### 5. **开发与贡献**

- 克隆项目：

  ```bash
  git clone <git@github.com:zhpywhatever/priComp.git>
  ```

- **安装依赖**：在前端和后端目录中运行 `yarn install` 来安装依赖。

- **本地开发**：在开发时，可以分别启动前端与后端服务，进行开发与调试。

------

### 结语

`Pricomp` 项目力求为用户提供一个便捷的商品价格对比平台，帮助用户做出更明智的购物决策。通过前后端分离的架构，灵活的微服务管理，以及容器化技术，确保了系统的高效与可维护性。随着项目的进一步发展，未来还可以加入更多功能，如价格提醒、用户推荐等。