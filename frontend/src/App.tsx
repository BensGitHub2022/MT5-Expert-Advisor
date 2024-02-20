import { useEffect, useState } from "react";
import type { ClosedOrderType } from "./types";
import { ClosedOrder } from "./components/order";
import styles from "./app.module.css";

export default function App() {
  const [data, setData] = useState<ClosedOrderType[]>();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:5000/orders-closed");
        const json = await response.json();
        const orders: ClosedOrderType[] = json.orders;
        setData(orders);
      } catch (err) {
        console.error("Data fetching error", err);
      }
    };
    fetchData();
  }, []);
  console.log(data);
  const info =
    data !== undefined ? (
      <div>
        <h1>Order History</h1>
        <table>
          <tr>
            <th className={styles.th}>Transaction Date</th>
            <th className={styles.th}>Ticket Number</th>
            <th className={styles.th}>Symbol</th>
            <th className={styles.th}>Volume</th>
            <th className={styles.th}>Comment</th>
            <th className={styles.th}>Order Type</th>
            <th className={styles.th}>Profit</th>
          </tr>
          {data.map((order, idx) => (
            <ClosedOrder
              order_type={order.order_type}
              comment={order.comment}
              profit={order.profit}
              symbol={order.symbol}
              ticket={order.ticket}
              time={order.time}
              volume={order.volume}
              key={idx}
            />
          ))}
        </table>
      </div>
    ) : (
      <div>Loading...</div>
    );
  return <div>{info}</div>;
}
