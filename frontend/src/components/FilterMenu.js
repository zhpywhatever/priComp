import {
    Typography,
    Slider,
    FormControl,
    Select,
    MenuItem,
    Checkbox,
    FormControlLabel,
    Grid,
  } from '@material-ui/core';
  
  const FilterMenu = ({ filters, setFilters }) => {
    const handlePriceChange = (event, newValue) => {
      setFilters(prev => ({ ...prev, priceRange: newValue }));
    };
  
    const handleRatingChange = event => {
      setFilters(prev => ({ ...prev, rating: event.target.value }));
    };
  
    const handleBrandChange = event => {
      setFilters(prev => ({ ...prev, brand: event.target.value }));
    };
  
    const handleStockChange = event => {
      setFilters(prev => ({ ...prev, inStock: event.target.checked }));
    };
  
    return (
      <Grid container spacing={2} alignItems="center">
        {/* 价格范围 */}
        <Grid item>
          <Typography>价格范围</Typography>
          <Slider
            value={filters.priceRange}
            onChange={handlePriceChange}
            valueLabelDisplay="auto"
            min={0}
            max={5000}
            style={{ width: 200 }}
          />
        </Grid>
  
        {/* 评分 */}
        <Grid item>
          <Typography>评分</Typography>
          <FormControl>
            <Select value={filters.rating} onChange={handleRatingChange}>
              {[0, 1, 2, 3, 4, 5].map(rating => (
                <MenuItem key={rating} value={rating}>
                  {rating} 星以上
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
  
        {/* 品牌 */}
        <Grid item>
          <Typography>品牌</Typography>
          <FormControl>
            <Select
              value={filters.brand}
              onChange={handleBrandChange}
              displayEmpty
            >
              <MenuItem value="">全部</MenuItem>
              <MenuItem value="BrandA">BrandA</MenuItem>
              <MenuItem value="BrandB">BrandB</MenuItem>
            </Select>
          </FormControl>
        </Grid>
  
        {/* 仅显示有货 */}
        <Grid item>
          <FormControlLabel
            control={
              <Checkbox
                checked={filters.inStock}
                onChange={handleStockChange}
              />
            }
            label="仅显示有货"
          />
        </Grid>
      </Grid>
    );
  };
  
  export default FilterMenu;
  