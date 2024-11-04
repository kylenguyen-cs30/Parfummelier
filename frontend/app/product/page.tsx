import React from "react";
import Image from "next/image"; // Use next/image for optimized images

interface ProductProps {
  product: {
    id: number;
    name: string;
    description: string;
    price: number;
    rating: number;
    reviews: number;
    image: string;
  };
}

const Product: React.FC<ProductProps> = () => {
  const product = {
    id: 1,
    name: "Rose Petal Elegance",
    description: `This fragrance exudes elegance and romance, blending soft floral notes of fresh roses with delicate petals that float around its luxurious glass bottle. With a warm and inviting scent, this perfume captures the essence of timeless beauty and grace, perfect for special occasions or everyday sophistication.`,
    price: 80.0,
    rating: 4.5,
    reviews: 53,
    image: "/images/perfume1.webp", // Example image path
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="container mx-auto py-8 px-4 lg:px-8">
        {/* Top section with fragrance image and details */}
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
            <div className="mb-4">
              <h1 className="text-4xl font-bold mb-2">{product.name}</h1>
              <p className="text-lg text-gray-400 mb-4">
                {product.description}
              </p>
              <div className="flex items-center mb-4">
                {/* Rating */}
                <span className="text-yellow-400 mr-2">
                  ⭐ {product.rating}
                </span>
                <span className="text-gray-400">{product.reviews} ratings</span>
              </div>
            </div>

            {/* Pricing and Purchase Options */}
            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="flex justify-between items-center mb-4">
                <span className="text-2xl font-bold">
                  ${product.price.toFixed(2)}
                </span>
                <button className="bg-blue-600 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded-lg">
                  Add to Cart
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Subscription and other purchase options */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8">
          {/* Subscription option */}
          <div className="bg-gray-800 p-4 rounded-lg">
            <h2 className="text-lg font-bold mb-2">Subscription</h2>
            <p className="text-gray-400 mb-4">30-day supply of fragrance</p>
            <div className="flex justify-between items-center">
              <span className="text-2xl font-bold">$8.47</span>
              <button className="bg-yellow-600 hover:bg-yellow-500 text-white font-bold py-2 px-4 rounded-lg">
                Subscribe
              </button>
            </div>
          </div>

          {/* One-time purchase */}
          <div className="bg-gray-800 p-4 rounded-lg">
            <h2 className="text-lg font-bold mb-2">One-time purchase</h2>
            <p className="text-gray-400 mb-4">Full-size bottle</p>
            <div className="flex justify-between items-center">
              <span className="text-2xl font-bold">$21.95</span>
              <button className="bg-green-600 hover:bg-green-500 text-white font-bold py-2 px-4 rounded-lg">
                Buy Now
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Product;
