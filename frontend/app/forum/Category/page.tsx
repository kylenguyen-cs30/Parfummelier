import { useRouter } from "next/router";
import axios from "axios";
import { useEffect, useState } from "react";

//This page lists all topics within a specific category
export default function CategoryPage() {
  const router = useRouter();
  const { categoryId } = router.query;
  const [topics, setTopics] = useState([]);

  useEffect(() => {
    if (categoryId) {
      axios.get(`/api/category/${categoryId}/topics`).then((response) => {
        setTopics(response.data);
      });
    }
  }, [categoryId]);

  return (
    <div>
      <h1>Topics in Category</h1>
      <ul>
        {topics.map((topic) => (
          <li key={topic.id}>
            <a href={`/topic/${topic.id}`}>{topic.title}</a>
          </li>
        ))}
      </ul>
    </div>
  );
}
