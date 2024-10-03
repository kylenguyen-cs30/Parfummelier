import React from "react";

interface NavbarProps {
  children: React.ReactNode;
}
const Navbar: React.FC<NavbarProps> = ({ children }) => {
  const text = "Parfummelier store";
  return (
    <nav>
      {/* animation for letters */}
      {/* NOTE: we need Logo */}
      <div className="max-w-screen-xl flex flex-wrap items-center justify-center mx-auto p-3">
        <h1 className="p-4 text-2xl text-black">{text}</h1>

        <div className=" w-full ml-8">{children}</div>
      </div>
    </nav>
  );
};

export default Navbar;
