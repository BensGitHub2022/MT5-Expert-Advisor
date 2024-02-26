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
### GET /orders-open/:ticket
  Returns the open order with the given ticket number.
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
  order: <OpenOrder_Object>
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
### GET /orders-closed/:ticket
  Returns the closed order with the given ticket number.
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
  order: <ClosedOrder_Object>
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