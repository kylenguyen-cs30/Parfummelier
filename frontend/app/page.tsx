import Header from "./components/Header";
import Navbar from "./components/Navbar";
import Content from "./components/Content";
import Footer from "./components/Footer";

export default function Home() {
  return (
    <div>
      <Header />
      <Navbar />
      <Content>
        <h1>This is landing page</h1>
      </Content>
      <Footer />
    </div>
  );
}
