// app/products/page.tsx
"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "../../components/ui/card/Card";
import { api } from "../../lib/axios";
import LoadingScreen from "@/app/components/common/LoadingScreen/LoadingScreen";

interface Accord {
  name: string;
  background_color: string;
}

interface Product {
  id: number;
  name: string;
  accords: Accord[];
  brand: string;
  imageURL: string | null;
}

const getImageUrl = (url: string | null) => {
  if (!url) return null;
  // Replace localhost with api-gateway in URLs if they exist
  if (url.includes("localhost:8000")) {
    return url.replace("localhost:8000", "api-gateway:8000");
  }
  return url;
};

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const { data } = await api.get("/products/products");

        const transformedProducts = data.map((product: Product) => ({
          ...product,
          imageURL: getImageUrl(product.imageURL),
        }));
        setProducts(transformedProducts);
      } catch (err) {
        console.error("Fetch error:", err);
        setError(
          err instanceof Error ? err.message : "Failed to fetch products",
        );
      } finally {
        setIsLoading(false);
      }
    };
    fetchProducts();
  }, []);

  if (isLoading) return <LoadingScreen />;
  if (error)
    return <div className="text-center text-red-500 p-8">Error: {error}</div>;

  return (
    <div className="container mx-auto p-8">
      <h1 className="text-3xl font-bold mb-8">Perfume Collection</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {products.map((product) => (
          <Card key={product.id}>
            <CardHeader>
              <CardTitle>{product.name}</CardTitle>
              <p className="text-gray-500">{product.brand}</p>
            </CardHeader>

            <CardContent>
              {product.imageURL && (
                <div className="relative h-64 mb-4">
                  <Image
                    src={product.imageURL}
                    alt={product.name}
                    fill
                    className="object-cover rounded-md"
                  />
                </div>
              )}

              <div className="flex flex-wrap gap-2">
                {product.accords.map((accord, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 rounded-full text-sm"
                    style={{
                      backgroundColor: accord.background_color,
                      color: isLightColor(accord.background_color)
                        ? "black"
                        : "white",
                    }}
                  >
                    {accord.name}
                  </span>
                ))}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}

function isLightColor(color: string) {
  const hex = color.replace("#", "");
  const r = parseInt(hex.slice(0, 2), 16);
  const g = parseInt(hex.slice(2, 4), 16);
  const b = parseInt(hex.slice(4, 6), 16);

  const brightness = (r * 299 + g * 587 + b * 114) / 1000;
  return brightness > 128;
}
