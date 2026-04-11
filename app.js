document.getElementById("browseroombtn").addEventListener("click",function(){
    document.getElementById("roomsSection").style.display = "block";
    fetch("https://studyroom-api-vcns.onrender.com/rooms")
    .then(function(response){
        return response.json()
    })
    .then(function(data){
        console.log(data)
    })
})

