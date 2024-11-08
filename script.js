function loadHeader(callback) {
    fetch("top.html")
        .then(response => response.text())
        .then(data => {
            document.getElementById("header-placeholder").innerHTML = data;
            if (callback) callback(); // Run callback after header loads
        })
        .catch(error => {
            console.error("Error loading the header:", error);
        });
}

function loadFooter(callback) {
    fetch("bottom.html")
        .then(response => response.text())
        .then(data => {
            document.getElementById("footer-placeholder").innerHTML = data;
            if (callback) callback(); // Run callback after footer loads
        })
        .catch(error => console.error("Error loading footer:", error));
}

// Function to initialize the hrinfo form after loading header and footer
function initializeHrInfoForm() {
    const hrinfoForm = document.getElementById("hrinfo");
    if (hrinfoForm) {
        hrinfoForm.addEventListener("submit", function(event) {
            event.preventDefault();
            const email = document.getElementById("hrEmail").value;
            const password = document.getElementById("hrPassword").value;
            if ((email === "ajayhonrao12@gmail.com" || email === "karanyeole@gmail.com") && (password === "ajay&karan")) {
                console.log("welcome");
            } else {
                console.log("sorry wrong password");
            }
        });
    } else {
        console.error("'hrinfo' not found.");
    }
}

// Load header, footer, and initialize hrinfo form
document.addEventListener("DOMContentLoaded", function() {
    loadHeader(() => {
        loadFooter(initializeHrInfoForm);
    });
});

// Load Bootstrap
function loadBootstrap() {
    const script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js";
    script.integrity = "sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz";
    script.crossOrigin = "anonymous";
    document.head.appendChild(script);
}

loadBootstrap();