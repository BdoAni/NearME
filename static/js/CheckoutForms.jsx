// import React, { useState, useEffect } from "react";
// import {
//     CardElement,
//     useStripe,
//     useElements
// } from "@stripe/react-stripe-js";
// import "./Stripe.css";
// import axios from 'axios';
// import { Link, navigate } from '@reach/router';


// export default function CheckoutForm(props) {
//     const [succeeded, setSucceeded] = useState(false);
//     const [error, setError] = useState(null);
//     const [processing, setProcessing] = useState('');
//     const [disabled, setDisabled] = useState(true);
//     const [clientSecret, setClientSecret] = useState('');
//     const [email, setEmail] = useState('');
//     const stripe = useStripe();
//     const elements = useElements();
//     const [loading, setLoading] = useState(true);
//     const [thisUser, setThisUser] = useState({})
//     const [thisTool, setThisTool] = useState({})
//     // const { user, tool } = props;
//     const [thisToolPrice, setThisToolPrice] = useState(1)
//     const { user, tool, toolPrice } = props;

//     useEffect(() => {
//         axios.get(`http://localhost:8000/api/user/${user}`)
//             .then(res => {
//                 console.log(res);
//                 // console.log(res);
//                 setThisUser(res.data.user);
//                 // setThisTool(res.data.user.tools);
//                 setLoading(false);
//             })
//             .catch(err => console.log(err))
//     }, []);
//     useEffect(()=> {
//         axios.get(`http://localhost:8000/api/tool/${tool}`)
//             .then(res => {
//                 console.log(res);
//                 // console.log(res);
//                 setThisTool(res.data.results);
//                 setThisToolPrice(res.data.results.price);
//             })
//     }, []);

//     useEffect(() => {
//         // Create PaymentIntent as soon as the page loads
//         window.fetch("http://localhost:8000/create-payment-intent", { //api/userid/toolid/
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json"
//             },
//             body: JSON.stringify({items: [{ id: "xl-tshirt" }]})
//             body: JSON.stringify({items: [toolPrice]})
//         })
//             .then(res => {
//                 return res.json();
//  function CheckoutForm(props) {
//                 setClientSecret(data.clientSecret);
//             });
//     }, []);


//     const cardStyle = {
//         style: {
//           function CheckoutForm(props) {
//         }
//     };

//     console.log(thisTool);
//     // console.log(toolPrice);

//     if (loading) {
//         return (
//             <p>Loading....</p>
//         )
//     }


//     return (
//         <>
//         <div>
//             <Link to={`/homepage`}> Home </Link>
//             <br/>
//             <Link to={`/user/${thisUser._id}`}> {thisUser.firstName}'s details page </Link>
//             <h3>Confirmation</h3>
//             <p>You are about to rent the {thisTool.type}</p>
//             <p>from {thisUser.firstName} {thisUser.lastName}</p>
//             <p>for ${thisTool.price} a day.</p>
//             <br/>
//             <h4>If this is correct, please enter your card information below</h4>
//         <form id="payment-form" class="form" onSubmit={handleSubmit}>
//             <input type="text" class="input" value={email} onChange={(e) => setEmail(e.target.value)} placeholder={thisUser.email} />
//             <CardElement id="card-element" options={cardStyle} onChange={handleChange} />
//             <button disabled={processing || disabled || succeeded} id="submit" class="button">
//                 <span id="button-text">
//                     {processing ? (
//                         <div className="spinner" id="spinner"></div>
//                     ) : (
//                         "Pay now"
//                     )}
//                 </span>
//             </button>
//             {/* Show any error that happens when processing the payment */}
//             {error && (
//                 <div className="card-error" role="alert">
//                     {error}
//                 </div>
//             )}
//             {/* Show a success message upon completion */}
//             <p className={succeeded ? "result-message" : "result-message hidden"}>
//                 Payment succeeded, see the result in your
//                 <a href={`https://dashboard.stripe.com/test/payments`}>{" "} Stripe dashboard.</a> 
//                 Refresh the page to pay again.
//             </p>
//         </form>
//         </div>
//         </>
//     );
// }