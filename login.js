document.getElementById("loginform").addEventListener("submit",function(event){
    event.preventDefault()
    console.log("submitted")
    let username = document.getElementById("username").value
    let password = document.getElementById("password").value

    fetch("https://studyroom-api-2.onrender.com/login", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: `username=${username}&password=${password}`
})
.then(res => res.json())
.then(data => {
    if (data.access_token) {
        console.log(data)
        localStorage.setItem("token", data.access_token)
        window.location.href = "index.html"
    } else {
        document.getElementById("errorMsg").textContent = data.detail;
    }
})
})