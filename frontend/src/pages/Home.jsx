import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import API from "../api";

function Home() {
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    API.get("/categories")
      .then(res => setCategories(res.data.categories))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h1>ShopPulse</h1>
      <h2>Categories</h2>
      <ul>
        {categories.map((cat, index) => (
          <li key={index}>
            <Link to={`/category/${cat}`}>{cat}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Home;