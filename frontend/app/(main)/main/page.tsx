"use client";
import { useAuth } from "@/app/components/auth/AuthContext";
import HowitWorkHero from "@/app/components/layout/HowItWorksHero";
import Content from "@/app/components/ui/content/Content";
import React from "react";

export default function Main() {
  const { user } = useAuth();

  return (
    <div>
      {/* Content Section  */}
      <Content>
        {/*NOTE: welcome user title  */}
        <h1>
          Welcome , {user?.firstName} {user?.lastName}
        </h1>
      </Content>

      {/* NOTE: Hero section */}
      <HowitWorkHero />

      {/* NOTE: How to use the website */}

      <div>
        <div>
          <h1>How to use Parfummelier</h1>
        </div>
      </div>

      {/* NOTE: Recommendation by user's accord */}

      {/* NOTE: Recommendation by Season */}

      <div>
        <div>
          <h1>Seasonal Recommendation</h1>
        </div>
      </div>
    </div>
  );
}
