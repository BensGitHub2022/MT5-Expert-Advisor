# BBSTrader API Contract

## Objects

### Account object
```
{
  login: integer
  balance: float
  profit: float
  equity: float
  server: string
}
```

### ClosedOrder object
```
{
  ticket: integer
  time: milliseconds since epoch
  order_type: integer
  volume: float
  profit: float
  symbol: string
}
```

### OpenOrder object
```
{
    ticket: integer
    time_setup: milliseconds since epoch
    order_type: integer
    volume_current: float
    stop_loss: float
    take_profit: float
    price_open: float
    price_current: float
    symbol: string
}
```

## Endpoints 
### GET /orders-open
  Returns all open orders.
* **URL Params**  
  None
* **Data Params**  
  None
* **Headers**  
  Content-Type: application/json  
* **Success Response:**  
* **Code:** 200  
  **Content:**  
```
{
  orders: [
           {<OpenOrder_Object>},
           {<OpenOrder_Object>},
           {<OpenOrder_Object>}
         ]
}
```
----
### GET /orders-closed
  Returns all historical orders.
* **URL Params**  
  None
* **Data Params**  
  None
* **Headers**  
  Content-Type: application/json  
* **Success Response:**  
* **Code:** 200  
  **Content:**  
```
{
  orders: [
           {<ClosedOrder_Object>},
           {<ClosedOrder_Object>},
           {<ClosedOrder_Object>}
         ]
}
```
----
### GET /account-info
  Returns account data for the currently-connected MT5 account.
* **URL Params**  
  None
* **Data Params**  
  None
* **Headers**  
  Content-Type: application/json  
* **Success Response:**  
* **Code:** 200  
  **Content:**  
```
{
  account: <Account_Object>
}
```
----
### POST /create
  Create a new trade bot.
* **URL Params**  
  None
* **Data Params**  
  symbol: the symbol to trade on (e.g., BTCUSD)

  ema_short: the short term EMA boundary

  ema_long: the long term EMA boundary
* **Headers**  
  Content-Type: application/json  
* **Success Response:**  
* **Code:** 200  
  **Content:**  
```
{
  message: "Trade bot initialized on symbol `symbol` with a short term EMA boundary of `ema_short` and a long term EMA boundary of `ema_long`
}
```
* **Code:** 400  
  **Content:**
```
{
    error: "Trade bot could not be initialized"
}
```
----