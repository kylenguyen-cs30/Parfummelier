"use client";
import { useAuth } from "@/app/components/auth/AuthContext";
import HowitWorkHero from "@/app/components/layout/HowItWorksHero";
import ProtectedRoute from "@/app/components/ProtectedRoute";
import Content from "@/app/components/ui/content/Content";
import React from "react";

export default function Main() {
  const { user } = useAuth();

  return (
    <ProtectedRoute>
      <div>
        {/* NOTE: Content Section  */}
        <Content>
          {/*NOTE: welcome user title  */}
          <h1>
            Welcome , {user?.firstName} {user?.lastName}
          </h1>
        </Content>

        {/* NOTE: How it work Hero section */}
        <HowitWorkHero />

        {/* NOTE: Recommendation by user's accord */}

        <div>
          <div>
            <h1>User's Accord Recommendation</h1>
            <h2>Base on quiz answer</h2>
          </div>
        </div>
        {/* NOTE: Recommendation by Season */}

        <div>
          <div>
            <h1>Seasonal Recommendation</h1>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
