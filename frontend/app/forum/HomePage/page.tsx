import axios from "axios";
import { useEffect, useState } from "react";

//This page lists all categories
export default function HomePage() {
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    axios.get("/api/categories").then((response) => {
      setCategories(response.data);
    });
  }, []);

  return (
    <div>
      <h1>Forum Categories</h1>
      <ul>
        {categories.map((category) => (
          <li key={category.id}>
            <a href={`/category/${category.id}`}>{category.name}</a>
          </li>
        ))}
      </ul>
    </div>
  );
}
