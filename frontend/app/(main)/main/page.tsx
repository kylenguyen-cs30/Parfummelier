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
        {/* welcome user title  */}
        <h1>Welcome , {user?.email}</h1>

        {/* NOTE: Recommendation by user's accord */}

        {/* NOTE: Recommendation by Season */}

        {/* NOTE: Recommendation by best selling */}
      </Content>
    </div>
  );
}
