"use client";
import { useAuth } from "@/app/components/auth/AuthContext";
import Content from "@/app/components/ui/content/Content";
import React from "react";

export default function Main() {
  const { user } = useAuth();

  return (
    <div>
      {/* Content Section  */}
      <Content>
        <h1>Welcome , {user?.email}</h1>

        {/* <Card></Card> */}
      </Content>
    </div>
  );
}
