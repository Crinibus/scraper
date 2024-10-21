import { useMemo } from "react";
import { useParams } from "react-router-dom";
import { Button, Divider, Stack, Typography } from "@mui/material";
import { ProductDataPoints, ProductPriceChart } from "../components/ProductPriceChart";
import { ProductInfo } from "./ProductsPage";
import { products, randomPrice } from "../test-data/products-data";

export const ProductPage = () => {
  const { id } = useParams();

  // TODO: Get product info from API
  const productInfo = useMemo(() => {
    return products.find((product) => product.id == id);
  }, [id]);

  // TODO: Get product data from API
  const productDataPoints = useMemo((): ProductDataPoints[] => {
    return [
      { date: "2024-09-15", price: randomPrice(400) },
      { date: "2024-09-16", price: randomPrice(1000) },
      { date: "2024-09-17", price: randomPrice(300) },
      { date: "2024-09-20", price: randomPrice(600) },
      { date: "2024-09-21", price: randomPrice(500) },
      { date: "2024-09-22", price: randomPrice(200) },
    ];
  }, []);

  const handleClickScrape = () => {
    // TODO: call API
    console.log(`Scrape product with id: ${id}`);
  };

  const handleClickDeactivate = () => {
    // TODO: call API
    console.log(`Deactivate product with id: ${id}`);
  };

  return (
    <>
      <Stack justifyContent={"center"} alignItems={"center"} direction={"column"}>
        <ProductDetails productInfo={productInfo} />
        <Stack alignItems={"center"} direction={"row"} justifyContent={"center"} spacing={2} padding={2}>
          <Button variant="contained" onClick={handleClickScrape}>
            Scrape product
          </Button>
          <Button variant="contained" onClick={handleClickDeactivate}>
            {productInfo?.isActive ? "Deactivate" : "Activate"}
          </Button>
        </Stack>
        <ProductPriceChart
          productName={productInfo?.name ?? "N/A"}
          dataPoints={productDataPoints}
          currency={productInfo?.currency ?? "N/A"}
        />
      </Stack>
    </>
  );
};

type ProductDetailsProps = {
  productInfo?: ProductInfo;
};

const ProductDetails = ({ productInfo }: ProductDetailsProps) => {
  return (
    <>
      <Typography fontSize={30} paddingTop={4}>
        {productInfo?.name}
      </Typography>
      <Stack direction={"row"} spacing={2} divider={<Divider flexItem orientation="vertical" />}>
        <Typography fontSize={20}>Category: {productInfo?.category}</Typography>
        <Typography fontSize={20}>Domain: {productInfo?.domain}</Typography>
      </Stack>
    </>
  );
};
