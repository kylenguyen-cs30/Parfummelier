import React from "react";
import Image from "next/image"; // Use next/image for optimized images
import "../styles/globals.css"; // Import global CSS

// Define the interface within the component file
interface ProductProps {
  product: {
    id: number;
    name: string;
    description: string;
    rating: number;
    reviews: number;
    image: string;
  };
}

export default function Product({ product }: ProductProps) {
  // Mock product data (can be passed as props in the future)
  product = {
    id: 1,
    name: "Rose Petal Elegance",
    description: `This fragrance exudes elegance and romance, blending soft floral notes of fresh roses with delicate petals that float around its luxurious glass bottle. With a warm and inviting scent, this perfume captures the essence of timeless beauty and grace, perfect for special occasions or everyday sophistication.`,
    rating: 4.5,
    reviews: 53,
    image: "/images/perfume1.webp", // Example image path
  };

  return (
    <div className="min-h-screen container">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Image Section */}
        <div className="relative">
          <Image
            src={product.image}
            alt={product.name}
            width={500}
            height={700}
            objectFit="cover"
            className="rounded-lg"
          />
        </div>

        {/* Product Details */}
        <div>
          <h1 className="product-title">{product.name}</h1>
          <p className="product-description">{product.description}</p>
          <div className="flex items-center mb-4">
            <span className="product-rating">⭐ {product.rating}</span>
            <span className="text-gray-400">{product.reviews} ratings</span>
          </div>

          {/* Purchase Options */}
          <div className="card">
            <h2 className="card-title">Subscription</h2>
            <p className="product-description">30-day supply of fragrance</p>
            <div className="flex justify-between items-center">
              <span className="card-price">$8.47</span>
              <button className="button card-button">Subscribe</button>
            </div>
          </div>

          <div className="card">
            <h2 className="card-title">One-time purchase</h2>
            <p className="product-description">Full-size bottle</p>
            <div className="flex justify-between items-center">
              <span className="card-price">$21.95</span>
              <button className="button card-button">Buy Now</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
