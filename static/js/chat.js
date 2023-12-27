const id = JSON.parse(document.getElementById("json-username").textContent);
const message_username = JSON.parse(
  document.getElementById("json-message-username").textContent
);

const socket = new WebSocket(
  "ws://" + window.location.host + "/ws/" + id + "/"
);

socket.onopen = function (e) {
  console.log("Connection established");
};

socket.onclose = function (e) {
  console.log("Connection lost");
};

socket.onerror = function (e) {
  console.log(e);
};

socket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  const message = data.message;
  if (message.sender == message_username) {
    document.querySelector("#chat-body").innerHTML += `
        <tr>
            <td>
                <p class="bg-success p-2 mt-2 mr-5 shadow-sm text-white float-right rounded">
                    ${message.message}
                </p>
            </td>
            <td>
                <p><small class="p-1 shadow-sm">${message.timestamp.substring(
                  11,
                  16
                )}</small>
                </p>
            </td>
        </tr>
        `;
  } else {
    document.querySelector("#chat-body").innerHTML += `<tr>
    <td>
        <p class="bg-primary p-2 mt-2 mr-5 shadow-sm text-white float-left rounded">
            ${data.message.message}
        </p>
    </td>
    <td>
        <p><small class="p-1 shadow-sm">${message.timestamp.substring(
          11,
          16
        )}</small>
        </p>
    </td>
</tr>
        `;
  }
};

document.querySelector("#chat-message-submit").onclick = function (e) {
  const message_input = document.querySelector("#message_input");
  const message = message_input.value;

  socket.send(
    JSON.stringify({
      message: message,
      username: message_username,
    })
  );
  message_input.value = "";
};