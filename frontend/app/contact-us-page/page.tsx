"use client";
import React from "react";
import ContactForm from "../components/ContactForm";

const ContactUs = () => {
  return (
    <div>
      <div>
        <h1>Contact Us</h1>
        <p>
          We’d love to hear from you! Whether you have a question about our app,
          need help finding the perfect fragrance, or just want to share your
          thoughts, feel free to reach out.
        </p>
        <p>Get in Touch</p>
        <p>Email: contact@parfummelier.com</p>
        <p>Phone: +1 (123) 456-7890</p>
        <p>Address: Parfummelier Headquarters</p>
        <p>123 Fragrance Street, Scent City, 45678</p>
      </div>
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <ContactForm />
      </div>
      <div>
        <h1>Follow Us</h1>
        <p>
          Stay connected and follow us on social media for the latest updates on
          new fragrances, features, and more!
        </p>
        <ul>
          <li>Instagram: @parfummelier</li>
          <li>Twitter: @parfummelier</li>
          <li>Facebook: Parfummelier</li>
        </ul>
      </div>
      <div>
        <h1>FAQ</h1>
        <p>
          Looking for quick answers? Check out our <a href="#">FAQ page</a>.
        </p>
      </div>
    </div>
  );
};

export default ContactUs;
