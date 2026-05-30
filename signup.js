document.getElementById("signupform").addEventListener("submit", function(event) {
    event.preventDefault()
    let username = document.getElementById("username").value
    let password = document.getElementById("password").value
    let email = document.getElementById("email").value
    startProgress();
    fetch("https://studyroom-api-2.onrender.com/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: username, email: email, password: password })
    })
    .then(res => {
        return res.json().then(data => {
            if (!res.ok) throw data;
            return data;
        });
    })
    .then(data => {
        stopProgress();
        if (data.detail) {
            const message = data.detail.includes("exists")
                ? "Invalid inputs: maybe username or email already exists"
                : data.detail;
            document.getElementById("errorMsg").textContent = message;
        } else {
            window.location.href = "login.html"
        }
    })
    .catch(error => {
        stopProgress();
        console.error("Signup error:", error);
        const message = error?.detail || error?.message || "Signup failed. Please try again.";
        document.getElementById("errorMsg").textContent = message;
    });

});