# NearME:App for Renting Garage Tools Near You!
![NearME](https://media.giphy.com/media/TeG2kklmwHvWHyZ1OW/giphy.gif)



## Table of Contents:

- [Project Description](https://github.com/BdoAni/NearMe#project-description)
- [Tech Stack](https://github.com/BdoAni/NearMe#tech-stack)
- [Features](https://github.com/BdoAni/NearMe#features)
- [Possible Future Features](https://github.com/BdoAni/NearMe#possible-future-features)
- [Installation](https://github.com/BdoAni/NearMe#installation)


## Project Description:

NearMe is a shared economy application for garage tool rentals. It is an online marketplace allowing tool owners to rent out their tools to nearby renters, from hammers and wrenches to concrete mixers and air compressors. The primary benefits of the app will be rental income for the tool owners and lower cost of using the tools for the renters (who could simply pay for rental instead of buying brand new tools).The app will also make a positive sustainability impact - increasing the efficiency of using construction tools and reducing the carbon emissions from manufacturing and supply chain of new tools.

<hr>

**All Tools**

<img src="https://media.giphy.com/media/laWABsDZiBUyyJRFt5/giphy.gif">


**Homepage**

<img src="https://media.giphy.com/media/v9eWbQZeFuOdyJoyri/giphy.gif">

**Create a Tool**

<img src="https://media.giphy.com/media/eqlEe6wk0xCDXZGNBR/giphy.gif">

**Reserve a Tool**

<img src="https://media.giphy.com/media/bVC1bmJDKUmK3CGQCu/giphy.gif">

**Checkout a Tool**

<img src="https://media.giphy.com/media/LsXTpelwPesBNq2lk6/giphy.gif">

## Tech Stack:

- Python
- Flask
- Jinja2
- PostgreSQL
- SQLAlchemy
- JavaScript
- React
- jQuery
- AJAX
- HTML
- CSS
- Bootstrap 5



APIs:

- [Cloudinary API](https://cloudinary.com/documentation/image_upload_api_reference)
- [Stripe API](https://stripe.com/docs/api/payment_methods)
- [Google Maps Geocoding API](https://developers.google.com/maps/documentation/javascript/geocoding)
- [Google Maps Geolocation API](https://developers.google.com/maps/documentation/geolocation/overview)




## Features:

- **Create an account, login / logout, and delete account**
- **Search and browse garage tools available for rentals in your location zip code**
- **Create and publish listings to rent out your owned garage tools, update and delete listing**
- **Checkout with your debit/Credit Card via Stripe Payments**
- **Provide a rating and reviews for your completed tool rentals**


## Possible Future Features:

- **Create automated description for your tool listings by using image recognition AI**
- **Be able to communicate with other users via online chat by using Socket.io**
- **Be able to buy insurance for your tool rentals**
- **Be able to use Hub Box to a self-service delivery location to drop and return tools at any convenient time**



## Installation

To run NearMe locally on your computer:
1. **Clone repository to your local computer**
2. **Activate virtual environment**
    ```
    $ cd NearMe
    $ virtualenv env
    $ source env/bin/activate
    ```
3. **Download requirements from requirements.txt**
    ```
    $ pip3 install -r requirements.txt
    ```
4. **Get API key for Cloudinary, Stripe, and Google Maps**
  - [Cloudinary](https://cloudinary.com/documentation/image_upload_api_reference)
  - [Stripe](https://stripe.com/docs/api) 
  - [Google Maps](https://console.cloud.google.com/google/maps-apis/api-list)
  
5. **Store your  Cloudinary, Stripe, and Google Maps API key**
  - Create a file called `secrets.sh` in the app directory. Add the code below to the file and replace the text in the quotation marks:
    ```
    export CLOUDINARY_KEY=""
    export CLOUDINARY_SECRET=""
    export GOOGLEMAP_KEY=""
    export STRIPEPAYMENTS_KEY=""
    export ENDPOINTSECRET_KEY=""
    ```

6. **Read the key variables into your shell**
  ```
  $ source secrets.sh
  ```
7. **Create the database**
  ```
  $ python3 seed_database.py
  ```
8. **Start up the Flask server**
  ```
  $ python3 server.py
  ```
9. **Go to http://localhost:5000 in your browser and have fun with NearMe!**
