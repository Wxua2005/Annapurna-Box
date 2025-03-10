const signupButton = document.querySelector(".signup-text");
const signinButton = document.querySelector(".sign-in-button");
const profileButton = document.getElementById("profile-btn");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");

signupButton.addEventListener("click", function (event) {
    event.preventDefault();
    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();

    if (email && password) {
        let users = JSON.parse(localStorage.getItem("users")) || {};
        if (users[email]) {
            alert("User already exists!");
        } else {
            users[email] = { password, statistics: { donations: 0, visits: 1 } };
            localStorage.setItem("users", JSON.stringify(users));
            alert("Sign-up successful! You can now log in.");
        }
    } else {
        alert("Please enter email and password.");
    }
});

signinButton.addEventListener("click", function (event) {
    event.preventDefault();
    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();

    let users = JSON.parse(localStorage.getItem("users")) || {};
    if (users[email] && users[email].password === password) {
        users[email].statistics.visits += 1;
        localStorage.setItem("users", JSON.stringify(users));
        alert("Login successful!");
    } else {
        alert("Invalid credentials!");
    }
});

profileButton.addEventListener("click", function () {
    const email = emailInput.value.trim();
    let users = JSON.parse(localStorage.getItem("users")) || {};

    if (users[email]) {
        alert(`User: ${email}\nDonations: ${users[email].statistics.donations}\nVisits: ${users[email].statistics.visits}`);
    } else {
        alert("No user data found! Log in first.");
    }
});