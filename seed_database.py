"""Script to seed database."""
import os
import model
import server

os.system('dropdb nearme')
os.system('createdb nearme')

model.connect_to_db(server.app)

# Updates the database schema
model.db.create_all()

# TODO: use create methods to add objects to database