import axios from 'axios';
import {
  PRODUCT_LIST_REQUEST,
  PRODUCT_LIST_SUCCESS,
  PRODUCT_LIST_FAIL,
  PRODUCT_DETAILS_REQUEST,
  PRODUCT_DETAILS_SUCCESS,
  PRODUCT_DETAILS_FAIL,
  PRODUCT_CREATE_REVIEW_REQUEST,
  PRODUCT_CREATE_REVIEW_SUCCESS,
  PRODUCT_CREATE_REVIEW_FAIL,
  PRODUCT_TOP_REQUEST,
  PRODUCT_TOP_SUCCESS,
  PRODUCT_TOP_FAIL,
  PRODUCT_RELATED_REQUEST,
  PRODUCT_RELATED_SUCCESS,
  PRODUCT_RELATED_FAIL,
} from '../constants/productConstants';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8888', // 设置基础 URL
  timeout: 10000,                    // 可选：请求超时时间
});

export const listProducts =
  (pageNumber = '') =>
  async dispatch => {
    // console.log("111")
    try {
      dispatch({ type: PRODUCT_LIST_REQUEST });

      // setTimeout(async () => {
      //   const { data } = await axios.get('/api/products');

      //   dispatch({ type: PRODUCT_LIST_SUCCESS, payload: data });
      // }, 3000);
      // console.log("get products success0")
      const { data } = await axiosInstance.get(
        `/api/products?pageNumber=${pageNumber}`
      );
      console.log("get products success1")

      dispatch({ type: PRODUCT_LIST_SUCCESS, payload: data.products });
      // console.log("get products success2")
    } catch (error) {
      // console.log("get products failed1")
      dispatch({
        type: PRODUCT_LIST_FAIL,
        payload:
          error.response && error.response.data.message
            ? error.response.data.message
            : error.message,
      });
      // console.log("get products failed2")
    }
  };
export const listProductDetails = id => async dispatch => {
  try {
    dispatch({ type: PRODUCT_DETAILS_REQUEST });
    // setTimeout(async () => {
    //   const { data } = await axiosInstance.get('/api/products');

    //   dispatch({ type: PRODUCT_DETAIL_SUCCESS, payload: data });
    // }, 3000);
    console.log("id:",id)
    let { data } = await axiosInstance.get(`/api/products/${id}`);
    dispatch({ type: PRODUCT_DETAILS_SUCCESS, payload: data });
  } catch (error) {
    dispatch({
      type: PRODUCT_DETAILS_FAIL,
      payload:
        error.response && error.response.data.message
          ? error.response.data.message
          : error.message,
    });
  }
};
export const createProductReview =
  (productId, review) => async (dispatch, getState) => {
    try {
      dispatch({
        type: PRODUCT_CREATE_REVIEW_REQUEST,
      });
      const {
        userLogin: { userInfo },
      } = getState();
      const config = {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${userInfo.token}`,
        },
      };
      await axiosInstance.post(`/api/products/${productId}/reviews`, review, config);
      dispatch({
        type: PRODUCT_CREATE_REVIEW_SUCCESS,
      });
    } catch (error) {
      dispatch({
        type: PRODUCT_CREATE_REVIEW_FAIL,
        payload:
          error.response && error.response.data.message
            ? error.response.data.message
            : error.message,
      });
    }
  };
export const listTopProducts = () => async dispatch => {
  try {
    dispatch({ type: PRODUCT_TOP_REQUEST });

    const { data } = await axiosInstance.get(`/api/products/top`);

    dispatch({
      type: PRODUCT_TOP_SUCCESS,
      payload: data,
    });
    console.log("get top success")
  } catch (error) {
    dispatch({
      type: PRODUCT_TOP_FAIL,
      payload:
        error.response && error.response.data.message
          ? error.response.data.message
          : error.message,
    });
  }
};
export const listRelatedProducts = id => async dispatch => {
  try {
    dispatch({ type: PRODUCT_RELATED_REQUEST });

    let { data } = await axiosInstance.get(`/api/products/${id}/related`);
    dispatch({ type: PRODUCT_RELATED_SUCCESS, payload: data });
  } catch (error) {
    dispatch({
      type: PRODUCT_RELATED_FAIL,
      payload:
        error.response && error.response.data.message
          ? error.response.data.message
          : error.message,
    });
  }
};
