"use client";

import { motion } from "framer-motion";
import { useAuth } from "../auth/AuthContext";
import { useRouter } from "next/navigation";
import Header from "./Header/Header";
import Sidebar from "./Sidebar/Sidebar";
import Footer from "./Footer/Footer";

const LoadingScreen = () => {
  return (
    <div className="fixed inset-0 flex items-center justify-center bg-white">
      <div className="relative">
        {/* Background pulse effect */}
        <motion.div
          className="absolute inset-0 bg-gray-100 rounded-full -z-10"
          initial={{ scale: 0.9 }}
          animate={{ scale: 1.2 }}
          transition={{
            type: "spring",
            stiffness: 260,
            damping: 20,
            repeat: Infinity,
            repeatType: "reverse",
            duration: 1.5,
          }}
        ></motion.div>

        {/* Text Animation */}
        <motion.div
          initial={{ y: -20 }}
          animate={{ y: 0 }}
          transition={{
            type: "spring",
            stiffness: 300,
            damping: 15,
            repeat: Infinity,
            repeatType: "reverse",
            duration: 1.5,
          }}
          className="px-8 py-4"
        >
          <h1 className="text-4xl font-bold text-gray-800">Parfumelier</h1>
        </motion.div>
      </div>
    </div>
  );
};

const MainLayout = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  if (isLoading) {
    return <LoadingScreen />;
  }

  if (!isAuthenticated) {
    router.push("/");
    return null;
  }

  return (
    <div className="app-layout">
      <Header />
      <div className="main-content">
        <Sidebar />
        <main className="content-area">{children}</main>
      </div>
      <Footer />
    </div>
  );
};

export default MainLayout;
