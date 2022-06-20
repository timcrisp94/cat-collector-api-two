# created at timestamp
from datetime import datetime
# import db so Cat model inherits basic functionality from Model property of db
from api.models.db import db

class Cat(db.Model):
  # define tablename as it will appear in the psql shell
    __tablename__ = 'cats'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    breed = db.Column(db.String(100))
    description = db.Column(db.String(250))
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # establish "belongs to" relationship
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))

    # __repr__ method returns a string representation of our object
    def __repr__(self):
      return f"Cat('{self.id}', '{self.name}'"

    # serialize method iterates through columns in the table and adds each k/v pair to a dictionary, giving us the ability to view our data in a JSON serializable format (for React)
    def serialize(self):
      cat = {c.name: getattr(self, c.name) for c in self.__table__.columns}
      return cat