import type { ClosedOrderType, OpenOrderType } from "../../lib/types";
import { getFormattedCurrency } from "../../lib/util";

import styles from "./order.module.css";

export function ClosedOrder(props: ClosedOrderType) {
  return (
    <tr>
      <td>{new Date(props.time).toLocaleDateString()}</td>
      <td>{props.ticket}</td>
      <td>{props.symbol || "No symbol"}</td>
      <td>{props.volume}</td>
      <td>{props.comment || "No comment"}</td>
      <td>{props.order_type}</td>
      <td>{getFormattedCurrency(props.profit)}</td>
    </tr>
  );
}

export function ClosedOrderWrapper({ children }: { children: JSX.Element[] }) {
  return (
    <div>
      <h1>Order History:</h1>
      <hr />
      <table>
        <thead>
          <tr>
            <th className={styles.th}>Transaction Date</th>
            <th className={styles.th}>Ticket Number</th>
            <th className={styles.th}>Symbol</th>
            <th className={styles.th}>Volume</th>
            <th className={styles.th}>Comment</th>
            <th className={styles.th}>Order Type</th>
            <th className={styles.th}>Profit</th>
          </tr>
        </thead>
        <tbody>{children}</tbody>
      </table>
      <hr />
    </div>
  );
}

export function OpenOrder(props: OpenOrderType) {
  return (
    <tr>
      <td>{new Date(props.time_setup).toLocaleDateString()}</td>
      <td>{props.ticket}</td>
      <td>{props.symbol}</td>
      <td>{props.volume_current}</td>
      <td>{props.comment || "No comment"}</td>
      <td>{props.order_type}</td>
      <td>{props.price_open}</td>
      <td>{props.price_current}</td>
      <td>{props.stop_loss}</td>
      <td>{props.take_profit}</td>
    </tr>
  );
}

export function OpenOrderWrapper({ children }: { children: JSX.Element[] }) {
  return (
    <div>
      <h1>Open Orders:</h1>
      <hr />
      <table>
        <thead>
          <tr>
            <th className={styles.th}>Opened At</th>
            <th className={styles.th}>Ticket</th>
            <th className={styles.th}>Symbol</th>
            <th className={styles.th}>Current Volume</th>
            <th className={styles.th}>Comment</th>
            <th className={styles.th}>Order Type</th>
            <th className={styles.th}>Opening Price</th>
            <th className={styles.th}>Current Price</th>
            <th className={styles.th}>Stop Loss</th>
            <th className={styles.th}>Take Profit</th>
          </tr>
        </thead>
        <tbody>{children}</tbody>
      </table>
      <hr />
    </div>
  );
}
