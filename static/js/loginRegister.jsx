'use strict'
// alert("you connected to js")

function Register() {
    const [first_name, setFirst_name] = React.useState("");
    const [last_name, setLast_name] = React.useState("");
    const [email, setEmail] = React.useState('');
    const [password, setPassword] = React.useState('');
    const [address, setAddress] = React.useState('');
    const [profile_image, setProfile_image] = React.useState('');



    const handleRegister = (evt) => {
        evt.preventDefault()
        const data = new FormData( evt.target)
        // data.append("first_name", first_name);
        // data.append("last_name", last_name);
        // data.append("email", email);
        // data.append("password", password);
        // data.append("address", address);
        // console.log('*************', profile_image)
        // data.append("profile_image", profile_image);

        fetch(`/users/new/api`, {
            method: 'POST',
            // headers: { 'Content-type': 'application/json; charset=UTF-8' },
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
                    First Name <input type="text" name="first_name" value={first_name} onChange={(e) => setFirst_name(e.target.value)} />
                </p>
                <p>
                    Last Name<input type="text" name="last_name" value={last_name} onChange={(e) => setLast_name(e.target.value)} />
                </p>
                <p>
                    Email <input type="text" name="email" value={email} onChange={(e) => setEmail(e.target.value)} />
                </p>
                <p>
                    Password <input type="password" name="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                </p>
                <p>
                    Your Addrress <input type="text" name="address" value={address} onChange={(e) => setAddress(e.target.value)} />
                </p>
                <p>
                    Upload your img: <input type="file" name="file"  onChange={(e) => setProfile_image(e.target.files)} /></p>
                <input type="submit"></input>
            </form>
        </div>
    )

}

ReactDOM.render(<Register />, document.getElementById('app'));







