import React, { useState, useEffect } from 'react';
import { loadStripe } from "@stripe/stripe-js";
import { Elements } from "@stripe/react-stripe-js";
import CheckoutForm from './CheckoutForm';
import axios from 'axios';

const promise = loadStripe("pk_test_51IalToAQmXzgarKriNlG0enhbeYqakTPb3e8GyHE6mbNLEIZMACg8k5J0Ul8GPk9nFEsbuyBAUzhCMF5AELLp0CZ003isiZgwB");

function CheckoutForm2(props) {
    // const {userId, toolsId} = props;
    // console.log(userId);
    // console.log(toolsId);
    const [user, setUser] = useState(props._id)
    const [tool, setTool] = useState(props.tool_id)
    const [toolPrice, setToolPrice] = useState(0)
    const [loading, setLoading] = useState(true);
    console.log(user);
    console.log(tool);


    useEffect(()=> {
        axios.get(`http://localhost:8000/api/tool/${tool}/price`)
            .then(res => {
                console.log(res);
                setToolPrice(res.data.results);
                setLoading(false);
            })
    }, []);

    if(loading){
        return (
            <p>Loading....</p>
        )
    }
    // const { props } = props;
    return (
        <div>
            <Elements stripe={promise}>
                <CheckoutForm props={props} user={user} tool={tool}/>
                <CheckoutForm props={props} user={user} tool={tool} toolPrice={toolPrice}/>
            </Elements>
        </div>
    )
}
export default CheckoutForm2