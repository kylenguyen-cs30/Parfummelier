"use client";

import Header from "../components/ui/header/page";
import Sidebar from "../components/ui/sidebar/Sidebar";

const DashboardLayout = () => {
  return (
    <div className="h-screen flex flex-col">
      {/* Header */}
      <Header />

      <div className="flex flex-grow">
        {/* Sidebar */}
        <Sidebar />

        {/* Main content area */}
        <main className="flex-grow p-8 bg-gray-900 text-white">
          {/* Dashboard content will go here */}
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
