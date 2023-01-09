'use strict'
// alert("you connected to js")

function Register() {
    const handleRegister = (evt) => {
        evt.preventDefault()
        const data = new FormData(evt.target)
        fetch(`/users/new/api`, {
            method: 'POST',

            body: data
        })
            .then(res => res.json()
                .then(data => {
                    console.log(data)
                }))
            .catch((err) => console.error(err));
    };

    return (
      
                            <div>
                                <form onSubmit={handleRegister}>
                                    <p>
                                        First Name <input type="text" name="first_name" />
                                    </p>
                                    <p>
                                        Last Name<input type="text" name="last_name" />
                                    </p>
                                    <p>
                                        Email <input type="text" name="email" />
                                    </p>
                                    <p>
                                        Password <input type="password" name="password" />
                                    </p>
                                    <p>
                                        Your Addrress <input type="text" name="address" />
                                    </p>
                                    <p>
                                        Upload your img: <input type="file" name="file" />
                                    </p>
                                    <input type="submit"></input>
                                </form>
                            </div>

    )

}

ReactDOM.render(<Register />, document.getElementById('app'));







