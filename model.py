from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import math


db = SQLAlchemy()

class User(db.Model):
    """ A user class"""
    __tablename__ = "users"
    
    user_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name=db.Column(db.String(255),  nullable=False)
    last_name=db.Column(db.String(255),  nullable=False)
    email = db.Column(db.String,  nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    phone_number=db.Column(db.String(20))
    address = db.Column(db.String(255), nullable=False)
    about = db.Column(db.Text, nullable=True)
    profile_image = db.Column(db.String)
    created_at = db.Column(db.DateTime(timezone=True))
    updated_at = db.Column(db.DateTime(timezone=True))
 
    reviews = db.relationship("Review", back_populates="user")
    tools = db.relationship("Tool", back_populates="user")
    reservations = db.relationship("Reservation", back_populates="user")
    
    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"
    
    

    
    @classmethod
    def create(self, first_name, last_name,  email, password,address, profile_image ):
       """Create and return a new user."""

       return self( first_name=first_name, last_name=last_name,  email=email, password=password, address=address, profile_image=profile_image )
    @classmethod
    def get_by_id(self, user_id):
        return self.query.get(user_id)
    
    @classmethod
    def get_by_email(self, email):
        return self.query.filter(User.email == email).first()
    
    @classmethod
    def all_users(self):
        return self.query.all()
    
    
class Tool(db.Model):
    """A tool."""

    __tablename__ = "tools"

    tool_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    tool_name = db.Column(db.String(255), nullable=False )
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(6,2), nullable=False)
    availability_start= db.Column(db.DateTime(timezone=True))
    availability_end= db.Column(db.DateTime(timezone=True))
    created_at = db.Column(db.DateTime(timezone=True))
    updated_at = db.Column(db.DateTime(timezone=True))
    tool_image = db.Column(db.String)
    

    reviews = db.relationship("Review", back_populates="tools")
    user = db.relationship("User", back_populates="tools")
    reservations = db.relationship("Reservation", back_populates="tool")
    media = db.relationship("Media", back_populates="tool")
    
    def __repr__(self):
        return f"<Tool  tool_id={self.tool_id} tool_name={self.tool_name}>"
    
    
    @classmethod
    def create(self, tool_name, description, price,  availability_start, availability_end, tool_image, user_id):
        """Create and return a new tool."""

        return self(
            tool_name=tool_name,
            description=description,
            price=price,
            availability_start=availability_start,
            availability_end=availability_end,
            tool_image=tool_image,
            user_id=user_id
            )
    @classmethod
    def all_tools(self):
        """Return all tools."""

        return self.query.all() 
    
    @classmethod
    def get_by_id(self, tool_id):
        """Return a tool by primary key."""

        return self.query.get(tool_id)   
    
    
    @classmethod
    def get_review_by_tool(self, tool_id):
        """this is getting reviews for tool by one user """
        tool=self.get_by_id(tool_id)
        reviews=tool.reviews

        return (reviews)
    
    
    
    def get_avg_review_of_tool(self):
        
        star_sum=0
        star_avg=None
        for review in self.reviews:
            star_sum += review.rating
        if len(self.reviews) > 0:
            # print(f'*************** THIS IS STAR SUM BEFORE { self.tool_name} ------>>{star_sum}')
            star_avg=star_sum/len(self.reviews)
        else:
            star_avg=0
        # print(f'*************** THIS IS STAR SUM FOR { self.tool_name} ------>>{star_avg}')
            
        return star_avg
    
class Reservation(db.Model):
    """A tool reservations."""
#  do i need to ad a name for my user to the reservation table?=
    __tablename__ = "reservations"

    reservation_id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
    tool_id = db.Column(db.Integer, db.ForeignKey("tools.tool_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    start_date = db.Column(db.DateTime(timezone=True))
    end_date = db.Column(db.DateTime(timezone=True))
    price = db.Column(db.Numeric(6,2), nullable=False)
    processed = db.Column(db.Boolean(), nullable=False)
    total = db.Column(db.Numeric(6,2), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True))
    updated_at = db.Column(db.DateTime(timezone=True))
    

    tool = db.relationship("Tool", back_populates="reservations")
    user = db.relationship("User", back_populates="reservations")
  
    def __repr__(self):
        return f"<Reservation reservation_id={self.reservation_id} user_id={self.user_id} start_date={self.start_date} end_date={self.end_date}>"
    
    
    @classmethod
    def create(self, start_date, end_date, price,  total,  user_id, tool_id ):
        """Create and return a new movie."""
        
        now = datetime.now()
        new_reservation = self(
            start_date = start_date,
            end_date = end_date,
            price = price,
            total = total,
            user_id = user_id,
            tool_id = tool_id,
            created_at = now,
            updated_at = now,
            processed = False
        )
        return new_reservation
    
    def processed_update(self):
        self.processed=True
        

    @classmethod
    def all_reservations(self):
        """Return all reservations."""

        return self.query.all() 
    
    @classmethod
    def get_by_id(self, reservation_id):
        """Return a reservation by primary key."""

        return self.query.get(reservation_id)  
    
    @classmethod
    def get_reserved_days(self, reservation_id, user_id, start_day, end_day):
        """Return a reservation by primary key."""

        return self.query.get(reservation_id, user_id, start_day, end_day )  
    
class Review(db.Model):
    """A tool reviews."""

    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tool_id = db.Column(db.Integer, db.ForeignKey("tools.tool_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    name = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True))
    

    tools = db.relationship("Tool", back_populates="reviews")
    user = db.relationship("User", back_populates="reviews")
    media = db.relationship("Media", back_populates="review")
    

    def __repr__(self):
        return f"<Review  review_id={self.review_id} review={self.rating} user_id={self.user_id}>"
    
    @classmethod
    def create(self, user_id, tool_id,  name, rating, comment):
        """Return all reservations."""

        return self(user_id=user_id,
                    tool_id=tool_id,
                    # media=media,
                    name=name,
                    rating=rating,
                    comment=comment
                    ) 
    @classmethod
    def update(self, review_id, new_rating):
        """ Update a rating given rating_id and the updated rating. """
        rating = self.query.get(review_id)
        rating.rating =new_rating
        
    
class Media(db.Model):
    """A media for reviews."""

    __tablename__ = "media"

    media_id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
    tool_id = db.Column(db.Integer, db.ForeignKey("tools.tool_id"))
    review_id = db.Column(db.Integer, db.ForeignKey("reviews.review_id"))
    media_type = db.Column(db.String)
    url = db.Column(db.String)


    tool = db.relationship("Tool", back_populates="media")
    review = db.relationship("Review", back_populates="media")

    def __repr__(self):
        return f"<Media media_id={self.media_id} tool_id={self.tool_id=} review_id={self.review_id}>"
    
    @classmethod
    def get_by_id(self, media_id):
        """Return a media by primary key."""

        return self.query.get(media_id) 
    
def connect_to_db(flask_app, db_uri="postgresql:///nearme", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app
    import os

    # these linews give you a blank slate
    # os.system("dropdb nearme --if-exists")
    # os.system("createdb nearme")

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)

    db.create_all()