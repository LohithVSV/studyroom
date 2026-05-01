console.log("app.js loaded")
function joinRoom(roomId) {
    fetch("https://studyroom-api-vcns.onrender.com/rooms/" + roomId + "/join", {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("token")
        }
    })
    .then(res => res.json())
    .then(data => {
        console.log(data)
        window.location.href = "room.html?id=" + roomId
    })
}
document.getElementById("browseroombtn").addEventListener("click",function(){
    document.getElementById("roomsSection").style.display = "block";
    fetch("https://studyroom-api-vcns.onrender.com/rooms")
    .then(function(response){
        return response.json()
    })
    .then(function(data){
        for (let room of data) {
        let card = document.createElement("div")
        card.innerHTML = `
            <h3>${room.title}</h3>
            <p>${room.description}</p>
            <button onclick="joinRoom(${room.id})">Join</button>
        `
        document.getElementById("roomsContainer").appendChild(card)
    }
    })
})

document.getElementById("createroombtn").addEventListener("click",function(){
    document.getElementById("createroommodal").style.display="block";
})
document.getElementById("submitroombtn").addEventListener("click",function(){
    let roomtitle=document.getElementById("roomtitle").value
    let roomdescription=document.getElementById("roomdescription").value
        fetch("https://studyroom-api-vcns.onrender.com/rooms",{
        method:"POST",
        headers:{ "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("token") 
        },
        body: JSON.stringify({ title: roomtitle, description: roomdescription })
    })
    .then(res => res.json())
    .then(data => {
        window.location.href = "index.html"
    })
    })
document.getElementById("closemodalbtn").addEventListener("click",function(){
        document.getElementById("createroommodal").style.display = "none"
    })
