import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import API from "../api";
import { Link } from "react-router-dom";

function Category() {
  const { categoryName } = useParams();
  const [products, setProducts] = useState([]);

  useEffect(() => {
    API.get(`/products?category=${categoryName}`)
      .then(res => setProducts(res.data.products))
      .catch(err => console.error(err));
  }, [categoryName]);

  return (
    <div>
      <h2>{categoryName} Products</h2>
      {products.map(product => (
        <div key={product.master_product_id}>
          <Link to={`/product/${product.master_product_id}`}>
            {product.product_name}
          </Link>
        </div>
      ))}
    </div>
  );
}

export default Category;