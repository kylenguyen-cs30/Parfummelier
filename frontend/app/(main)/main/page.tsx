"use client";
import { useAuth } from "@/app/components/auth/AuthContext";
import HowitWorkHero from "@/app/components/layout/HowItWorksHero";
import ProtectedRoute from "@/app/components/ProtectedRoute";
import QuizPromptSection from "@/app/components/quiz/QuizPromptSection";
import Content from "@/app/components/ui/content/Content";
import React from "react";

export default function Main() {
  const { user } = useAuth();

  const isNewUser = !user?.accord || user.accord.length === 0;

  return (
    <ProtectedRoute>
      <div>
        <Content>
          <h1>
            Welcome , {user?.firstName} {user?.lastName}
          </h1>
        </Content>
        <HowitWorkHero />
        {/* NOTE: Quiz prompt section */}
        <QuizPromptSection isNewUser={isNewUser}></QuizPromptSection>
        {/* NOTE: Recommendation by user's accord, we need to find a way to connect */}
        {/* the user's answer to the user's context for the update product */}
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
