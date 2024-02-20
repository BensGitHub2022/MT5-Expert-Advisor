import type { ClosedOrderType } from "../types";

export function ClosedOrder(props: ClosedOrderType) {
  return (
    <tr>
      <td>{new Date(props.time).toLocaleDateString()}</td>
      <td>{props.ticket}</td>
      <td>{props.symbol || "No symbol"}</td>
      <td>{props.volume}</td>
      <td>{props.comment || "No comment"}</td>
      <td>{props.order_type}</td>
      <td>
        {props.profit > 0 ? "+" : "-"}${props.profit}
      </td>
    </tr>
  );
}
