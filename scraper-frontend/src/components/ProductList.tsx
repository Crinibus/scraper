import { useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { Box, Button } from "@mui/material";
import { DataGrid, GridCellParams, GridColDef } from "@mui/x-data-grid";
import { v4 as uuidv4 } from "uuid";
import { ProductInfo } from "../pages/ProductsPage";

export type ProductListProps = {
  products: ProductInfo[];
};

export const ProductList = ({ products }: ProductListProps) => {
  const navigate = useNavigate();

  const columns = useMemo((): GridColDef[] => {
    const renderCellWithButton = (params: GridCellParams) => {
      const productId = params.row.id;

      const onClick = (event: React.MouseEvent) => {
        event.stopPropagation();
        navigate(`/product/${productId}`);
      };

      return (
        <Button variant="text" onClick={onClick} fullWidth>
          View product
        </Button>
      );
    };

    return [
      { field: "name", headerName: "Name", flex: 1 },
      { field: "category", headerName: "Category", flex: 1 },
      { field: "domain", headerName: "Domain", flex: 1 },
      { field: "currency", headerName: "Currency", flex: 1 },
      {
        field: "action",
        headerName: "",
        width: 200,
        sortable: false,
        hideable: false,
        filterable: false,
        renderCell: renderCellWithButton,
      },
    ];
  }, [navigate]);

  return (
    <>
      <Box alignContent={"center"} justifyContent={"center"} alignItems={"center"} padding={2} height={"800px"}>
        <DataGrid rows={products} columns={columns} getRowId={() => uuidv4()} disableRowSelectionOnClick />
      </Box>
    </>
  );
};
