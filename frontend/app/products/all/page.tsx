"use client";

import { useEffect, useState, useMemo } from "react";
import Image from "next/image";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "../../components/ui/card/Card";
import { api } from "../../lib/axios";
import { Search } from "lucide-react";
import LoadingScreen from "@/app/components/common/LoadingScreen/LoadingScreen";
import ProtectedRoute from "@/app/components/ProtectedRoute";
import axios from "axios";
import Link from "next/link";

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

// NOTE: format the image to point the correct addresss
// and render them correctly on the right server
const getImageUrl = (url: string | null) => {
  if (!url) return null;
  try {
    // Fix potential missing slash between 'images' and filename
    const fixedUrl = url.replace("/images", "/images/");
    const imageUrl = new URL(fixedUrl);

    // For development environment, use localhost:8000
    if (process.env.NODE_ENV === "development") {
      imageUrl.hostname = "localhost";
      imageUrl.port = "8000";
    }

    return imageUrl.toString();
  } catch (error) {
    console.error("Error processing image URL:", error);
    return url;
  }
};

// NOTE: Product Card Component for Image rendering
const ProductCard = ({ product }: { product: Product }) => {
  const [imageError, setImageError] = useState(false);

  const imageUrl = useMemo(() => {
    if (!product.imageURL) return null;
    return getImageUrl(product.imageURL);
  }, [product.imageURL]);

  if (!imageUrl || imageError) {
    return (
      <div className="relative w-[240px] h-[320px] mb-4 bg-gray-200 flex items-center justify-center">
        <span className="text-gray-400">No image available</span>
      </div>
    );
  }

  return (
    <div className="relative w-[240px] h-[320px] mb-4">
      <Image
        src={imageUrl}
        alt={product.name}
        width={240}
        height={320}
        className="rounded-md object-cover"
        onError={(e) => {
          console.error(`Failed to load image: ${imageUrl}`);
          setImageError(true);
        }}
        unoptimized
        // quality={75}
      />
    </div>
  );
};

export default function AllProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Search and filter states
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedBrand, setSelectedBrand] = useState<string>("all");
  const [selectedAccord, setSelectedAccord] = useState<string>("all");

  //Memoized unique brands and accords
  const brands = useMemo(() => {
    const uniqueBrands = Array.from(new Set(products.map((p) => p.brand)));
    return ["all", ...uniqueBrands.sort()];
  }, [products]);

  const accords = useMemo(() => {
    const uniqueAccords = Array.from(
      new Set(products.flatMap((p) => p.accords.map((a) => a.name))),
    );
    return ["all", ...uniqueAccords.sort()];
  }, [products]);

  // memoized filter product
  const filteredProducts = useMemo(() => {
    return products.filter((product) => {
      const matchesSearch =
        product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.brand.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesBrand =
        selectedBrand === "all" || product.brand === selectedBrand;
      const matchesAccord =
        selectedAccord === "all" ||
        product.accords.some((accord) => accord.name === selectedAccord);

      return matchesSearch && matchesBrand && matchesAccord;
    });
  }, [products, searchTerm, selectedAccord, selectedBrand]);

  // api request to the backend for product
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const { data } = await api.get("/products/products");

        const transformedProducts = data.map((product: Product) => {
          const transformedUrl = getImageUrl(product.imageURL);
          return {
            ...product,
            imageURL: transformedUrl,
          };
        });

        setProducts(transformedProducts);
      } catch (err) {
        if (axios.isAxiosError(err)) {
          console.error("Axios error details:", {
            status: err.response?.status,
            data: err.response?.data,
            headers: err.response?.headers,
            config: err.config,
          });
        }
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
    <ProtectedRoute>
      <div className="container mx-auto p-8">
        <h1 className="text-3xl font-bold mb-8">Perfume Collection</h1>
        {/* NOTE: Search and filter Section */}
        <div className="mb-8 space-y-3">
          <div className="flex flex-col sm:flex-row gap-4">
            {/* NOTE: Search Input */}
            <div className="relative flex-1">
              <div className="absolute inset-y-0 left-3 flex items-center pointer-events-none">
                <Search className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="text"
                placeholder="Search products..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 pr-4 py-2 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
              />
            </div>

            {/* NOTE: Brand Select  */}
            <select
              value={selectedBrand}
              onChange={(e) => setSelectedBrand(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none bg-white"
            >
              <option value="all">All Brands</option>
              {brands
                .filter((brand) => brand !== "all")
                .map((brand) => (
                  <option key={brand} value={brand}>
                    {brand}
                  </option>
                ))}
            </select>

            {/* NOTE: Accord Select */}
            <select
              value={selectedAccord}
              onChange={(e) => setSelectedAccord(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none bg-white"
            >
              <option value="all">All Accords</option>
              {accords
                .filter((accord) => accord !== "all")
                .map((accord) => (
                  <option key={accord} value={accord}>
                    {accord}
                  </option>
                ))}
            </select>
          </div>
          {/* NOTE: Result count */}
          <div>
            Showing {filteredProducts.length} of {products.length} products
          </div>
        </div>

        {/* NOTE: Product Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {filteredProducts.map((product) => (
            <Link
              key={product.id}
              href={`/products/${encodeURIComponent(product.name)}`}
            >
              <Card className="flex flex-col">
                <CardHeader className="flex-none">
                  <CardTitle className="text-lg">{product.name}</CardTitle>
                  <p className="text-gray-500 text-sm">{product.brand}</p>
                </CardHeader>
                <CardContent className="flex-grow flex flex-col items-center">
                  <ProductCard product={product} />
                  <div className="flex flex-wrap gap-1.5 justify-center">
                    {product.accords.map((accord, index) => (
                      <span
                        key={index}
                        className="px-2 py-0.5 rounded-full text-xs"
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
            </Link>
          ))}
        </div>
      </div>
    </ProtectedRoute>
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
