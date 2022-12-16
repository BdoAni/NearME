"""Server for tool lental app."""

import math
from flask import Flask, render_template, request, flash, session, redirect, url_for, jsonify
from model import connect_to_db, db, User, Tool, Review, Reservation, Media
from jinja2 import StrictUndefined
from datetime import date
# from flask_ckeditor import CKEditor, CKEditorField
import cloudinary.uploader
import os
import googlemaps 



app = Flask(__name__)
print('creating flask app')
app.jinja_env.undefined = StrictUndefined
app.secret_key = "super secret key"
# ckeditor = CKEditor(app)
CLOUDINARY_KEY=os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET=os.environ['CLOUDINARY_SECRET']
CLOUD_NAME="dqrjpc9gf"
GOOGLEMAP_KEY=os.environ['GOOGLEMAP_KEY']


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

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

    user = User.get_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = User.create(first_name, last_name, email, password, address)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")


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

    return render_template("user_dashboard.html", user=user, GOOGLEMAP_KEY=GOOGLEMAP_KEY)

#//////////////////////////// display all users ////////////////////
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

    return render_template("all_tools.html", tools=tools)

# ///////////////////////////////////// tool detail //////////////////////////////////////
@app.route("/tools/<tool_id>")
def show_detail_tool(tool_id):
    """Show details on a particular tool."""
    
    tool=Tool.get_by_id(tool_id)
    
    
    return render_template("tool_details.html", tool=tool)


# /// TODO Create ADD TO CARD and check out 

# @app.route("/update_review", methods=["POST"])
# def update_rating():
#     review_id = request.json["review_id"]
#     updated_score = request.json["updated_score"]
#     Review.update(review_id, updated_score)
#     db.session.commit()

#     return "Success"

# ///////////////////////////// Review for the tool ///////////////////////////
@app.route("/tools/<tool_id>/review", methods=["POST"])
def create_review(tool_id):
    """Create a new rating for the tool."""
    
    if not "user_id" in session:
        flash("You must log in to rate a movie.")
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
    print(f'********************THIS IS REQUEST>FILES---{request.files}')
    tool_image=request.files.get("file")
    print(f'********************THIS IS TOOL IMAGE---{tool_image}')
    
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
    # print(f'****************** this is RESULTS {search_term}')
    # print(f'****************** this is RESULTS {results}')
    
    results_list = []
    for result in results:
        results_list.append({"tool_name":result.tool_name,"tool_id": result.tool_id, "tool_description":result.description, "tool_price":float(result.price)})
        # /// TODO add mor for search terms to be able get more information DONE 
        # print(f'****************** this is RESULTS {results}')
    return jsonify(results_list)


# /////////////// reservation POST/////////////////
@app.route("/user/reservation/tool/<tool_id>", methods=["POST"])
def create_tool_reservation(tool_id):

    if not "user_id" in session:
        return redirect("/")
    user_id=session["user_id"]
    # print(f'**************** RESER POST--------- TOOL ID==={tool_id}')

    # TODO reservation is not working correctly [ request.form.get((('end_date'-'start_date') + 1 ) * ('price')) ]
    start_date = request.form.get("start_day")
    end_date = request.form.get("end_day")
    price = float(request.form.get("price"))
    # TO DO get fix  total amount
    # total =  float(request.form.get((int(float('end_date'))-int(float('start_date')) + 1 ) * int('price')))
    # total =(math.floor((int('end_date')-int('start_date')).total_seconds()/float(86400)))
    total=25
    print(f'***************************** This is total {total}')
    
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
    # print(f'**************** RESER GET--------- USER ID==={user_id}')
    
    # TODO add get all reserv for one user.
    reservations = Reservation.all_reservations()
    
    return render_template( 'reservation.html',  user=user, reservations=reservations)




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

# //// todo create card and add all reserved tools to that card 


# /////////////// 3. need to create a card where all accepted offers from you will be in that card/////
# /////////////// 4. need to create a revie for each tool ////// Almost Done see line 139 Done
# //////////////////////// Need to create a search bar for a user to serch a spesific tool///// almost done


def add_user_img_record(img_url):
    """Stub function for persisting data to database"""
    print("\n".join([f"{'*' * 20}", "SAVE THIS url to your database!!",
                    img_url, f"{'*' * 20}" ]))

    
    
    
    
if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)