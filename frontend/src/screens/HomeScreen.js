import {
  Typography,
  makeStyles,
  Box,
  useScrollTrigger,
  Zoom,
  Fab,
} from '@material-ui/core';
import Meta from '../components/Meta';
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { listProducts } from '../actions/productActions';
import WhatshotIcon from '@material-ui/icons/Whatshot';
import Masonry from 'react-masonry-css';
import Product from '../components/Product';
import Message from '../components/Message';
import FilterMenu from '../components/FilterMenu';
import SkeletonArticle from '../skeletons/SkeletonArticle';
import SearchBox from '../components/SearchBox';
import KeyboardArrowUpIcon from '@material-ui/icons/KeyboardArrowUp';
import PaginationComponent from '../components/Pagination';
import ProductCarousel from './ProductCarousel';
import HeroSection from '../components/HeroSection';
import Pricing from '../components/Pricing';
import { motion } from 'framer-motion';
import axios from 'axios';
import { useHistory } from 'react-router-dom';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8888', // 设置基础 URL
  timeout: 10000,                    // 可选：请求超时时间
});

const useStyles = makeStyles(theme => {
  return {
    title: {
      margin: ' 0 0 1.5rem 0',
    },
    new: {
      display: 'flex',
      alignItems: 'center',
      marginBottom: '0.5rem',
    },
    root: {
      position: 'fixed',
      bottom: theme.spacing(2),
      right: theme.spacing(2),
    },
  };
});

function ScrollTop(props) {
  const { children, window } = props;
  const classes = useStyles();
  // Note that you normally won't need to set the window ref as useScrollTrigger
  // will default to window.
  // This is only being set here because the demo is in an iframe.
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

const HomeScreen = ({ match }) => {
  const history = useHistory();

  const pageNumber = match.params.pageNumber || 1;
  const dispatch = useDispatch();
  const productList = useSelector(state => state.productList);
  const { loading, error, allProducts, products, page, pages } = productList;
  const userLogin = useSelector(state => state.userLogin);
  const { userInfo } = userLogin;
  const [filters, setFilters] = useState({
    priceRange: [0, 1000],
    rating: 0,
    brand: '',
    inStock: false,
  });
  
  const [keyword, setKeyword] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false); // 是否在搜索状态
  const filteredProducts = allProducts?.filter(product => {
    const matchesPrice =
      product.price >= filters.priceRange[0] &&
      product.price <= filters.priceRange[1];
    const matchesRating = product.rating >= filters.rating;
    const matchesBrand = !filters.brand || product.brand === filters.brand;
    const matchesStock = !filters.inStock || product.countInStock > 0;
  
    return matchesPrice && matchesRating && matchesBrand && matchesStock;
  });
  

  

  const [clickedCategory, setClickedCategory] = React.useState('');

  useEffect(() => {
    console.log("clickedCategory",clickedCategory);
    console.log("allProducts:",allProducts)
  }, [clickedCategory]);
  const filteredCategoryProducts = allProducts?.filter(product =>
    product.category?.toLowerCase().includes(clickedCategory?.toLowerCase())
  );

  const onInputChange = e => {
    e.preventDefault();
    setKeyword(e.target.value?.toLowerCase());
  };

  useEffect(() => {
    dispatch(listProducts(pageNumber));
  }, [dispatch, pageNumber, userInfo]);

  const handleSearch = async (query) => {
    history.push('/search',{ key: keyword} )
  };

  const clearSearch = () => {
    setIsSearching(false); // 清除搜索状态
    setSearchResults([]);
    setKeyword('');
  };

  const classes = useStyles();
  const breakpoints = {
    default: 3,
    1100: 2,
    700: 1,
  };
  const animation = {
    hidden: {},
    visible: {
      transition: {
        staggerChildren: 0.15,
      },
    },
  };
  return (
    <>
      <Meta />
      {loading ? (
        <Typography variant="h2" component="h1" className={classes.title}>
          {[1, 2, 3, 4, 5]?.map(n => (
            <SkeletonArticle key={n}></SkeletonArticle>
          ))}
        </Typography>
      ) : error ? (
        <Message variant="error">{error}</Message>
      ) : (
        <>
          {/* <Glass /> */}
          {!clickedCategory && !keyword && <HeroSection userInfo={userInfo} />}

          <div id="back-to-top-anchor"></div>

          {!clickedCategory && !keyword && <ProductCarousel />}

          <SearchBox
            onChange={onInputChange}
            onSearch={handleSearch}
            keyword={keyword}
            clearSearch={clearSearch}
          />
          

            

          {!clickedCategory && !keyword && (
            <div className={classes.new}>
              <WhatshotIcon color="secondary" />
              <span style={{ fontWeight: 'bold', fontSize: '1.5rem' }}>
                {' '}
                商品上新
              </span>
            </div>
          )}

          {keyword && (
            <Box display="flex" flexDirection="column"  marginBottom="10px" marginRight="1rem">
            <FilterMenu filters={filters} setFilters={setFilters} />
          </Box>
          )}

          {/* //masonry-css */}
          <Masonry
            breakpointCols={breakpoints}
            className="my-masonry-grid"
            columnClassName="my-masonry-grid_column"
            id="scroll-to-main-product"
            component={motion.div}
            variants={animation}
            initial="hidden"
            animate="visible"
          >
            {clickedCategory
              ? filteredCategoryProducts?.map(product => (
                  <div key={product.id}>
                    <Product product={product} />
                  </div>
                ))
              : keyword
              ? filteredProducts?.map(product => (
                  <div key={product.id}>
                    <Product product={product} />
                  </div>
                ))
              : products?.map(product => (
                  <div key={product.id}>
                    <Product product={product} />
                  </div>
                ))}
          </Masonry>
          {!clickedCategory && !keyword && (
            <>
              <Box
                style={{
                  width: '100%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  marginTop: '2rem',
                }}
              >
                <PaginationComponent
                  style={{ width: '100%' }}
                  pages={pages}
                  page={page}
                />
              </Box>

              <Box
                style={{
                  width: '100%',
                  marginTop: '2rem',
                }}
              >
                <Pricing />
              </Box>
            </>
          )}
          <ScrollTop>
            <Fab color="secondary" size="small" aria-label="scroll back to top">
              <KeyboardArrowUpIcon />
            </Fab>
          </ScrollTop>
        </>
      )}
    </>
  );
};

export default HomeScreen;
