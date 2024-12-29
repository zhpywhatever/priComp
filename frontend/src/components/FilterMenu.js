import {
    Typography,
    Slider,
    FormControl,
    Select,
    MenuItem,
    Checkbox,
    FormControlLabel,
    Grid,
    Box,
    TextField,
  } from '@material-ui/core';
  
  const FilterMenu = ({ filters, setFilters }) => {
    const handlePriceChange = (event, newValue) => {
      setFilters(prev => ({ ...prev, priceRange: newValue }));
    };
  
    const handleRatingChange = event => {
      setFilters(prev => ({ ...prev, rating: event.target.value }));
    };
  
    const handlePlatformChange = event => {
      setFilters(prev => ({ ...prev, platform: event.target.value }));
    };
  
    const handleStockChange = event => {
      setFilters(prev => ({ ...prev, inStock: event.target.checked }));
    };

    const handlePriceInputChange = (e, type) => {
      const value = parseInt(e.target.value, 10) || 0; // 确保值为数字
      setFilters((prevFilters) => {
        const newPriceRange = [...prevFilters.priceRange];
        if (type === 'min') {
          newPriceRange[0] = value; // 更新最低价格
        } else if (type === 'max') {
          newPriceRange[1] = value; // 更新最高价格
        }
        return {
          ...prevFilters,
          priceRange: newPriceRange,
        };
      });
    };
    
  
    return (
      <Grid container spacing={10} alignItems="center" direction="row">
        {/* 价格范围 */}
        <Grid item>
          <Box display="flex" alignItems="center">
            <Typography style={{ marginRight: 8 }}>价格范围:</Typography>
            {/* 最低价格输入框 */}
            <TextField
              label="最低价格"
              type="number"
              value={filters.priceRange[0]}
              onChange={(e) => handlePriceInputChange(e, 'min')}
              variant="outlined"
              size="small"
              style={{ width: 100, marginRight: 8 }}
            />
            <Typography>-</Typography>
            {/* 最高价格输入框 */}
            <TextField
              label="最高价格"
              type="number"
              value={filters.priceRange[1]}
              onChange={(e) => handlePriceInputChange(e, 'max')}
              variant="outlined"
              size="small"
              style={{ width: 100, marginLeft: 8 }}
            />
          </Box>
        </Grid>
    
        {/* 评分 */}
        <Grid item>
          <Box display="flex" alignItems="center">
            <Typography style={{ marginRight: 8 }}>评分:</Typography>
            <FormControl size="small">
              <Select value={filters.rating} onChange={handleRatingChange}>
                {[0, 1, 2, 3, 4, 5].map((rating) => (
                  <MenuItem key={rating} value={rating}>
                    {rating} 星以上
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>
        </Grid>
    
        {/* 品牌 */}
        <Grid item>
          <Box display="flex" alignItems="center">
            <Typography style={{ marginRight: 8 }}>平台:</Typography>
            <FormControl size="small">
              <Select
                value={filters.platform}
                onChange={handlePlatformChange}
                displayEmpty
              >
                <MenuItem value="">全部</MenuItem>
                <MenuItem value="jd">京东</MenuItem>
                <MenuItem value="tb">淘宝</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </Grid>
    
        {/* 仅显示有货 */}
        <Grid item>
          <Box display="flex" alignItems="center">
            <FormControlLabel
              control={
                <Checkbox
                  checked={filters.inStock}
                  onChange={handleStockChange}
                />
              }
              label="仅显示有货"
            />
          </Box>
        </Grid>
      </Grid>
    );
    
    
  };
  
  export default FilterMenu;
  