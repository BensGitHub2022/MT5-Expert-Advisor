//import Chart from 'chart.js/auto'

var datasets_data = []
var data_labels = []

ctx = document.getElementById("my_chart");
my_chart = new Chart(ctx, 
    {
        type: 'line',
        data: {
            labels: data_labels,
            datasets: [
                {
                    label: 'Balance by Trade',
                    data: datasets_data
                }
            ]
        },
        options: {
            parsing: {
              xAxisKey: 'timestamp',
              yAxisKey: 'balance'
            }
        }
    }
);

window.addEventListener("DOMContentLoaded", () => {

    const websocket = new WebSocket("ws://localhost:5678/");
    websocket.onmessage = function(data) {
      arr_data = JSON.parse(data.data)
      var data_obj = process_received_messages(arr_data)
      try {
        data_labels.push(data_obj.timestamp)
        datasets_data.push(data_obj)
        my_chart.update()
      } catch (e) {
        console.log(e)
      }
    };

    websocket.onclose = function(event) {
      websocket.close(1000, "Work complete");
      event.code === 1000
      event.reason === "Work complete"
      event.wasClean === true
    };
  });
  
  function process_received_messages(data) {
      const arr_data = data.map(row => ({
        timestamp: (row['timestamp']),
        balance: (row['balance']),
        side: (row['side'])
      }));
      //Example data_obj: {timestamp: '2023-12-28 07:29:36.351481+00:00', balance: 42841.6, side: "SELL"}
      data_obj = {timestamp: Date(arr_data[0].timestamp), balance: arr_data[0].balance, side: arr_data[0].side}
      return data_obj
  };