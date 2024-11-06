function loadHeader() {
    fetch("top.html")
        .then(response => response.text())
        .then(data => {
            document.getElementById("header-placeholder").innerHTML = data;
        })
        .catch(error => console.error("Error loading header:", error));
}

function loadFooter() {
    fetch("bottom.html")
        .then(response => response.text())
        .then(data => {
            document.getElementById("footer-placeholder").innerHTML = data;
        })
        .catch(error => console.error("Error loading footer:", error));
}

// Call these functions when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
    loadHeader();
    loadFooter();
});


document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("hrinfo").addEventListener("submit", function(event) {
        event.preventDefault();

        const email = document.getElementById("hrEmail").value;
        const password = document.getElementById("hrPassword").value;
        if ((email == "ajayhonrao12@gmail.com" || email == "karanyeole@gmail.com") && (password == "ajay&karan")) {
            console.log("welcome");
        } else {
            console.log("sorry wrong password");
        }
    });
});


// Function to dynamically load an external script
function loadBootstrap() {
    const script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js";
    script.integrity = "sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz";
    script.crossOrigin = "anonymous";
    document.head.appendChild(script);
}

// Load Bootstrap
loadBootstrap();
