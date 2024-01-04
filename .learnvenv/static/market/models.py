from typing import List
from static.market import db, bcrypt, login_manager
from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    #__tablenamae__ = "user"   

    uid: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(db.String(length=30), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(db.String(length=50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(db.String(length=60), nullable=False)
    budget: Mapped[int] = mapped_column(db.Integer, nullable=True, default=10000)
    item: Mapped[List["Item"]] = db.relationship(backref="owned_user", lazy=True)
    
    @property
    def prettier_budget(self):
        if len(str(self.budget)) > 3:
            return f'${str(self.budget)[:-3]},{str(self.budget)[-3:]}'
        else: 
            return f'{self.budget}'

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
        
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def get_id(self):
           return (self.uid)
    
    def can_purchase(self, item_object):
        return self.budget >= item_object.price
    
    def can_sell(self, item_obj):
        return item_obj in self.item
           

class Item(db.Model):
    #__tablenamae__ = "item" 
    
    pid: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(length=30), unique=True, nullable=False)
    price: Mapped[int] = mapped_column(db.Integer, nullable=False)
    barcode: Mapped[str] = mapped_column(db.String(length=20), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(db.String(length=1024), nullable=False, unique=True)
    owner = mapped_column(db.Integer, db.ForeignKey("user.uid"))

    def __repr__(self): #string representation
        return f'Item {self.name}'
    
    def ownership(self, user):
        self.owner = user.uid
        user.budget -= self.price
        db.session.commit()
        
    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()
