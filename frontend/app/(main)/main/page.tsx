"use client";
import { useAuth } from "@/app/components/auth/AuthContext";
import MainLayout from "@/app/components/layout/MainLayout";
import Content from "@/app/components/ui/content/Content";
import React from "react";

export default function Main() {
  const { user } = useAuth();

  return (
    <MainLayout>
      <div>
        {/* Content Section  */}
        <Content>
          <h1>Welcome , {user?.email}</h1>

          {/* <Card></Card> */}
        </Content>
      </div>
    </MainLayout>
  );
}
