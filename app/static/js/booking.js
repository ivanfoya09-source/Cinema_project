const selectedCount =
    document.getElementById("selectedCount");

const totalPrice =
    document.getElementById("totalPrice");

const hall = document.getElementById("cinemaHall");

const selectedSeats = [];

const selectedInfo = document.getElementById("selectedSeatsInfo");

function updateSelectedSeats() {

    if (selectedSeats.length === 0) {

        selectedInfo.textContent = "Нічого";

        selectedCount.textContent = "0";

        totalPrice.textContent = "0 грн";

        return;

    }

    selectedInfo.textContent = selectedSeats
        .map(s => `${s.row}-${s.seat}`)
        .join(", ");

    selectedCount.textContent = selectedSeats.length;

    const price = Number(sessionPrice);

    totalPrice.textContent =
        `${price * selectedSeats.length} грн`;

}

if (hall) {

    for (let row = 1; row <= hallRows; row++) {

        const rowDiv = document.createElement("div");
        rowDiv.className = "hall-row";

        const rowNumber = document.createElement("div");
        rowNumber.className = "row-number";
        rowNumber.innerHTML = row;

        rowDiv.appendChild(rowNumber);

        for (let seat = 1; seat <= hallSeats; seat++) {

            if (seat === 6) {

                const aisle = document.createElement("div");
                aisle.className = "aisle";

                rowDiv.appendChild(aisle);

            }

            const div = document.createElement("div");

            div.className = "seat";
            div.dataset.row = row;
            div.dataset.seat = seat;
            div.innerHTML = seat;

            div.onclick = () => {

                if (div.classList.contains("occupied")) {
                    return;
                }

                div.classList.toggle("selected");

                const index = selectedSeats.findIndex(
                    s => s.row === row && s.seat === seat
                );

                if (index === -1) {

                    selectedSeats.push({
                        row,
                        seat,
                    });

                } else {

                    selectedSeats.splice(index, 1);

                }

                updateSelectedSeats();

            };

            rowDiv.appendChild(div);

        }

        hall.appendChild(rowDiv);

    }

}

const bookButton = document.getElementById("bookButton");

if (bookButton) {

    bookButton.onclick = async () => {

        if (selectedSeats.length === 0) {
            alert("Оберіть хоча б одне місце");
            return;
        }

        const sessionId = Number(
            window.location.pathname.split("/").pop()
        );

        // 1. Тимчасове резервування через Redis
        const reserveResponse = await fetch("/reservations/", {

            method: "POST",

            credentials: "include",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                session_id: sessionId,

                seats: selectedSeats

            })

        });

        const reserveData = await reserveResponse.json();

        if (!reserveResponse.ok) {

            alert(reserveData.detail);

            return;

        }

        // 2. Створення бронювання
        const bookingResponse = await fetch("/bookings/", {

            method: "POST",

            credentials: "include",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                session_id: sessionId,

                seats: selectedSeats

            })

        });

        const bookingData = await bookingResponse.json();

        if (bookingResponse.ok) {

            alert("Бронювання успішне!");

            window.location = `/payment/${bookingData.id}`;

        } else {

            console.log(bookingData);
            alert(JSON.stringify(bookingData));

        }

    };

}

const sessionId = window.location.pathname.split("/").pop();

async function loadOccupiedSeats() {

    const response = await fetch(
        `/bookings/session/${sessionId}`
    );

    const data = await response.json();

    document.querySelectorAll(".seat").forEach(seat => {
        seat.classList.remove("occupied");
    });

    data.forEach(seat => {

        const element = document.querySelector(
            `.seat[data-row="${seat.row}"][data-seat="${seat.seat}"]`
        );

        if (element) {
            element.classList.add("occupied");
        }

    });

}

loadOccupiedSeats();

setInterval(loadOccupiedSeats, 5000);