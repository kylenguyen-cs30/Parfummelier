// lib/axios.ts
import axios from "axios";

export const api = axios.create({
  baseURL: "http://localhost:8000",
  timeout: 10000,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});
