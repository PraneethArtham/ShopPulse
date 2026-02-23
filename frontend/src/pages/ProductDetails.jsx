import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import API from "../api";

function ProductDetails() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);

  useEffect(() => {
    API.get(`/products/${id}`)
      .then(res => setProduct(res.data))
      .catch(err => console.error(err));
  }, [id]);

  if (!product) return <div>Loading...</div>;

  return (
    <div>
      <h1>{product.product.product_name}</h1>

      <h3>Online Platforms</h3>
      {product.platform_listings.map((item, index) => (
        <div key={index}>
          <p>Price: ₹{item.price}</p>
          <p>Seller: {item.seller?.seller_name}</p>
        </div>
      ))}

      <h3>Local Stores</h3>
      {product.local_store_listings.map((item, index) => (
        <div key={index}>
          <p>Price: ₹{item.price}</p>
          <p>Store: {item.store?.store_name}</p>
        </div>
      ))}
    </div>
  );
}

export default ProductDetails;