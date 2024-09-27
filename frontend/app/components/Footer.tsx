import React from "react";
import Image from "next/image";

const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white py-6 w-full">
      <div className="flex flex-col md:flex-row justify-between items-center px-4 max-w-7xl mx-auto">
        <div className="mb-4 md:mb-0">
          <h3 className="text-xl font-bold">Parfummelier</h3>
          <p className="text-gray-400">
            &copy; {new Date().getFullYear()} Parfummelier. All rights reserved.
          </p>
        </div>

        <div className="flex space-x-6">
          <a
            href="/about"
            className="text-gray-400 hover:text-white transition duration-200"
          >
            About Us
          </a>
          <a
            href="#"
            className="text-gray-400 hover:text-white transition duration-200"
          >
            Privacy Policy
          </a>
          <a
            href="#"
            className="text-gray-400 hover:text-white transition duration-200"
          >
            Contact
          </a>
        </div>
      </div>
      <div className="flex flex-col md:flex-row justify-between items-center px-4 max-w-7xl mx-auto">
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="https://nextjs.org/learn?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            aria-hidden
            src="https://nextjs.org/icons/file.svg"
            alt="File icon"
            width={16}
            height={16}
          />
          Learn
        </a>

        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="https://vercel.com/templates?framework=next.js&utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            aria-hidden
            src="https://nextjs.org/icons/window.svg"
            alt="Window icon"
            width={16}
            height={16}
          />
          Examples
        </a>

        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="https://nextjs.org?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            aria-hidden
            src="https://nextjs.org/icons/globe.svg"
            alt="Globe icon"
            width={16}
            height={16}
          />
          Go to nextjs.org →
        </a>
      </div>
    </footer>
  );
};

export default Footer;
