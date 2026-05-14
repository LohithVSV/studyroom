let params = new URLSearchParams(window.location.search)
let roomId = params.get("id")
console.log(roomId)

fetch("https://studyroom-api-vcns.onrender.com/rooms/" + roomId)
.then(res =>res.json())
.then(data => {
    console.log(data)
    document.getElementById("roomTitle").innerText = data.title
})

let timerRunning = false

document.getElementById("startBtn").addEventListener("click", function() {
    if (timerRunning) return
    timerRunning = true
    document.getElementById("startBtn").style.display = "none"

    let timeset = document.getElementById("timeset").value
    let seconds = timeset * 60

    let timer = setInterval(function() {
        seconds = seconds - 1

        if (seconds <= 0) {
            clearInterval(timer)
            document.getElementById("timerDisplay").innerText = "Time's up! 🔥"
            return
        }

        let mins = Math.floor(seconds / 60)
        let secs = String(seconds % 60).padStart(2, "0")
        document.getElementById("timerDisplay").innerText = mins + ":" + secs
    }, 1000)

})

document.getElementById("leaveBtn").addEventListener("click", function() {
    window.location.href = "index.html"
})

fetch("https://studyroom-api-vcns.onrender.com/rooms/" + roomId + "/members")
.then(res => res.json())
.then(data => {
    let count = data.member_count
    let text = count === 1 ? "member" : "members"
    document.getElementById("memberCount").innerText = "👥 " + count + " " + text
})

fetch("https://studyroom-api-vcns.onrender.com/rooms/" + roomId + "/notes")
.then(res => res.json())
.then(function(data) {
    let notesList=document.getElementById("notesList")
    for(let note of data){
        let noteElement=document.createElement("div")
        noteElement.innerText=note.content
        notesList.appendChild(noteElement)
    }
})   

document.getElementById("addNoteBtn").addEventListener("click",function(){
    let noteContent=document.getElementById("noteInput").value
    fetch("https://studyroom-api-vcns.onrender.com/rooms/" + roomId + "/notes", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("token")
        },
        body: JSON.stringify({ content: noteContent })
    })
    .then(res => res.json())
    .then(data => {
        let notesList = document.getElementById("notesList")
        let noteElement = document.createElement("div")
        noteElement.innerText = data.content
        notesList.appendChild(noteElement)
        document.getElementById("noteInput").value = ""
    })
})


