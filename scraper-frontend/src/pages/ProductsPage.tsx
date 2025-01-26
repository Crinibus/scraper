import { Stack, Typography } from "@mui/material";
import { ProductList } from "../components/ProductList";
import { products } from "../test-data/products-data";

export type ProductInfo = {
  id: string;
  name: string;
  category: string;
  domain: string;
  currency: string;
  isActive: boolean;
};

export const ProductsPage = () => {
  // TODO: Get product data from API

  return (
    <>
      <Stack direction={"column"} gap={2} paddingTop={2}>
        <Typography fontSize={30} paddingLeft={2}>
          Products
        </Typography>
        <ProductList products={products} />
      </Stack>
    </>
  );
};
