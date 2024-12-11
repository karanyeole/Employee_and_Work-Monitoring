function initializeHrInfoForm() {
    const hrinfoForm = document.getElementById("hrinfo");
    const empinfo = document.getElementById("empinfo");
    const servicesLink = document.getElementById("services-link");
    const hr_servicesLink = document.getElementById("services-link-hr");
    const emp_servicesLink = document.getElementById("services-link-emp");
    const logoutItem = document.getElementById("logout-item");
    const signupItem = document.getElementById("signupDropdown");

    // Check for HR login status in sessionStorage
    if (sessionStorage.getItem("isHrLoggedIn") === "true") {
        servicesLink.style.display = "none"; // Hide the "Services" link if logged in as HR
        if (hr_servicesLink) {
            hr_servicesLink.style.display = "block"; // Show the HR-specific Services link
        }
        // Hide Signup and show Logout button
        signupItem.style.display = "none"; // Hide the signup dropdown
        logoutItem.style.display = "block"; // Show the logout button
    }

    // Check for Employee login status in sessionStorage
    if (sessionStorage.getItem("isEmpLoggedIn") === "true") {
        servicesLink.style.display = "none"; // Hide the "Services" link if logged in as an Employee
        if (emp_servicesLink) {
            emp_servicesLink.style.display = "block"; // Show the Employee-specific Services link
        }
        // Hide Signup and show Logout button
        signupItem.style.display = "none"; // Hide the signup dropdown
        logoutItem.style.display = "block"; // Show the logout button
    }

    // HR form submission logic
    if (hrinfoForm) {
        hrinfoForm.addEventListener("submit", function(event) {
            event.preventDefault();

            const email = document.getElementById("hrEmail").value;
            const password = document.getElementById("hrPassword").value;

            if ((email === "ajayhonrao12@gmail.com" || email === "karanyeole@gmail.com") && password === "ajay&karan") {
                servicesLink.style.display = "none";
                if (hr_servicesLink) {
                    hr_servicesLink.style.display = "block"; // Show HR Services link
                }
                sessionStorage.setItem("isHrLoggedIn", "true"); // Store HR login status
                sessionStorage.removeItem("isEmpLoggedIn"); // Remove employee login status if set

                // Hide Signup and show Logout button
                signupItem.style.display = "none"; // Hide the signup dropdown
                logoutItem.style.display = "block"; // Show the logout button

                setTimeout(() => {
                    window.location.href = "/hr_services";
                }, 100);
            } else {
                console.log("Sorry, wrong password");
            }
        });
    } else {
        console.error("'hrinfo' form not found.");
    }

    // Employee form submission logic
    if (empinfo) {
        empinfo.addEventListener("submit", async function(event) {
            event.preventDefault();
    
            const email = document.getElementById("existingEmployeeEmail").value;
            const password = document.getElementById("existingEmployeePassword").value;
    
            // Send email and password to the server to validate
            try {
                const response = await fetch('/validate_employee', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });
                
                const data = await response.json();
    
                if (data.success) {
                    // Hide services link and show employee services
                    servicesLink.style.display = "none";
                    if (emp_servicesLink) {
                        emp_servicesLink.style.display = "block";
                    }
                    
                    sessionStorage.setItem("isEmpLoggedIn", "true");
                    sessionStorage.removeItem("isHrLoggedIn");
                    
                    signupItem.style.display = "none";
                    logoutItem.style.display = "block";
                    
                    window.location.href = "/emp_services";
                } else {
                    console.log("Invalid email or employee ID");
                }
            } catch (error) {
                console.error("Error:", error);
            }
        });
    } else {
        console.error("'empinfo' form not found.");
    }
    
}

document.addEventListener("DOMContentLoaded", function() {
    initializeHrInfoForm();
});

function logout() {
    sessionStorage.removeItem("isHrLoggedIn");
    sessionStorage.removeItem("isEmpLoggedIn");
    // Hide the logout button and show the signup dropdown again
    document.getElementById("logout-item").style.display = "none"; // Hide the logout button
    document.getElementById("signupDropdown").style.display = "block"; // Show the signup dropdown
    window.location.href = "/"; // Redirect to homepage or login page
}


// Toggle Employee Form
function toggleEmployeeForm() {
    const form = document.getElementById("employeeForm");
    form.style.display = form.style.display === "none" ? "block" : "none";
}

// Add the form toggling function call in initializeHrInfoForm if required
initializeHrInfoForm();

document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form[data-url]");
    
    if (form) {
        form.addEventListener("submit", function(event) {
            event.preventDefault();

            const formData = new FormData(this);
            const url = form.getAttribute("data-url");

            fetch(url, {
                method: "POST",
                body: formData
            })
            .then(response => response.json()) // Parse JSON response directly
            .then(data => {
                if (data.success) {
                    alert("Employee added successfully! Employee ID: " + data.employee_id);
                    document.getElementById("employee-form").style.display = "none"; 
                    document.getElementById("img_cap_data").style.display = "block"; 

                } else {
                    alert("An error occurred. Please try again.");
                }
            })
            .catch(error => {
                console.error("Fetch error:", error);
                alert("An error occurred. Please try again.");
            });
        });
    }
});