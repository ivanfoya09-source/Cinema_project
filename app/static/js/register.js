const registerForm = document.getElementById("registerForm");

if (registerForm) {

    registerForm.addEventListener("submit", async (e) => {

        e.preventDefault();

        const response = await fetch("/auth/register", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                username: document.getElementById("username").value,

                email: document.getElementById("email").value,

                password: document.getElementById("password").value

            })

        });

        const data = await response.json();

        if (response.ok) {

            alert("Реєстрація успішна!");

            window.location = "/login";

        } else {

            alert(data.detail || "Помилка реєстрації");

        }

    });

}