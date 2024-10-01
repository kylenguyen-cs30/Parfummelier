import React, { useState } from "react";
import axios from "axios";
import { useRouter } from "next/router";
import Button from "../components/ui/button";
import Header from "../components/Header";

const ForgetPassword = () => {
  const [formData, setFormData] = useState({
    email: "",
    userName: "",
  });
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const router = useRouter();

  // NOTE: check input
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    try {
      const response = await axios.post(
        "http://localhost:5002/forget-password/",
        formData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        },
      );

      if (response.status === 200) {
        router.push("/reset-password"); // TODO: Make sure the page available before testing
      } else {
        console.log("email not found");
      }
    } catch (error: any) {
      setError(
        error.response?.data?.error || "An Error occured while verfiying",
      );
    }
  };

  const handleTestApi = async () => {
    try {
      const response = await axios.get("http://localhost:5002/");
      if (response.status === 200) {
        alert("backend is online");
      }
    } catch (error: any) {
      setMessage("Failed to fetch message");
    }
  };

  return (
    <div className="container mx-auto">
      <Header />
      <h1>Forget Password</h1>
      {error && <p>{error}</p>}
      {/* Display Message  */}

      <form onSubmit={handleSubmit}>
        <div>
          <label>Email</label>
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
          <label>User Name</label>
          <input
            type="text"
            name="userName"
            value={formData.userName}
            onChange={handleChange}
            required
            className="w-full border rounded py-2 px-1"
          />
        </div>
        <Button type="submit">Submit</Button>
      </form>
      <Button type="button" onClick={handleTestApi}>
        Test Connection
      </Button>
    </div>
  );
};

export default ForgetPassword;
