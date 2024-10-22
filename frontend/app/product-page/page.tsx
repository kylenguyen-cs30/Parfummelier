import React from "react";
import Image from "next/image";
import "../styles/product-page.css";

export default function ProductPage() {
  const product = {
    id: 1,
    name: "Rose Petal Elegance",
    description: `This fragrance exudes elegance and romance, blending soft floral notes of fresh roses with delicate petals that float around its luxurious glass bottle. With a warm and inviting scent, this perfume captures the essence of timeless beauty and grace, perfect for special occasions or everyday sophistication.`,
    rating: 4.5,
    reviews: 53,
    image: "/images/perfume1.webp",
    notes: ["Rose", "Jasmine", "Musk"],
    accords: ["Floral", "Warm", "Soft"],
    seasons: ["Spring", "Autumn"],
    collection: "Classic Collection",
    designer: "Perfume House",
    manufacturer: "Fragrance Inc.",
  };

  const reviews = [
    { content: "Absolutely love this fragrance!", stars: 5 },
    { content: "Very elegant and long-lasting.", stars: 4 },
    { content: "Perfect for special occasions.", stars: 4.5 },
  ];

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
            className="product-image"
          />
        </div>

        {/* Product Details */}
        <div className="product-details">
          <h1 className="product-title">{product.name}</h1>
          <p className="product-description">{product.description}</p>

          {/* Additional Product Information */}
          <div className="additional-info">
            <p>
              <strong>Notes:</strong> {product.notes.join(", ")}
            </p>
            <p>
              <strong>Accords:</strong> {product.accords.join(", ")}
            </p>
            <p>
              <strong>Seasons:</strong> {product.seasons.join(", ")}
            </p>
            <p>
              <strong>Collection:</strong> {product.collection}
            </p>
            <p>
              <strong>Designer:</strong> {product.designer}
            </p>
            <p>
              <strong>Manufacturer:</strong> {product.manufacturer}
            </p>
          </div>

          {/* Rating and Reviews */}
          <div className="flex items-center mt-4">
            <span className="product-rating" title="Product Rating">
              ⭐ {product.rating}
            </span>
            <span className="product-reviews">{product.reviews} reviews</span>
          </div>

          {/* User Review Section */}
          <div className="review-section">
            <h2 className="review-title">User Reviews</h2>
            <ul className="review-list">
              {reviews.map((review, index) => (
                <li key={index} className="review-item">
                  <span className="review-content">{review.content}</span>
                  <div className="review-stars">
                    {Array.from(
                      { length: Math.floor(review.stars) },
                      (_, i) => (
                        <span key={i}>⭐</span>
                      )
                    )}
                    {review.stars % 1 !== 0 && <span>⭐½</span>}
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
