'use strict'
// alert("you connected to js")
const deleteResBtns = document.querySelectorAll('.delete-reservation');
// console.log(deleteResBtns);
for (let delBtn of deleteResBtns) {
    // console.log(delBtn);
    delBtn.addEventListener("click", (evt) => {
        const res_id = evt.target.value;
    console.log(res_id);

        fetch(`http:/user/reservation/delete/${res_id}`, {
            method: 'POST',
        })
            .then(res => res.json()) // or res.json()
            .then(res =>{
                console.log(res);
                const reservationId =res["reservation_id"];
                const reservationDiv =document.querySelector(`#reservation-${reservationId}`); 
                console.log(reservationDiv);
                reservationDiv.remove();
            } )
    })
}


