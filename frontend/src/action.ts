import type { ClosedOrderType } from "./types";

type ClosedOrderResponse = {
  orders: ClosedOrderType[];
};

export async function getClosedOrders() {
  try {
    const response = await fetch("http://localhost:5000/orders-closed");
    const json: ClosedOrderResponse = await response.json();
    return json.orders;
  } catch (err) {
    throw err;
  }
}
