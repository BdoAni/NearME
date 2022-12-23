'use strict'
alert("you connected to js")

function Register() {
    const [first_name, setFirst_name] = React.useState("");
    const [last_name, setLast_name] = React.useState("");
    const [email, setEmail] = React.useState('');
    const [password, setPassword] = React.useState('');
    const [address, setAddress] = React.useState('');



    const handleRegister = (evt) => {
        evt.preventDefault()
        fetch(`/users/new/api`, {
            method: 'POST',
            headers: { 'Content-type': 'application/json; charset=UTF-8' },
            body: JSON.stringify({
                "first_name": first_name, 
                "last_name": last_name, 
                "email": email, 
                "password": password, 
                "address": address 
            })
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
                First Name <input type="text" value={first_name} onChange={(e) => setFirst_name(e.target.value)} />
            </p>
            <p>
                Last Name<input type="text" value={last_name} onChange={(e) => setLast_name(e.target.value)} />
            </p>
            <p>
                Email <input type="text" value={email} onChange={(e) => setEmail(e.target.value)} />
            </p>
            <p>
                Password <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
            </p>
            <p>
                Your Addrress <input type="text" value={address} onChange={(e) => setAddress(e.target.value)} />
            </p>
            <input type="submit"></input>
            </form>
        </div>
    )

}

ReactDOM.render(<Register/>, document.getElementById('app'));







