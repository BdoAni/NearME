"""Server for tool lental app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db, User, Tool, Review, Reservation, Media
from jinja2 import StrictUndefined


app = Flask(__name__)
print('creating flask app')
app.jinja_env.undefined = StrictUndefined
app.secret_key = "super secret key"

@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')



@app.route("/users")
def all_users():
    """View all users."""
      
    users = User.all_users()

    return render_template("all_users.html", users=users)


# Create a new user
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

# /Log in post method and need to redirect to the sesson user personal page with all his listing items 
# /////////////////////////////////////// LOGIN//////////////////////////////////////////////////////
@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")
    # print(" ******** email **************", email)

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



@app.route("/dashboard")
def show_user_dashboard():
    # this is getting an user from the sessin and redirects if you'r not logedin 
    if not "user_id" in session:
        return redirect("/")
  
    user_id=session["user_id"]
    
    user=User.get_by_id(user_id)

    return render_template("user_dashboard.html", user=user)

# display all users

@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""
    
    user=User.get_by_id(user_id)

    return render_template("user_details.html", user=user)

@app.route("/tools")
def all_tools():
    """View all tools."""

    tools= Tool.all_tools()

    return render_template("all_tools.html", tools=tools)


@app.route("/tools/<tool_id>")
def show_tool(tool_id):
    """Show details on a particular tool."""
    
    tool=Tool.get_by_id(tool_id)
    
    
    return render_template("tool_details.html", tool=tool)



# ///////////////////////////// Review for the tool /////
@app.route("/tools/<tool_id>/review", methods=["POST"])
def create_review(tool_id):
    """Create a new rating for the tool."""
    
    if not "user_id" in session:
        flash("You must log in to rate a movie.")
        return redirect("/")
    
    user_id=session["user_id"]
    # user=User.get_by_id(user_id)
    
    # tool =Tool.get_by_id(tool_id)
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



# /////////////////////////////////////////////////////////////////////////////////
# creating a tool 
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
    tool_image=request.form.get("image")
    
    
    tool=Tool.create(tool_name, description, price, availability_start, availability_end, tool_image, user_id)
    # print(f'++++++++++++{tool_name }, {description}, {price}, {availability_start}, {availability_end}, {tool_image}, {user_id}++++++++' )
    db.session.add(tool)
    db.session.commit()
    if Tool.get_by_id(tool.tool_id):
        flash("Cannot create a tool. Try again.")

    return redirect("/dashboard")



# /////////////////////////////////////////////////////////////////////////////////
# update or eddit a tool  get method
@app.route('/tools/<tool_id>/edit')
def edit_tool(tool_id):
    
    
    tool = Tool.get_by_id(tool_id)
    if not "user_id" in session:
        return redirect("/")
  
    user_id=session["user_id"]
    user=User.get_by_id(user_id)
    return render_template("tool_ediit.html", tool=tool, user=user)  

  
# /////////////////////////////////////////////////////////////////////////////////
# update or eddit a tool  post method 
@app.route('/tools/<tool_id>/edit', methods=["POST"])
def edit_tool_by_id(tool_id):
    
    tool = Tool.get_by_id(tool_id)
    tool_name=request.form.get("name")
    description=request.form.get("description")
    price=request.form.get("price")
    availability_start=request.form.get("formstart_date")
    availability_end=request.form.get("formend_date")
    tool_image=request.form.get("image")
    
    tool.tool_name=tool_name
    tool.description=description
    tool.price=price
    tool.availability_start=availability_start
    tool.availability_end=availability_end
    tool.tool_image=tool_image
    db.session.add(tool)
    db.session.commit()
    
    return redirect("/dashboard")
    
    
# ////////////////1. need delete the tool/////
# /////////////// 2. need a create a reservation page and methods ///////
# /////////////// 3. need to create a card where all accepted offers from you will be in that card/////
# /////////////// 4. need to create a revie for each tool //////
# /////////////// 5. logout////////////////////////////////////
    
    
    
    
if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)