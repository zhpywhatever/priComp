import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  Typography,
  Box,
  Fab,
  Zoom,
  makeStyles,
  useScrollTrigger,
} from '@material-ui/core';
import Meta from '../components/Meta';
import FilterMenu from '../components/FilterMenu';
import SearchBox from '../components/SearchBox';
import Message from '../components/Message';
import Product from '../components/Product';
import Masonry from 'react-masonry-css';
import SkeletonArticle from '../skeletons/SkeletonArticle';
import KeyboardArrowUpIcon from '@material-ui/icons/KeyboardArrowUp';
import axios from 'axios';
import { Pagination } from '@mui/material';


const axiosInstance = axios.create({
  baseURL: 'http://localhost:8888',
  timeout: 10000,
});

const useStyles = makeStyles(theme => ({
  title: {
    margin: '0 0 1.5rem 0',
  },
  root: {
    position: 'fixed',
    bottom: theme.spacing(2),
    right: theme.spacing(2),
  },
}));

function ScrollTop(props) {
  const { children, window } = props;
  const classes = useStyles();
  const trigger = useScrollTrigger({
    target: window ? window() : undefined,
    disableHysteresis: true,
    threshold: 150,
  });

  const handleClick = event => {
    const anchor = (event.target.ownerDocument || document).querySelector(
      '#back-to-top-anchor'
    );
    if (anchor) {
      anchor.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  };

  return (
    <Zoom in={trigger}>
      <div onClick={handleClick} role="presentation" className={classes.root}>
        {children}
      </div>
    </Zoom>
  );
}

const SearchScreen = () => {
  const classes = useStyles();
  const [keyword, setKeyword] = useState('');
  const [filters, setFilters] = useState({
    priceRange: [0, 1000],
    rating: 0,
    platform: '',
    inStock: false,
  });
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

// 新增状态管理
const [page, setPage] = useState(1);  // 当前页
const [pageSize, setPageSize] = useState(9);  // 每页显示数量
const [totalPages, setTotalPages] = useState(1);  // 总页数（从后端获取）
const [refresh, setRefresh] = useState(1);  // 总页数（从后端获取）
  
  const fetchFilteredProducts = async () => {
    setLoading(true);
    setError(null);
    try {
      const params = {
        keyword,
        rating: filters.rating,
        platform: filters.platform,
        inStock: filters.inStock,
        page: page, // 默认分页参数，可以根据需要动态设置
      page_size: pageSize, // 默认分页大小
      };
      const priceRangeParams = filters.priceRange.map(value => `priceRange=${value}`).join('&');

      const { data } = await axiosInstance.get(`/api/products?${priceRangeParams}`, { params });
      setProducts(data.products);  // 这里假设 API 返回的数据有 products 数组
    setTotalPages(data.total_pages);  // 假设 API 返回总页数
    let searchData = JSON.stringify(keyword);
    sessionStorage.setItem("searchData",searchData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSpider = async () => {
    const axiosInstance = axios.create({
      baseURL: 'http://localhost:8888',
      timeout: 100000,
    });
    setLoading(true);
    setError(null);
    try {
      const { res } = await axiosInstance.get(`/api/spider/get-products/${keyword}`);
      const params = {
        keyword,
        rating: filters.rating,
        platform: filters.platform,
        inStock: filters.inStock,
        page: page, // 默认分页参数，可以根据需要动态设置
      page_size: pageSize, // 默认分页大小
      };
      const priceRangeParams = filters.priceRange.map(value => `priceRange=${value}`).join('&');

      const { data } = await axiosInstance.get(`/api/products?${priceRangeParams}`, { params });
      setPage(1);  // 重置页码
      setTotalPages(data.total_pages);  // 假设 API 返回总页数
      setProducts(data.products);  // 这里假设 API 返回的数据有 products 数组
      // 9090window.location.reload();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // 使用 useEffect 来触发 fetch 操作
useEffect(() => {
  window.scrollTo(0, 0);  // 每次进入页面时滚动到顶部
  let searchData = JSON.parse(sessionStorage.getItem('searchData'));
    if(searchData){
      // console.log(searchData);
      //直接setFieldsValue()可以把值赋值到表单里面
      setKeyword(searchData);
      setRefresh(searchData);
      //setFilters(prev => ({ ...prev, keyword: searchData }));
      //完了之后记得把本地的数据清除掉
      //sessionStorage.removeItem("searchData");
      fetchFilteredProducts();
    }

  fetchFilteredProducts();
  
}, [filters, page, pageSize,refresh]);  // 每次 filters、page 或 pageSize 变动时重新请求数据

  const handleFilterChange = newFilters => {
    setFilters(prevFilters => ({ ...prevFilters, ...newFilters }));
  };

  const handleSearchChange = e => {
    setKeyword(e.target.value);
  };

  const breakpoints = {
    default: 3,
    1100: 2,
    700: 1,
  };

  return (
    <>
      <Meta />
      <div id="back-to-top-anchor"></div>
      <SearchBox value={keyword} onChange={handleSearchChange} onSearch={fetchFilteredProducts} onSpider={handleSpider}/>
      <Box display="flex" flexDirection="column" marginBottom="10px" marginRight="1rem">
        <FilterMenu filters={filters} onChange={handleFilterChange} setFilters={setFilters}/>
      </Box>
      {loading ? (
        <Typography variant="h2" component="h1" className={classes.title}>
          {[1, 2, 3, 4, 5]?.map(n => (
            <SkeletonArticle key={n}></SkeletonArticle>
          ))}
        </Typography>
      ) : error ? (
        <Message variant="error">{error}</Message>
      ) : (
        <Masonry
          breakpointCols={breakpoints}
          className="my-masonry-grid"
          columnClassName="my-masonry-grid_column"
        >
          {products?.map(product => (
            <div key={product.id}>
              <Product product={product} />
            </div>
          ))}
        </Masonry>
      )}

      {/* 分页组件 */}
    <Pagination
      count={totalPages}  // 总页数
      page={page}  // 当前页
      onChange={(_, value) => setPage(value)}  // 更新当前页
      color="primary"
      shape="rounded"
      variant="outlined"
      size="large"
    />

      <ScrollTop>
        <Fab color="secondary" size="small" aria-label="scroll back to top">
          <KeyboardArrowUpIcon />
        </Fab>
      </ScrollTop>
    </>
  );
};

export default SearchScreen;
