"use client";
import { Fragment } from "react";
import { useAuth } from "../../auth/AuthContext";
import { Menu, Transition } from "@headlessui/react";
import { Search, Sun, Moon, ChevronDown } from "lucide-react";
import { useTheme } from "next-themes";
import Link from "next/link";
import Image from "next/image";

const Header = () => {
  const { user, logout } = useAuth();
  const { theme, setTheme } = useTheme();

  const navigation = {
    products: [
      { name: "All Products", href: "all-products" },
      { name: "Product By Accord", href: "/product-by-accord" },
    ],
  };
};

export default Header;
