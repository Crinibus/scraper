import { Link } from "react-router-dom";
import { Button, Stack, Typography } from "@mui/material";

export const NoPage = () => {
  return (
    <>
      <Stack alignItems={"center"} justifyItems={"center"} paddingTop={8} spacing={4}>
        <Typography fontSize={30}>404 - No page</Typography>
        <Link to={"/"}>
          <Button variant="contained">Go to homepage</Button>
        </Link>
      </Stack>
    </>
  );
};
