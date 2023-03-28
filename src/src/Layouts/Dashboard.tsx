import { AppShell, Container } from "@mantine/core";
import { Routes, Route } from "react-router-dom";

import { HeaderSimple } from "../Components/Header";
import { FooterLinks } from "../Components/Footer";
import { ProjectsPage } from "../Pages/Project/List";
import { NavbarSection } from "../Components/Navbar";
import { NotFoundPage } from "../Pages/NotFound";
import { ProjectViewPage } from "../Pages/Project/View";


export const DashboardLayout = ({header_links, footer_data, all_classes}: {header_links: any, footer_data: any, all_classes: any}) => {
  return (
    <AppShell
      padding="md"
      navbar={<NavbarSection />}
      header={<HeaderSimple links={header_links} />}
      footer={<FooterLinks data={footer_data} />}
    >
      <Container>
        <div className={all_classes.content}>
          <Routes>
            <Route path="/project/:projectId" element={<ProjectViewPage />}></Route>
            <Route path="/" element={<ProjectsPage />}></Route>
            <Route path="*" element={<NotFoundPage />}></Route>
          </Routes>
        </div>
      </Container>
    </AppShell>
  )
}
