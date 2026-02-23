import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api";

function Search() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const navigate = useNavigate();

  const handleSearch = async (e) => {
    e.preventDefault();

    if (!query.trim()) return;

    try {
      const response = await API.get(`/search?query=${query}`);
      setResults(response.data.results);
    } catch (error) {
      console.error("Search error:", error);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Search Products</h2>

      {/* 🔎 Search Form */}
      <form onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="Search for products..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={{ padding: "8px", width: "250px" }}
        />
        <button type="submit" style={{ marginLeft: "10px", padding: "8px" }}>
          Search
        </button>
      </form>

      <hr />

      {/* 📦 Search Results */}
      <div>
        {results.length === 0 ? (
          <p>No results found.</p>
        ) : (
          results.map((product) => (
            <div
              key={product.master_product_id}
              style={{
                border: "1px solid #ddd",
                padding: "10px",
                marginBottom: "10px",
                cursor: "pointer",
              }}
              onClick={() =>
                navigate(`/product/${product.master_product_id}`)
              }
            >
              <h4>{product.product_name}</h4>
              <p>Category: {product.category}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Search;