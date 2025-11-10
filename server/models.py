from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    #relationship: a customer can write many reviews
    #back_populates links this relationship to the 'item' attribute in Review

    reviews=db.relationship('Review', back_populates='customer')

    #creating an association proxy
    items= association_proxy('reviews', 'item')
    #Add Serialization
    serialize_rules=('-reviews.customer',)
    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    #relationship: an item can have many reviews
    # back_populates links this relationship to the 'item' attribute in Review

    reviews=db.relationship('Review', back_populates='item')

    #Add Serialization
    serialize_rules=('-reviews.item',)
    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

#review model to connect customers and items
class Review(db.Model, SerializerMixin):
    #table name in db
    __tablename__='reviews'

    id=db.Column(db.Integer, primary_key=True)
    comment=db.Column(db.String)
    #foreign for the customer that wrote the review
    customer_id=db.Column(db.Integer, db.ForeignKey('customers.id'))
    #foreign key for the item being reviewed
    item_id=db.Column(db.Integer, db.ForeignKey('items.id'))
    #relationship to link back to customer
    #allows the review.customer to get the customer object
    customer=db.relationship('Customer', back_populates='reviews')
    #relationship to link back to item
    item=db.relationship('Item', back_populates='reviews')

    #Add Serialization
    serialize_rules=('-customer.reviews','-item.reviews')

    # String representation for debugging
    def __repr__(self):
        return f'<Review {self.id}, {self.comment}>'