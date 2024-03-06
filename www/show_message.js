window.addEventListener("DOMContentLoaded", () => {
    const messages = document.createElement("ul");
    document.body.appendChild(messages);

    var host = "localhost"
    var port = 5678

    const websocket = new WebSocket("ws://localhost:5678/");
    websocket.onopen = function(e) {
      websocket.send("Connection established with " + host + " on port " + port);
    };

    websocket.onmessage = ({ data }) => {
      const message = document.createElement("li");
      const content = document.createTextNode(data);
      message.appendChild(content);
      messages.appendChild(message);
      websocket.send(data)
    };

    websocket.onclose = event => {
      event.code === 1000
      event.reason === "Work complete"
      // event.wasClean === true (clean close)
    };

    websocket.onerror = function(error) {
      alert(error);
    };
  });