import { createStyles } from "@mantine/core";
import { Routes, Route } from "react-router-dom";
import { observer } from 'mobx-react-lite';

import { ThemeProvider } from "./ThemeProvider";
import { useStore } from "./store";
import { MainLayout } from "./Layouts/Main";
import { DashboardLayout } from "./Layouts/Dashboard";
import { useMutation, useQuery } from '@apollo/client';
import { ME } from "./graphql/queries";
import { REFRESH_TOKEN } from "./graphql/mutations";


const useStyles = createStyles((theme) => ({
  content: {
    maxWidth: 1200,
    marginRight: theme.spacing.xl,

    [theme.fn.smallerThan('md')]: {
      maxWidth: '100%',
      marginRight: 0,
    },
  },
}));

export const App = observer(() => {
  const { classes } = useStyles();
  let { user } = useStore();

  let header_links = [
    {
      "link": "/",
      "label": "Main"
    },
    {
      "link": user.isLoggedIn ? "/dashboard" : "/login",
      "label": user.isLoggedIn ? "Dashboard" : "Login / Signup"
    },
    {
      "link": "https://docs.tronql.com/",
      "label": "Docs",
      "target": "_blank"
    },
    {
      "link": "https://api.tron.tronql.com/",
      "label": "Graphql docs",
      "target": "_blank"
    }
  ];
  let footer_data = [
    {
      "title": "Tronql",
      "links": header_links
    }
  ];

  const meQuery = useQuery(ME, {
    onCompleted: (data: any) => {
      user.setData(data.me);
    },
    onError: () => {
      const token = localStorage.getItem("refreshToken");
      if (token) {
        refreshToken();
      } else {
        user.setData(null);
      }
    }
  });

  let [refreshToken] = useMutation(REFRESH_TOKEN, {
    variables: {
      form: {
        refreshToken: localStorage.getItem("refreshToken"),
      }
    },
    onCompleted: (data: any) => {
      localStorage.setItem("token", data.refreshToken.token.toString());
      localStorage.setItem("refreshToken", data.refreshToken.refreshToken.toString());
      meQuery.refetch();
    },
    onError: () => {
      user.logOut();
      user.setData(null);
    }
  });

  return (
    <ThemeProvider>
      {!user.isLoading && (
        <Routes>
          <Route path="/dashboard/*" element={<DashboardLayout header_links={header_links} footer_data={footer_data} all_classes={classes} />}></Route>
          <Route path="*" element={<MainLayout header_links={header_links} footer_data={footer_data} all_classes={classes} />}></Route>
        </Routes>
      )}
    </ThemeProvider>
  );
});
