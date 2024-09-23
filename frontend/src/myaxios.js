import axios from 'axios';

// 设置 baseURL 为 localhost:8888
const axiosInstance = axios.create({
    baseURL: 'http://localhost:8888', // 设置请求的基础 URL
    timeout: 10000,                    // 可选：设置请求超时时间
});

// 使用配置好的 axios 实例发送请求
const { data } = await axiosInstance.get('/api/admin/users', config);

// 处理返回的数据
console.log(data);
