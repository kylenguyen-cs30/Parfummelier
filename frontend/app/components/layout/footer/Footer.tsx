import React from "react";
import Image from "next/image";
import "./Footer.css";  // Import the CSS file

const Footer = () => {
  return (
    <footer className="footer-container">
      <div className="footer-content">
        <div className="footer-branding">
          <h3 className="footer-title">Parfummelier</h3>
          <p className="footer-copy">
            &copy; {new Date().getFullYear()} Parfummelier. All rights reserved.
          </p>
        </div>

        <div className="footer-links">
          <a href="/about" className="footer-link">About Us</a>
          <a href="#" className="footer-link">Privacy Policy</a>
          <a href="#" className="footer-link">Contact</a>
        </div>
      </div>

      <div className="footer-secondary">
        <a className="footer-resource-link" href="https://nextjs.org/learn" target="_blank" rel="noopener noreferrer">
          <Image
            aria-hidden
            src="https://nextjs.org/icons/file.svg"
            alt="File icon"
            width={16}
            height={16}
          />
          Learn
        </a>

        <a className="footer-resource-link" href="https://vercel.com/templates" target="_blank" rel="noopener noreferrer">
          <Image
            aria-hidden
            src="https://nextjs.org/icons/window.svg"
            alt="Window icon"
            width={16}
            height={16}
          />
          Examples
        </a>

        <a className="footer-resource-link" href="https://nextjs.org" target="_blank" rel="noopener noreferrer">
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
