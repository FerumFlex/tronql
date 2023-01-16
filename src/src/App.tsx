import { AppShell } from "@mantine/core";
import { ThemeProvider } from "./ThemeProvider";
import { HeaderSimple } from "./Components/Header";
import { FooterLinks } from "./Components/Footer";
import { MainPage } from "./Pages/Main";

export default function App() {
  let header_links = [
    {
      "link": "/",
      "label": "Main"
    },
    {
      "link": "https://api-nile.tronql.com/",
      "label": "Api - Nile"
    }
  ];
  let footer_data = [
    {
      "title": "Tronql",
      "links": header_links
    }
  ];
  return (
    <ThemeProvider>
      <AppShell
        padding="md"
        header={<HeaderSimple links={header_links} />}
        footer={<FooterLinks data={footer_data} />}
      >
        <MainPage />
      </AppShell>
    </ThemeProvider>
  );
}
