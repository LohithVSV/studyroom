document.getElementById("signupform").addEventListener("submit", function(event) {
    event.preventDefault()
    let username = document.getElementById("username").value
    let password = document.getElementById("password").value
    let email = document.getElementById("email").value

    fetch("https://studyroom-api-2.onrender.com/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: username, email: email, password: password })
    })
    .then(res => res.json())
    .then(data => {
        if (data.detail) {
            document.getElementById("errorMsg").textContent = data.detail;
        } else {
            window.location.href = "login.html"
        }
    })

})