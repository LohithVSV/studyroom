function startProgress() {
    const bar = document.getElementById("progressbar");
    bar.style.display = "block";
    bar.style.width = "0%";
    
    setTimeout(() => {
        bar.style.width = "75%";
    }, 75);  // tiny delay in milliseconds
}

function stopProgress() {
    const bar = document.getElementById("progressbar");
    bar.style.display="block";
    bar.style.width = "100%";

    setTimeout(()=> {
        bar.style.width ="0%";
        bar.style.display = "none";
    },400);
}

