"use client";
import React, { useEffect } from "react";
import Header from "../components/ui/header/page";
import Navbar from "../components/ui/navbar/page";
import Content from "../components/ui/content/page";
import Footer from "../components/ui/footer/page";
import Button from "../components/ui/button/page";
import { useAuth } from "../components/AuthContext";
import { useRouter } from "next/navigation";
import Sidebar from "../components/ui/Sidebar";

export default function Home() {
  const { accessToken } = useAuth();
  const { logout } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!accessToken) {
      router.push("/main-page");
    }
  }, [accessToken, router]);

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
      <Content>
        <h1>This is main page</h1>
      </Content>
      <Footer />
    </div>
  );
}
