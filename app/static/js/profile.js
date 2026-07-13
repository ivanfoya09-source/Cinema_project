const profileForm = document.getElementById("profileForm");

if (profileForm) {

    profileForm.onsubmit = async (e) => {

        e.preventDefault();

        const token = localStorage.getItem("access_token");

        const response = await fetch("/users/me", {

            method: "PUT",

            headers: {

                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`

            },

            body: JSON.stringify({

                first_name: document.getElementById("first_name").value,
                last_name: document.getElementById("last_name").value,
                phone: document.getElementById("phone").value,
                city: document.getElementById("city").value,
                birth_date: document.getElementById("birth_date").value

            })

        });

        if (response.ok) {

            alert("Профіль успішно оновлено!");

            location.reload();

        } else {

            alert("Помилка оновлення профілю");

        }

    };

}