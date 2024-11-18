"use client";
import { SigninForm } from "@/app/components/auth/Siginform";

const SignIn = () => {
  return (
    <div className="container mx-auto">
      <h1 className="text-2xl font-bold mb-6">Sign In</h1>
      <SigninForm />
    </div>
  );
};
export default SignIn;
