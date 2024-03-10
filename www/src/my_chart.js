import Chart from 'chart.js/auto'

window.addEventListener("DOMContentLoaded", () => {
    var host = "localhost"
    var port = 5678

    // {time: '2023-02-27 19:56:00', balance: 101142.4471284954},
    // {time: '2023-02-28 20:57:59', balance: 101107.5978952566}
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
                  xAxisKey: 'time',
                  yAxisKey: 'balance'
                }
            }
        }
    );

    const websocket = new WebSocket("ws://localhost:5678/");
    websocket.onopen = function(e) {
      websocket.send("Connection established with " + host + " on port " + port);
    };

    websocket.onmessage = function(data) {
      websocket.send(data.data)
      arr_data = JSON.parse(data.data)
      var data_obj = process_received_messages(arr_data)
      //my_chart.data.datasets[0].data.push({time:received_messages[0].time,balance:received_messages[0].balance})
      data_labels.push(data_obj.time)
      datasets_data.push(data_obj)
      my_chart.update()
    };

    websocket.onclose = function(event) {
      event.code === 1000
      event.reason === "Work complete"
    };

    websocket.onerror = function(error) {
      alert(error);
    };
  });
  
  function process_received_messages(data) {
      const arr_data = data.map(row => ({
        time: (row['time']),
        balance: (row['balance'])
      }));
      data_obj = {time: Date(arr_data[0].time), balance: arr_data[0].balance}
      received_messages.push(data_obj)
      return data_obj
  }

  export var received_messages = []