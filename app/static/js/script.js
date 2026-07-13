const logoutButton=document.getElementById("logoutButton");

if(logoutButton){

    logoutButton.onclick=()=>{

        localStorage.removeItem("access_token");

        localStorage.removeItem("refresh_token");

        window.location="/login";

    };

}


const loginForm=document.getElementById("loginForm");

if(loginForm){

loginForm.addEventListener("submit",async(e)=>{

e.preventDefault();

const response=await fetch("/auth/login",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({

email:document.getElementById("email").value,

password:document.getElementById("password").value

})

});

const data=await response.json();

if(response.ok){

localStorage.setItem("access_token",data.access_token);

localStorage.setItem("refresh_token",data.refresh_token);

window.location="/profile";

}else{

alert(data.detail);

}

});

}

const hall=document.getElementById("cinemaHall");

const selectedSeats=[];

if(hall){

for(let row=1;row<=8;row++){

for(let seat=1;seat<=10;seat++){

const div=document.createElement("div");

div.className="seat";

div.dataset.row=row;

div.dataset.seat=seat;

div.innerHTML=row+"-"+seat;

div.onclick=()=>{

if(div.classList.contains("occupied")){

return;

}

div.classList.toggle("selected");

const index=selectedSeats.findIndex(

s=>s.row==row&&s.seat==seat

);

if(index==-1){

selectedSeats.push({

row,

seat

});

}else{

selectedSeats.splice(index,1);

}

};

hall.appendChild(div);

}

}

}

const bookButton = document.getElementById("bookButton");

if (bookButton) {

    bookButton.onclick = async () => {

        if (selectedSeats.length === 0) {
            alert("Оберіть хоча б одне місце");
            return;
        }

        const token = localStorage.getItem("access_token");

        if (!token) {
            alert("Спочатку увійдіть в акаунт");
            window.location = "/login";
            return;
        }

        // Поки що беремо session_id із URL:
        // /booking/1 -> sessionId = 1
        const sessionId = window.location.pathname.split("/").pop();

        const response = await fetch("/bookings/", {

            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },

            body: JSON.stringify({
                session_id: Number(sessionId),
                seats: selectedSeats
            })

        });

        const data = await response.json();

        if (response.ok) {

            alert("Бронювання успішне!");

            window.location = "/profile";

        } else {

            alert(data.detail);

        }

    };

}

const sessionId = window.location.pathname.split("/").pop();

fetch(`/bookings/session/${sessionId}`)
.then(response => response.json())
.then(data => {

    data.forEach(seat => {

        const element = document.querySelector(

            `.seat[data-row="${seat.row}"][data-seat="${seat.seat}"]`

        );

        if (element) {

            element.classList.add("occupied");

        }

    });

});


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