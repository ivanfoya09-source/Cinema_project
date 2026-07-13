const loginForm = document.getElementById("loginForm");

if (loginForm) {

    loginForm.addEventListener("submit", async (e) => {

        e.preventDefault();

        const response = await fetch("/auth/login", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                email: document.getElementById("email").value,
                password: document.getElementById("password").value
            })

        });

        const data = await response.json();

        if (response.ok) {

            window.location = "/profile";

        } else {

            alert(data.detail);

        }

    });

}