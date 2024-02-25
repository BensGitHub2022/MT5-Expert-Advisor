import { mockAccount, mockClosedOrders, mockOpenorders } from "./mock";

export async function getClosedOrders() {
  if (import.meta.env.MODE === "development") {
    return mockClosedOrders;
  } else {
    try {
      const response = await fetch("http://localhost:5000/orders-closed");
      const data = await response.json();
      return data.orders;
    } catch (error) {
      console.log(error);
      throw error;
    }
  }
}

export async function getAccount() {
  if (import.meta.env.MODE === "development") {
    return mockAccount;
  } else {
    try {
      const response = await fetch("http://localhost:5000/account");
      const data = await response.json();
      return data.account;
    } catch (error) {
      console.log(error);
      throw error;
    }
  }
}

export async function getOpenOrders() {
  if (import.meta.env.MODE === "development") {
    return mockOpenorders;
  } else {
    try {
      const response = await fetch("http://localhost:5000/orders-open");
      const data = await response.json();
      return data.orders;
    } catch (error) {
      console.log(error);
      throw error;
    }
  }
}
