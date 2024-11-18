import React, { useState } from "react";
import { useAuth } from "./AuthContext";
import Button from "../ui/button/Button";

export const SigninForm = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });
  const [error, setError] = useState<string | null>(null);
  const { login } = useAuth();

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    try {
      await login(formData.email, formData.password);
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("An unexpected error occurred");
      }
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label className="block">Email</label>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
          className="w-full border rounded px-2 py-1"
        />
      </div>
      <div>
        <label className="block">Password</label>
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
          className="w-full border rounded px-2 py-1"
        />
      </div>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <div>
        <a href="/forget-password" className="text-blue-500">
          Forgot My Password?
        </a>
      </div>
      <Button type="submit">Sign In</Button>
    </form>
  );
};
