//import { useState, useEffect } from 'react';
import Card from "../components/ui/card/Card";

interface Product {
  id: number;
  name: string;
  price: string;
  image: string;
}

// const Basket: React.FC = () => {
//   const [viewedProducts, setViewedProducts] = useState<Product[]>([]);

//   useEffect(() => {
//     // Fetch viewed products from localStorage
//     const products = JSON.parse(localStorage.getItem('viewedProducts') || '[]');
//     setViewedProducts(products);
//   }, []);

//   const removeItem = (id: number) => {
//     const updatedProducts = viewedProducts.filter((product) => product.id !== id);
//     setViewedProducts(updatedProducts);
//     localStorage.setItem('viewedProducts', JSON.stringify(updatedProducts));
//   };

//   return (
//     <div className="min-h-screen bg-gray-100 py-8">
//       <div className="container mx-auto px-4">
//         <h1 className="text-4xl font-bold text-center mb-8">Viewed Products</h1>

//         {viewedProducts.length === 0 ? (
//           <p className="text-center text-lg">You haven't viewed any products yet</p>
//         ) : (
//           <div className="grid grid-cols-1 sm:grid-cols-2 gap-8">
//             {viewedProducts.map((product) => (
//               <div key={product.id} className="border border-gray-300 p-4 rounded-lg">
//                 <div className="relative w-full h-48 mb-4">
//                   <img
//                     src={product.image}
//                     alt={product.name}
//                     className="object-cover w-full h-full rounded-lg"
//                   />
//                 </div>
//                 <h3 className="text-lg font-bold mb-2">{product.name}</h3>
//                 <p className="text-md">Price: {product.price}</p>
//                 <button
//                   onClick={() => removeItem(product.id)}
//                   className="mt-4 bg-red-500 text-white px-4 py-2 rounded hover:bg-red-400"
//                 >
//                   Remove
//                 </button>
//               </div>
//             ))}
//           </div>
//         )}
//       </div>
//     </div>
//   );
// };

const products: Product[] = [
  { id: 1, name: "Fragrance A", price: "$50", image: "/images/perfume1.webp" },
  { id: 2, name: "Fragrance B", price: "$75", image: "/images/perfume2.webp" },
  { id: 3, name: "Fragrance C", price: "$100", image: "/images/perfume3.webp" },
  { id: 4, name: "Fragrance D", price: "$120", image: "/images/perfume1.webp" },
];

const Basket = () => {
  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-4xl font-bold text-center mb-8">My Basket</h1>
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
      <button
        className="mt-4 bg-red-600 text-white px-6 py-3 rounded hover:bg-red-500"
        // onClick={clearBasket}
      >
        Clear Basket
      </button>
    </div>
  );
};

export default Basket;
