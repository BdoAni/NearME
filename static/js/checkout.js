'use strict'
// alert("you connected to js") 

// const checkoutLinks = document.querySelectorAll('.check-out')
// for (const checkout of checkoutLinks) {
//     checkout.addEventListener('click', (evt) => {
//         evt.preventDefault()
//         console.log('*** Starting STRIPE checkout')
//     })
// }

const forms = document.querySelectorAll('.checkout-form');
for(const form of forms){
    form.addEventListener('submit', (event) => {
        event.preventDefault()
        const formData = new FormData(event.target)
        console.log("..****** PRINTING formData ", formData)
        for (const [key, value] of formData) {
            console.log(`${ key }: ${ value }\n`);
        }
        // create an object from the form data to send in the request
        const data = {}
        for (const [key, value] of formData) {
            data[key] = value
        }
        
        fetch('/create-checkout-session', {
            method: 'POST',
            body: JSON.stringify(data),
            // body: JSON.stringify({ token: result.paymentMethod.id }),

            // body: formData,
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then((fetchResult) => { return fetchResult.json(); })
        .then((data) => {
            console.log("..****** PRINT Data ", data)
            console.log("printing data.URL  -**************", data.url)
            window.location.replace(data.url);

            // console.log("**** printing a stripe key", {stripeKey})
            // console.log('***** data printing', fetchResult)
            const stripe = Stripe(stripeKey);
            
            const lineItems = [
                // { price: data.amount_total.toString(), quantity: 1 }
                {
                    price: data.line_items.data[0].price.unit_amount_decimal, quantity: 1 
                }
            ];
            // const lineItems = Array.from(data.line_items.data);
            console.log("printing line items------>", lineItems)
            stripe.redirectToCheckout({
                // Make the id field from the Checkout Session creation API response
                // available to this file, so you can provide it as parameter here
                // instead of the {{CHECKOUT_SESSION_ID}} placeholder.
                lineItems: lineItems,
                mode: 'payment',
                // TODO change the ip address for configurable host name 
                successUrl: data.success_url,
                cancelUrl: data.cancel_url,
                sessionId:data.sessionId
            }).then(function (result) {
                // If `redirectToCheckout` fails due to a browser or network
                // error, display the localized error message to your customer
                // using `result.error.message`.
            });
        })
    });
}
