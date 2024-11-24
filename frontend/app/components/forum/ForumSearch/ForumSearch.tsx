import React, { useState } from "react";
import { Search } from "lucide-react";

const ForumSearch = ({ posts, onSearch }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [searchFilter, setSearchFilter] = useState("");

  const handleSearch = (e) => {
    e.preventDefault();
    const filteredPosts = posts.filter((post) => {
      const searchLower = searchTerm.toLowerCase();
      if (searchFilter === "title") {
        return post.title.toLowerCase().includes(searchLower);
      } else {
        return post.topic.toLowerCase().includes(searchLower);
      }
    });
    onSearch(filteredPosts);
  };
  return (
    <div className="mb-6">
      <form onSubmit={handleSearch} className="flex gap-2">
        <div className="relative flex-1">
          <input
            type="text"
            placeholder={`Search by ${searchFilter}...`}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <Search
            className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"
            size={20}
          />
        </div>
        <select
          value={searchFilter}
          onChange={(e) => setSearchFilter(e.target.value)}
          className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="title">Title</option>
          <option value="topic">Topic</option>
        </select>
        <button
          type="submit"
          className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
        >
          Search
        </button>
      </form>
    </div>
  );
};

export default ForumSearch;
