import { AccountType } from "../../lib/types";
import { getFormattedCurrency } from "../../lib/util";

import styles from "./acc.module.css";

export default function Account(props: AccountType) {
  return (
    <div className={styles.container}>
      <div>Login({props.login})</div>
      <div>Balance({getFormattedCurrency(props.balance)})</div>
      <div>Equity({getFormattedCurrency(props.equity)})</div>
      <div>Profit({getFormattedCurrency(props.profit)})</div>
      <div>Server({props.server})</div>
    </div>
  );
}
