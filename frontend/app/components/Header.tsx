import React from "react";

const Header = () => {
  const text = "Parfummelier store";
  return (
    <nav>
      {/* animation for letters */}
      {/* NOTE: we need Logo */}
      <div className="max-w-screen-xl flex flex-wrap items-center justify-center justify-between mx-auto p-3">
        <a className="flex items-center space-x-6">
          {/* TODO: Add image link here */}
          <div className="p-4 text-2xl text-black">
            {text.split("").map((char, index) => (
              <span
                key={index}
                className="slide-in-effect"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                {char === " " ? "\u00A0" : char}
              </span>
            ))}
          </div>
        </a>
        {/* NOTE: Page Nav links */}
        <div className=" w-full ml-8">
          <ul className="font-medium flex p-4 mt-4 border rounded-lg md:space-x-8 md:mt-0">
            <li>
              <a href="/" className="block py-2 px-3 rounded">
                Home
              </a>
            </li>
            <li>
              <a href="/product" className="block py-2 px-3 rounded">
                Product
              </a>
            </li>
            <li>
              <a href="/signin" className="block py-2 px-3 rounded">
                Sign in
              </a>
            </li>
            <li>
              <a href="/signup" className="block py-2 px-3 rounded">
                Sign Up
              </a>
            </li>
            <li>
              <a href="/about" className="block py-2 px-3 rounded">
                About
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Header;
