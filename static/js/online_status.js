const loggedin_user= JSON.parse(document.getElementById('json-message-username').textContent)

const online_status = new WebSocket(
    "ws://" + window.location.host + "/ws/online/"
)
online_status.onopen= function(e){
    console.log("Connected to online consumer")
    online_status.send(JSON.stringify({
        'username':loggedin_user,
        'type':'open'
    }))
}


online_status.onclose= function(e){
    console.log("Disconnected from online consumer")
}
