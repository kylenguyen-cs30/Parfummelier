"use client";
import { useAuth } from "@/app/components/auth/AuthContext";
import MainLayout from "@/app/components/layout/MainLayout";
import Navbar from "@/app/components/layout/Navbar/NavBar";
import Content from "@/app/components/ui/content/Content";
import React from "react";

export default function Main() {
  const { user } = useAuth();

  return (
    <MainLayout>
      <div>
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
          </div>
        </Navbar>

        {/* Content Section  */}
        <Content>
          <h1>Welcome , {user?.email}</h1>

          {/* <Card></Card> */}
        </Content>
      </div>
    </MainLayout>
  );
}
