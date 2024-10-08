import React from "react";
import Image from "next/image";

interface CardProps {
  title: string;
  value: string;
  image: string; // Image URL
}

const Card: React.FC<CardProps> = ({ title, value, image }) => {
  return (
    <div className="border border-gray-300 p-4 rounded-lg mb-6 w-72 h-96">
      <div className="relative w-full h-48 mb-4">
        <Image
          src={image}
          alt={title}
          layout="fill" // Ensures the image covers the parent div
          objectFit="cover" // Makes the image cover the container properly
          className="rounded-lg"
        />
      </div>
      <h3 className="text-lg font-bold mb-2">{title}</h3>
      <p className="text-2xl font-semibold">{value}</p>
    </div>
  );
};

export default Card;
