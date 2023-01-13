'use strict'
// alert("you connected to js")
function App(){
    const [showForm, setShowForm]= React.useState(true);


    function hideForm(){
        setShowForm(false);
    }
    return (<div>
        {showForm ? <Register hideForm={hideForm} /> : <h5>You successfully created your account, Please login! </h5>
                   
        }
        </div>)
}



function Register(props) {
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
                    props.hideForm()
                }))
            .catch((err) => console.error(err));
    };

    return (
            <div>
            <form class="form-register" onSubmit={handleRegister}>
                <h5>Create an Account</h5>
                <p>
                    <input id="firstName" type="text" name="first_name"  />
                    <label class="form-label" for="firstName"> First Name</label>
                </p>
                <p>
                    <input id="lastName"  type="text" name="last_name" />
                    <label class="form-label" for="firstName"> last Name</label>
                </p>
                <p>
                    <input id='email' type="text" name="email" />
                    <label class="form-label" for="email"> Email </label>
                </p>
                <p>
                    <input id="loginPassword-react"  type="password" name="password" />
                    <label class="form-label" for="loginPassword-react">Password </label>
                </p>
                <p>
                    <input  id="address" type="text" name="address" />
                    <label class="form-label" for="Address">Your Addrress </label>
                </p>
                <p>
                    <input id="userImg"  type="file" name="file" />
                    <label class="form-label" for="userImg"> </label>
                                            
                </p>      
                <button type="submit" class="submit-login">Register</button>

                                    {/* <input type="submit"></input> */}
            </form>
        </div>

    )

}

ReactDOM.render(<App />, document.getElementById('app'));







