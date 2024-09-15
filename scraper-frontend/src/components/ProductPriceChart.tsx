import { useMemo } from "react";
import { Box } from "@mui/material";
import { LineChart } from "@mui/x-charts";

export type ProductDataPoints = {
  price: number;
  date: string;
};

type ProductPriceChartProps = {
  productName: string;
  dataPoints: ProductDataPoints[];
  currency: string;
};

export const ProductPriceChart = ({ productName, dataPoints, currency }: ProductPriceChartProps) => {
  const productDates = useMemo(() => dataPoints.map((dataPoint) => new Date(dataPoint.date)), [dataPoints]);
  const productPrices = useMemo(() => dataPoints.map((dataPoint) => dataPoint.price), [dataPoints]);

  return (
    <>
      <Box height={600} width={1} boxShadow={3}>
        <LineChart
          xAxis={[
            {
              scaleType: "time",
              data: productDates,
              label: "Date",
            },
          ]}
          yAxis={[
            {
              label: `Price ${currency}`,
            },
          ]}
          series={[
            {
              label: productName,
              data: productPrices,
              valueFormatter: (value) => `${currency} ${value}`,
              curve: "monotoneX",
            },
          ]}
        />
      </Box>
    </>
  );
};
