import { Button, Typography } from "@mui/material";
import { DataGrid, useGridApiRef } from "@mui/x-data-grid";
import { useMemo } from "react";
import { v4 as uuidv4 } from "uuid";
import { Product } from "../models/product";

export const ProductListPage = () => {
  const apiGridRef = useGridApiRef();

  const products = useMemo((): Product[] => {
    return [
      { name: "Name-1", category: "Cat-1", price: 123, domain: "domain-1" },
      { name: "Name-2", category: "Cat-2", price: 234, domain: "domain-2" },
      { name: "Name-3", category: "Cat-3", price: 345, domain: "domain-3" },
    ];
  }, []);

  const columns = useMemo(() => {
    return [
      { field: "name", headerName: "Name", flex: 1 },
      { field: "category", headerName: "Category", flex: 1 },
      { field: "domain", headerName: "Domain", flex: 1 },
      { field: "price", headerName: "Price", flex: 1 },
    ];
  }, []);

  const handleGetSelectedOnClick = () => {
    const selectedRows = apiGridRef.current.getSelectedRows();
    console.dir(selectedRows);
  };

  return (
    <>
      <Typography fontSize={30}>Simple product list</Typography>
      <div style={{ height: 300, maxWidth: 900, width: "100%" }}>
        <DataGrid
          apiRef={apiGridRef}
          rows={products}
          columns={columns}
          getRowId={() => uuidv4()}
          checkboxSelection
          disableRowSelectionOnClick
        />
      </div>
      <Button onClick={handleGetSelectedOnClick}>Get selected rows</Button>
    </>
  );
};
