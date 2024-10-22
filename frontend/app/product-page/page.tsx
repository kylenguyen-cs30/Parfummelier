import React from "react";
import Image from "next/image";
import "../styles/product-page.css";

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
  product = {
    id: 1,
    name: "Rose Petal Elegance",
    description: `This fragrance exudes elegance and romance, blending soft floral notes of fresh roses with delicate petals that float around its luxurious glass bottle. With a warm and inviting scent, this perfume captures the essence of timeless beauty and grace, perfect for special occasions or everyday sophistication.`,
    rating: 4.5,
    reviews: 53,
    image: "/images/perfume1.webp",
  };

  return (
    <div className="product-page-container">
      <div className="product-content">
        {/* Image Section */}
        <div className="relative">
          <Image
            src={product.image}
            alt={product.name}
            width={500}
            height={700}
            objectFit="cover"
            className="product-image"
          />
        </div>

        {/* Product Details */}
        <div>
          <h1 className="product-title">{product.name}</h1>
          <p className="product-description">{product.description}</p>

          {/* Rating and Reviews */}
          <div className="flex items-center mt-4">
            {/* Add hover effect to the rating stars */}
            <span className="product-rating" title="Product Rating">
              ⭐ {product.rating}
            </span>
            <span className="product-reviews">{product.reviews} reviews</span>
          </div>

          {/* User Review Section */}
          <div className="review-section">
            <h2 className="review-title">User Reviews</h2>
            <ul className="review-list">
              <li className="review-item">
                "Absolutely love this fragrance!" - 5 stars
              </li>
              <li className="review-item">
                "Very elegant and long-lasting." - 4 stars
              </li>
              <li className="review-item">
                "Perfect for special occasions." - 4.5 stars
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
