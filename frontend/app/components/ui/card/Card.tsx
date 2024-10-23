import React from "react";
import Image from "next/image";

interface CardProps {
  title: string;
  value: string;
  image: string; // Image URL
}

const Card: React.FC<CardProps> = ({ title, value, image }) => {
  return (
    <div className="card-container">
      <div className="image-wrapper">
        <Image
          src={image}
          alt={title}
          layout="fill" // Ensures the image covers the parent div
          objectFit="cover" // Makes the image cover the container properly
          className="rounded-lg"
        />
      </div>
      <h3 className="card-title">{title}</h3>
      <p className="card-value">{value}</p>
    </div>
  );
};

export default Card;
