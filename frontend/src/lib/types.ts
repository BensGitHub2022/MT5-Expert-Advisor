export type ClosedOrderType = {
  ticket: number;
  time: number;
  order_type: number;
  volume: number;
  profit: number;
  symbol: string;
  comment: string;
};

export type AccountType = {
  login: number;
  balance: number;
  profit: number;
  equity: number;
  server: string;
};

export type OpenOrderType = {
  ticket: number;
  time_setup: number;
  order_type: number;
  volume_current: number;
  stop_loss: number;
  take_profit: number;
  price_open: number;
  price_current: number;
  symbol: string;
  comment: string;
};
