import { Link } from "react-router-dom";
import { Button, Stack, Typography } from "@mui/material";

export const Home = () => {
  return (
    <>
      <Stack alignItems={"center"} direction={"column"} spacing={6} paddingTop={10}>
        <Typography fontSize={30}>Welcome</Typography>
        <Link to={"/products"}>
          <Button variant="contained">View your products</Button>
        </Link>
      </Stack>
    </>
  );
};
