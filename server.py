"""Server for tool lental app."""

import functools
from flask import Flask, render_template, request, flash, session, redirect, url_for, jsonify
import json
import math
from model import connect_to_db, db, User, Tool, Review, Reservation, Media
from jinja2 import StrictUndefined
from datetime import datetime, timedelta
# from flask_ckeditor import CKEditor, CKEditorField
import cloudinary.uploader
import os
import googlemaps 
import stripe
from html import escape, unescape




app = Flask(__name__)
print('creating flask app')
app.jinja_env.undefined = StrictUndefined
app.secret_key = "super secret key"
# ckeditor = CKEditor(app)
CLOUDINARY_KEY=os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET=os.environ['CLOUDINARY_SECRET']
CLOUD_NAME="dqrjpc9gf"
GOOGLEMAP_KEY=os.environ['GOOGLEMAP_KEY']
LOCAL_DOMAIN = 'http://localhost:5000/payment'
stripe_keys = {
'STRIPEPAYMENTS_KEY':os.environ['STRIPEPAYMENTS_KEY'],
'ENDPOINTSECRET_KEY':os.environ['ENDPOINTSECRET_KEY']
}
stripe.api_key=os.environ['ENDPOINTSECRET_KEY']


@app.route('/')
def homepage():
    """View homepage."""
    
    return render_template('homepage.html', GOOGLEMAP_KEY=GOOGLEMAP_KEY)

# ////////////////////////////////////////// GOOGLE MAP GET///////////////////////
@app.route('/map')
def google_map():
    """View map page."""

    return render_template('google_map.html', GOOGLEMAP_KEY=GOOGLEMAP_KEY)




@app.route("/users")
def all_users():
    """View all users."""
      
    users = User.all_users()

    return render_template("all_users.html", users=users)


# /////////////////////////////////////////Registter a new user//////////////////////////////
@app.route("/users/new", methods=["POST"])
def register_user():
    """Create a new user."""
    
    
    first_name = request.form.get("fname")
    last_name = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")
    address =request.form.get("address")
    profile_image=request.files['file']

    user = User.get_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = User.create(first_name, last_name, email, password, address, profile_image)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")


# /////////////////////////////////////////Registter a new user React//////////////////////////////
@app.route("/users/new/api", methods=["POST"])
def register_user_in_react():
    """Create a new user."""
    
    data=request.form.to_dict()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")
    address = data.get("address")
   
    
    profile_image = request.files['file']  
    # print(f'******************* PRINTING profile_image {profile_image}')
    result = cloudinary.uploader.upload(
        file=profile_image,
        api_key=CLOUDINARY_KEY,
        api_secret=CLOUDINARY_SECRET,
        cloud_name=CLOUD_NAME
        )
    profile_image = result['secure_url']

    user = User.get_by_email(email)

    result={}
    if user:
        result['status']="Cannot create an account with that email. Try again."
    else:
        user = User.create(first_name, last_name, email, password, address, profile_image)
        db.session.add(user)
        db.session.commit()
        result['status']="Account created! Please log in."

    return jsonify(result)


# /////////////////////////////////////// LOGIN  //////////////////////////////////////////////////////
@app.route("/login")
def login_page():
    """ user login."""
    
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.get_by_email(email)

    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
        return do_logout()
    
    # print(" ******** user_id **************", user.user_id)
    # Log in user by storing the user's email in session
    session["user_id"] = user.user_id
    session["email"] = email 
    session["first_name"] = user.first_name
    # print(" ******** email **************", email)
    flash(f"Welcome back, {user.first_name}!")

    return redirect("/dashboard")


# ////////////////////////////////////LOG OUT //////////////////////////
@app.route('/logout')
def logout():

    return do_logout()

def do_logout():
    if "user_id" in session:
        del session["user_id"]
    if "email" in session:
        del session["email"]
    # session["_flashes"].clear()
    return redirect('/')

# ///////////////////////////////// user Dashboard //////////////////////
@app.route("/dashboard")
def show_user_dashboard():
    # this is getting an user from the sessin and redirects if you'r not logedin 
    if not "user_id" in session:
        return redirect("/")
  
    user_id=session["user_id"]
    
    user=User.get_by_id(user_id)
    
    
    tools= Tool.all_tools() 
    for tool in tools:
        Tool.get_review_by_tool(tool.tool_id)
    

    return render_template("user_dashboard.html", user=user, tools=tools, GOOGLEMAP_KEY=GOOGLEMAP_KEY)

#//////////////////////////// display a user ////////////////////
@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""
    
    user=User.get_by_id(user_id)

    return render_template("user_details.html", user=user)



# ///////////////////////////////////// Getting All Tools /////////////////////////////
@app.route("/tools")
def all_tools():
    """View all tools."""

    tools= Tool.all_tools() 
    for tool in tools:
        Tool.get_review_by_tool(tool.tool_id)
    
    num_five_star_ratings=db.session.query((Review.rating)).filter(Review.rating==5).count()
    num_four_star_ratings=db.session.query((Review.rating)).filter(Review.rating==4).count()
    num_three_star_ratings=db.session.query((Review.rating)).filter(Review.rating==3).count()
    num_two_star_ratings=db.session.query((Review.rating)).filter(Review.rating==2).count()
    num_one_star_ratings=db.session.query((Review.rating)).filter(Review.rating==1).count()

    five_star=(5 * num_five_star_ratings)
    four_star=(4 * num_four_star_ratings )
    three_star=(3 * num_three_star_ratings)
    two_star=(2 * num_two_star_ratings)
    rating_stars=((
        five_star + four_star + 
        three_star + two_star + 
        num_one_star_ratings)/(num_five_star_ratings +
                                  num_four_star_ratings +
                                  num_three_star_ratings +
                                  num_two_star_ratings +
                                  num_one_star_ratings))
    star_avg=Tool.get_avg_review_of_tool(tool)

    return render_template("all_tools.html", tools=tools, rating_stars=rating_stars, star_avg=star_avg)

# ///////////////////////////////////// tool detail //////////////////////////////////////
@app.route("/tools/<tool_id>")
def show_detail_tool(tool_id):
    """Show details on a particular tool."""
    # getting user_id from the session
    if not "user_id" in session:
        flash("Please Login/Register for the best user experience")
        return redirect("/")

    user_id=session["user_id"]
    tool=Tool.get_by_id(tool_id)
    reviews=Tool.get_review_by_tool(tool_id)
    num_five_star_ratings=db.session.query((Review.rating)).filter(Review.rating==5).count()
    num_four_star_ratings=db.session.query((Review.rating)).filter(Review.rating==4).count()
    num_three_star_ratings=db.session.query((Review.rating)).filter(Review.rating==3).count()
    num_two_star_ratings=db.session.query((Review.rating)).filter(Review.rating==2).count()
    num_one_star_ratings=db.session.query((Review.rating)).filter(Review.rating==1).count()

    five_star=(5 * num_five_star_ratings)
    four_star=(4 * num_four_star_ratings )
    three_star=(3 * num_three_star_ratings)
    two_star=(2 * num_two_star_ratings)
    rating_stars=((
        five_star + four_star + 
        three_star + two_star + 
        num_one_star_ratings)/(num_five_star_ratings +
                                  num_four_star_ratings +
                                  num_three_star_ratings +
                                  num_two_star_ratings +
                                  num_one_star_ratings))
    return render_template("tool_details.html", tool=tool)


# ///////////////////////////// Review for the tool POST ///////////////////////////
@app.route("/tools/<tool_id>/review", methods=["POST"])
def create_review(tool_id):
    """Create a new rating for the tool."""
    
    if not "user_id" in session:
        flash("Please Login/Register for the best user experience")
        return redirect("/")
    
    user_id=session["user_id"]
    rating_score = request.form.get("rating")
    comment = request.form.get("comment")
    #  if comments came from the form as an empt. string we want to make them as a none 
    if comment =="":
        comment=None
    # media = request.form.get("media")
    name = request.form.get("name")
    if name=="":
        name=None
    if not rating_score:
        flash("Error: you didn't select a score for your rating.")
    else:
        rating = Review.create(user_id, tool_id,  name, int(rating_score), comment )
        db.session.add(rating)
        db.session.commit()
        
        # days= Reservation.query.filter()

        flash(f"You rated this tool-{rating_score} out of 5.")

    return redirect(f"/tools/{tool_id}")

# ///////////////////////////////////// Create a tool GET //////////////////////////////////////
@app.route("/tools/new")
def add_tool():
    if not "user_id" in session:
        return redirect("/")
  
    user_id=session["user_id"]
    
    user=User.get_by_id(user_id)
    return render_template("new_tool.html",  user=user)  

# ///////////////////////////////////// Create a tool  POST ///////////////////////////////////////
@app.route("/tools/new", methods=["POST"])
def create_tool(): 
    """Create a new tool."""
    
    if not "user_id" in session:
        return redirect("/")
  
    user_id=session["user_id"]
    
    user=User.get_by_id(user_id)
    
    tool_name=request.form.get("name")
    description=request.form.get("description")
    price=request.form.get("price")
    availability_start=request.form.get("formstart_date")
    availability_end=request.form.get("formend_date")
    tool_image=request.files['file']

    result = cloudinary.uploader.upload(
        file=tool_image,
        api_key=CLOUDINARY_KEY,
        api_secret=CLOUDINARY_SECRET,
        cloud_name=CLOUD_NAME
        )
    tool_image = result['secure_url']
    tool=Tool.create(tool_name, description, price, availability_start, availability_end, tool_image, user_id)
    db.session.add(tool)
    db.session.commit()
    
    
    if not Tool.get_by_id(tool.tool_id):
        flash("Cannot create a tool. Try again.")

    return redirect("/dashboard")




# //////////////////////////////////////update  edit the tool  get method /////////////////////////////
@app.route('/tools/<tool_id>/edit')
def edit_tool(tool_id):
    
    tool = Tool.get_by_id(tool_id)
    if not "user_id" in session:
        return redirect("/")
  
    user_id=session["user_id"]
    user=User.get_by_id(user_id)
    return render_template("tool_ediit.html", tool=tool, user=user)  

  
# //////////////////////////////////// Edit Tool  POST/////////////////////////////////////////////
@app.route('/tools/<tool_id>/edit', methods=["POST"])
def edit_tool_by_id(tool_id):
    
    tool = Tool.get_by_id(tool_id)
    tool_name=request.form.get("name")
    description=request.form.get("description")
    price=request.form.get("price")
    availability_start=request.form.get("formstart_date")
    availability_end=request.form.get("formend_date")
    tool_image=request.files.get("file")
    
    tool.tool_name=tool_name
    tool.description=description
    tool.price=price
    tool.availability_start=availability_start
    tool.availability_end=availability_end
    
    if tool.tool_image != tool_image:
        result = cloudinary.uploader.upload(
            file=tool_image,
            api_key=CLOUDINARY_KEY,
            api_secret=CLOUDINARY_SECRET,
            cloud_name=CLOUD_NAME
            )
        tool_image = result['secure_url']
        tool.tool_image=tool_image
        
    db.session.add(tool)
    db.session.commit()
    
    return redirect("/dashboard")
    
    
# ////////////////  delete a Tool by id////////////////////////
@app.route('/tools/delete/<tool_id>')
def delete_tool_by_id(tool_id):
    
    if not "user_id" in session:
        return redirect("/")
    
    tool = Tool.get_by_id(tool_id)
    try:
        db.session.delete(tool)
        db.session.commit()
        return redirect("/dashboard")
    except:
          "There was a problem deleting that tool"
    return render_template("tool_ediit.html", tool=tool) 

# // todo show beasy calendar  fro resered tool so other user cant  rserve

# ////////////////////////////// Search in javascript ////////////////////////
@app.route("/search")
def searchtools():
    tools = Tool.all_tools() 
    
    search_term = request.args.get("searched")
    # import pdb; pdb.set_trace() 
    results=db.session.query(Tool).filter(
        Tool.tool_name.ilike("%{}%".format(search_term))
        ).all()

    
    results_list = []
    for result in results:
        results_list.append({
            "tool_name":result.tool_name,
            "tool_id": result.tool_id,
            "tool_description":result.description,
            "tool_price":float(result.price),
            "user_address":result.user.address
            })

    return jsonify(results_list)



# /////////////// reservation POST/////////////////
@app.route("/user/reservation/tool/<tool_id>", methods=["POST"])
def create_tool_reservation(tool_id):

    if not "user_id" in session:
        return redirect("/")
    user_id=session["user_id"]
    
    start_date = datetime.strptime(request.form.get("start_date"), '%Y-%m-%d')
    end_date = datetime.strptime(request.form.get("end_date"), '%Y-%m-%d')
    price = float(request.form.get("price"))
    total=0
    
    number_of_days=(((end_date - start_date).days)+1)
    
    total = float(number_of_days * price)
    
    reservation = Reservation.create(start_date, end_date, price, total, user_id, tool_id )
    db.session.add(reservation)
    db.session.commit()
    return redirect ('/reservation')


# /////////////// reservation page and methods  Get/////////////////
@app.route("/reservation")
def reservation_tools():
    
    if not "user_id" in session:
        return redirect("/")
    user_id=session["user_id"]
    user=User.get_by_id(user_id)

   
    return render_template( 'reservation.html', user=user, reservations = user.reservations)




# /////////////////////////////////////////---> STRIPE <--- \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    
# ////////////////////////////////////////////// Publishable key ///////////////////
@app.route('/config')
def get_publishable_key():
    stripe_config = {'publicKey': stripe_keys['publishable_key']}
    return jsonify(stripe_config)


@app.route('/checkout')
def checkout():
    if not "user_id" in session:
        return redirect("/")
    user_id=session["user_id"]
    user=User.get_by_id(user_id)
                    
    return render_template('/checkout.html', reservations=user.reservations, stripe_key=stripe_keys['STRIPEPAYMENTS_KEY'])

# /////////////////////////////////// Checkout STRIPE /////////////////////////
@app.route("/payment",  methods=["POST"])
def payments_forms():
    
    if not "user_id" in session:
        return redirect("/")
    
    customer = stripe.Customer.create(
    email=request.form['stripeEmail'],
    source=request.form['stripeToken'],
    )
    amount = request.form.get('amount').replace('.','')

    charge = stripe.Charge.create(
        customer=customer.id,
        description='',
        amount=amount,
        currency='usd',
    )
    
    return redirect('/success')

# //////////////////////////////////////////////////////////////////////////
@app.route('/payment/success')
def success_forms():
    
    if not "user_id" in session:
        return redirect("/")
    user_id=session["user_id"]
    user=User.get_by_id(user_id)

    addresses=[]
    for reservation in user.reservations:
        addresses.append(reservation.tool.user.address)

    return render_template('success.html', user=user,  reservations=user.reservations, addresses=addresses, GOOGLEMAP_KEY=GOOGLEMAP_KEY )

# ////////////////////////////////////////////// POST CHECKOUT SESSION///////////////////////

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
      # define the tools variable
      
    if not "user_id" in session:
        return redirect("/")
    user_id=session["user_id"]
    user=User.get_by_id(user_id)
    
    try:
        data = json.loads(request.data)
        
    # get tool
        tool_id=int(data['tool_id'])
        tool_to_purchase=Tool.get_by_id(tool_id)
        reservation_id=int(data['reservation_id'])
        reservation=Reservation.get_by_id(reservation_id)
    # create new checkout session
        checkout_session = stripe.checkout.Session.create(
            expand= ['line_items'],
            line_items=[
                 {
                    'name': tool_to_purchase.tool_name,
                    'quantity': 1,
                    'currency': 'USD',
                    'amount': int(reservation.total * 100)
                }
            ],
            mode='payment',
            success_url= LOCAL_DOMAIN + '/success',
            cancel_url=  LOCAL_DOMAIN + '/cancel',
        )
        print(f'******************* PRINT checkout_session ', checkout_session )
        
        # return jsonify({'sessionId': checkout_session['id']})
        return jsonify(checkout_session)
    except Exception as e:
        print(f'******************* PRINT E', e)
        return jsonify(error=str(e))



# ////////////////  delete a reservation by id////////////////////////
@app.route('/user/reservation/delete/<reservation_id>', methods=['POST'])
def delete_reservation_by_id(reservation_id):
     
    if not "user_id" in session:
        return jsonify({"message": "ERROR You have to be loggedin "})
    
    reserve = Reservation.get_by_id(reservation_id)
    try:
        db.session.delete(reserve)
        db.session.commit()
        return jsonify({"message": "Deleted reservation successfuly", 'reservation_id': reservation_id} )
    except:
          
        return jsonify( {"message":"There was a problem deleting that reservation_id", 'reservation_id': reservation_id}) 


def add_user_img_record(img_url):
    """Stub function for persisting data to database"""
    print("\n".join([f"{'*' * 20}", "SAVE THIS url to your database!!",
                    img_url, f"{'*' * 20}" ]))

    
    
    
    
if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)