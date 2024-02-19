#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)

    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)

    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)

    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    # HBNB_TYPE_STORAGE can be “file” (FileStorage) or db (DBStorage)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship('Review', backref="place",
                               cascade="all, delete")
    else:
        @property
        def reviews(self):
            ''' FileStorage relationship between Place and Review
            returns the list of Review instances with place_id
            equals to the current Place.id '''
            from models import storage
            from models.review import Review
            review_list = []
            for review in list(storage.all(Review).values()):
                if self.id == review.place_id:
                    review_list.append(review)
            return review_list
