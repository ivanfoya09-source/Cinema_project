console.log("main.js завантажився");

const logoutButton = document.getElementById("logoutButton");

console.log(logoutButton);

if (logoutButton) {

    logoutButton.onclick = async (e) => {

        console.log("Натиснули Logout");

        e.preventDefault();

        const response = await fetch("/auth/logout", {
            method: "POST"
        });

        console.log(response.status);

        if (response.ok) {

            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");

            window.location = "/login";

        } else {

            alert("Помилка виходу");

        }

    };

}