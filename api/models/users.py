from api.utils.database import db
from api.utils.api import ma 

class User(db.Model):
    __tablename__ = 'users' 

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    isVerified = db.Column(db.Boolean, nullable=False, default=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User 

    id = ma.auto_field()
    username = ma.auto_field()
    isVerified = ma.auto_field()
    email = ma.auto_field()
