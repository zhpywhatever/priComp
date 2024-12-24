import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import axios from 'axios';
import { Button } from '@material-ui/core';
// 注册 Chart.js 模块
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const PriceHistoryChart = ({ productId }) => {
  const [priceData, setPriceData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isVisible, setIsVisible] = useState(false);  // 控制图表显示与隐藏

  // 获取历史价格数据
  useEffect(() => {
    const fetchPriceHistory = async () => {
      try {
        const response = await axios.get(`/api/products/${productId}/price-history`);
        console.log("response.data:",response.data)
        setPriceData(JSON.parse(response.data)); // 假设返回的数据结构是 [{ price: 100, timestamp: "2023-01-01" }, ...]
      } catch (error) {
        console.error("Error fetching price history", error);
      } finally {
        setLoading(false);
      }
    };

    fetchPriceHistory();
  }, [productId]);

  // 格式化数据供 Chart.js 使用
  const getChartData = () => {
    console.log("priceData:",priceData)
    const labels = priceData?.map(item => item.timestamp); // 提取时间戳作为标签
    const prices = priceData?.map(item => item.price); // 提取价格作为数据

    return {
      labels,
      datasets: [
        {
          label: '价格历史',
          data: prices,
          fill: false,
          borderColor: 'rgba(75,192,192,1)',
          tension: 0.1,
        },
      ],
    };
  };

  // Chart.js 配置项
  const options = {
    responsive: true,
    plugins: {
      title: {
        display: false, // 禁用标题
      },
      legend: {
        display: false, // 禁用图例
      },
      tooltip: {
        callbacks: {
          label: (tooltipItem) => `价格: ${tooltipItem.raw} 元`, // 自定义 Tooltip 样式
        },
      },
    },
    scales: {
      x: {
        type: 'category',
        labels: priceData?.map(item => item.timestamp), // 确保标签正确显示
        ticks: {
          autoSkip: true, // 自动跳过重复的标签
          maxRotation: 45, // 如果标签过多，旋转标签
          minRotation: 30, // 最小旋转角度
        },
      },
      y: {
        beginAtZero: true,
        ticks: {
          callback: (value) => `${value} 元`, // 自定义 Y 轴标签格式
        },
      },
    },
  };

  return (
    <div>
      <Button onClick={() => setIsVisible(!isVisible)} style={{ backgroundColor: 'rgb(32, 150, 243)',color:'white',marginTop:'20px' }}>
        {isVisible ? '隐藏历史价格' : '显示历史价格'}
      </Button>
      <Button onClick={() => setIsVisible(!isVisible)} style={{ backgroundColor: 'rgb(32, 150, 243)',color:'white',marginTop:'20px', marginLeft:"20px" }}>
        更新当前价格
      </Button>

      {loading ? (
        <p>加载中...</p>
      ) : (
        <div>
          {isVisible && (
            <div >  {/* 调整图表高度 */}
              <h3>商品历史价格</h3>
              <Line data={getChartData()} options={options}  /> {/* 设置图表高度 */}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default PriceHistoryChart;
