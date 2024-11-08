function initializeHrInfoForm() {
    const hrinfoForm = document.getElementById("hrinfo");// Check if the form is correctly found
    const empinfo = document.getElementById("empinfo");
    if (hrinfoForm) {
        hrinfoForm.addEventListener("submit", function(event) {
            event.preventDefault(); // Prevent the default form submission
            console.log("Form submitted");

            const email = document.getElementById("hrEmail").value;
            const password = document.getElementById("hrPassword").value;

            if ((email === "ajayhonrao12@gmail.com" || email === "karanyeole@gmail.com") && (password === "ajay&karan")) {
                window.location.href = "/hr_services";
            } else {
                console.log("Sorry, wrong password");
            }
        });
    } else {
        console.error("'hrinfo' form not found.");
    }

    if (empinfo) {
        empinfo.addEventListener("submit", function(event) {
            event.preventDefault(); // Prevent the default form submission
            console.log("Form submitted");

            const email = document.getElementById("existingEmployeeEmail").value;
            const password = document.getElementById("existingEmployeePassword").value;

            if ((email === "ajayhonrao12@gmail.com" || email === "karanyeole@gmail.com") && (password === "ajay&karan")) {
                window.location.href = "/emp_services";
            } else {
                console.log("Sorry, wrong password");
            }
        });
    } else {
        console.error("'hrinfo' form not found.");
    }
}

document.addEventListener("DOMContentLoaded", function() {
    initializeHrInfoForm(); // Call the function when the page is fully loaded
});
