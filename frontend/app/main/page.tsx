"use client";
import React from "react";
import Header from "../components/ui/header/Header";
import Navbar from "../components/ui/navbar/NavBar";
import Content from "../components/ui/content/Content";
import Footer from "../components/ui/footer/Footer";
import Button from "../components/ui/button/Button";
import { useAuth } from "../components/AuthContext";
import Sidebar from "../components/ui/sidebar/Sidebar";

export default function Main() {
  const { logout } = useAuth();


  return (
    <div>
      <Header />
      <Sidebar />
      <Navbar>
        <div className="flex flex-row">
          <ul>
            <li>
              <a>Perfumes</a>
            </li>
            <li>
              <a>Discover</a>
            </li>
            <li>
              <a>Community</a>
            </li>
          </ul>
          <Button type="button" onClick={logout}>
            Log out
          </Button>
        </div>
      </Navbar>

      {/* Content Section  */}
      <Content>
        <h1>This is main page</h1>
        {/* <Card></Card> */}
      </Content>
      <Footer />
    </div>
  );
}
