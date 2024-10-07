import React from "react";
import Card from "../components/ui/card/Card"; // Update this import based on your folder structure

interface Product {
  id: number;
  name: string;
  price: string;
  image: string;
}

const products: Product[] = [
  { id: 1, name: "Fragrance A", price: "$50", image: "/images/perfume1.webp" },
  { id: 2, name: "Fragrance B", price: "$75", image: "/images/perfume2.webp" },
  { id: 3, name: "Fragrance C", price: "$100", image: "/images/perfume3.webp" },
  { id: 4, name: "Fragrance D", price: "$120", image: "/images/perfume1.webp" },
];

const AllProducts: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-4xl font-bold text-center mb-8">All Products</h1>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
          {products.map((product) => (
            <Card
              key={product.id}
              title={product.name}
              value={product.price}
              image={product.image}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default AllProducts;
