function initializeHrInfoForm() {
    const hrinfoForm = document.getElementById("hrinfo");// Check if the form is correctly found
    if (hrinfoForm) {
        hrinfoForm.addEventListener("submit", function(event) {
            event.preventDefault(); // Prevent the default form submission
            console.log("Form submitted");

            const email = document.getElementById("hrEmail").value;
            const password = document.getElementById("hrPassword").value;

            if ((email === "ajayhonrao12@gmail.com" || email === "karanyeole@gmail.com") && (password === "ajay&karan")) {
                console.log("Welcome");
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
