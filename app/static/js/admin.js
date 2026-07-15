const movieForm = document.getElementById("movieForm");
const submitButton = document.getElementById("movieSubmitButton");

if (movieForm) {

    movieForm.addEventListener("submit", async (e) => {

        e.preventDefault();

        const token = localStorage.getItem("access_token");

        let posterUrl = "";

        const posterFile = document.getElementById("poster_file").files[0];

        if (posterFile) {

            const formData = new FormData();
            formData.append("file", posterFile);

            const uploadResponse = await fetch("/upload/poster", {
                method: "POST",
                body: formData
            });

            if (!uploadResponse.ok) {
                alert("Не вдалося завантажити постер");
                return;
            }

            const uploadData = await uploadResponse.json();
            posterUrl = uploadData.poster_url;

        } else {

            posterUrl = document.getElementById("poster_url").value;

        }

        const editing = movieId.value !== "";

        const url = editing
            ? `/admin/movies/${movieId.value}`
            : "/admin/movies";

        const method = editing
            ? "PUT"
            : "POST";

        const response = await fetch(url, {

            method,

            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },

            body: JSON.stringify({

                title: document.getElementById("title").value,

                original_title: document.getElementById("original_title").value,

                description: document.getElementById("description").value,

                genre_id: Number(document.getElementById("genre_id").value),

                director: document.getElementById("director").value,

                country: document.getElementById("country").value,

                release_year: Number(document.getElementById("release_year").value),

                duration: Number(document.getElementById("duration").value),

                age_limit: Number(document.getElementById("age_limit").value),

                rating: Number(document.getElementById("rating").value),

                poster_url: posterUrl,

                trailer_url: document.getElementById("trailer_url").value,

                is_active: true

            })

        });

        const data = await response.json();

        if (response.ok) {

            alert(
                editing
                    ? "Фільм успішно оновлено!"
                    : "Фільм успішно додано!"
            );

            location.reload();

        } else {

            alert(data.detail);

        }

    });

}


const deleteButtons = document.querySelectorAll(".deleteMovie");

deleteButtons.forEach(button => {

    button.addEventListener("click", async () => {

        if (!confirm("Видалити фільм?")) {

            return;

        }

        const token = localStorage.getItem("access_token");

        const movieId = button.dataset.id;

        const response = await fetch(`/admin/movies/${movieId}`, {

            method: "DELETE",

            headers: {
                "Authorization": `Bearer ${token}`
            }

        });

        if (response.ok) {

            location.reload();

        } else {

            alert("Не вдалося видалити фільм");

        }

    });

});

const genreForm = document.getElementById("genreForm");

if (genreForm) {

    genreForm.addEventListener("submit", async (e) => {

        e.preventDefault();

        const token = localStorage.getItem("access_token");

        const response = await fetch("/admin/genres", {

            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },

            body: JSON.stringify({

                name: document.getElementById("genreName").value

            })

        });

        const data = await response.json();

        if (response.ok) {

            alert("Жанр додано!");

            location.reload();

        } else {

            alert(data.detail);

        }

    });

}

const hallForm = document.getElementById("hallForm");

if (hallForm) {

    hallForm.addEventListener("submit", async (e) => {

        e.preventDefault();

        const token = localStorage.getItem("access_token");

        const response = await fetch("/admin/halls", {

            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },

            body: JSON.stringify({

                name: document.getElementById("hallName").value,

                hall_type: document.getElementById("hallType").value,

                description: document.getElementById("hallDescription").value,

                rows: Number(document.getElementById("hallRows").value),

                seats_per_row: Number(document.getElementById("hallSeats").value)

            })

        });

        const data = await response.json();

        if (response.ok) {

            alert("Зал успішно додано!");

            location.reload();

        } else {

            alert(data.detail);

        }

    });

}

const sessionForm = document.getElementById("sessionForm");

if (sessionForm) {

    sessionForm.addEventListener("submit", async (e) => {

        e.preventDefault();

        const token = localStorage.getItem("access_token");

        const response = await fetch("/sessions", {

            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },

            body: JSON.stringify({

                movie_id: Number(document.getElementById("sessionMovie").value),

                hall_id: Number(document.getElementById("sessionHall").value),

                start_time: document.getElementById("startTime").value,

                end_time: document.getElementById("endTime").value,

                language: "Українська",

                subtitle: false,

                price: Number(document.getElementById("sessionPrice").value),

                available_seats: 80,

                format: document.getElementById("sessionFormat").value,

                is_active: true

            })

        });

        const data = await response.json();

        if (response.ok) {

            alert("✅ Сеанс успішно створено!");

            location.reload();

        } else {

            console.log(data);

            alert(data.detail || "Помилка створення сеансу");

        }

    });

}

const movieId = document.getElementById("movieId");

document.querySelectorAll(".editMovie").forEach(button => {

    button.addEventListener("click", () => {

        movieId.value = button.dataset.id;

        document.getElementById("title").value =
            button.dataset.title;

        document.getElementById("original_title").value =
            button.dataset.original;

        document.getElementById("description").value =
            button.dataset.description;

        document.getElementById("director").value =
            button.dataset.director;

        document.getElementById("country").value =
            button.dataset.country;

        document.getElementById("release_year").value =
            button.dataset.year;

        document.getElementById("duration").value =
            button.dataset.duration;

        document.getElementById("age_limit").value =
            button.dataset.age;

        document.getElementById("rating").value =
            button.dataset.rating;

        document.getElementById("genre_id").value =
            button.dataset.genre;

        document.getElementById("trailer_url").value =
            button.dataset.trailer;

        document.getElementById("poster_url").value =
            button.dataset.poster;

        submitButton.innerHTML =
            "💾 Зберегти зміни";

        window.scrollTo({

            top: 0,

            behavior: "smooth"

        });

    });

});