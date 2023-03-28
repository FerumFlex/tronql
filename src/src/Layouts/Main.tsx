import { AppShell, Container } from "@mantine/core";
import { Routes, Route } from "react-router-dom";

import { HeaderSimple } from "../Components/Header";
import { FooterLinks } from "../Components/Footer";
import { MainPage } from "../Pages/Main";
import { LoginPage } from "../Pages/Auth/Login";
import { ForgotPasswordPage } from "../Pages/Auth/Forgot";
import { NotFoundPage } from "../Pages/NotFound";
import { RegisterPage } from "../Pages/Auth/Register";
import { VerifyPage } from "../Pages/Auth/Verify";
import { ChangePasswordPage } from "../Pages/Auth/Change";


export const MainLayout = ({header_links, footer_data, all_classes}: {header_links: any, footer_data: any, all_classes: any}) => {
  return (
    <AppShell
      padding="md"
      header={<HeaderSimple links={header_links} />}
      footer={<FooterLinks data={footer_data} />}
    >
      <Container>
        <div className={all_classes.content}>
          <Routes>
            <Route path="/" element={<MainPage />}></Route>
            <Route path="/login" element={<LoginPage />}></Route>
            <Route path="/register" element={<RegisterPage />}></Route>
            <Route path="/forgot" element={<ForgotPasswordPage />}></Route>
            <Route path="/verify/:code" element={<VerifyPage />}></Route>
            <Route path="/password/change/:code" element={<ChangePasswordPage />}></Route>
            <Route path="*" element={<NotFoundPage />}></Route>
          </Routes>
        </div>
      </Container>
    </AppShell>
  )
}
