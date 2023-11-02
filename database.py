#import os
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Therapist(Base):
    __tablename__ = 'therapists'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    specialty = Column(String)
    location = Column(String)
    rating = Column(Float)
    total_ratings = Column(Integer)

    def __str__(self):
        return f"Therapist ID: {self.id}, Name: {self.name}, Specialty: {self.specialty}, Location: {self.location}, Rating: {self.rating}, Total Ratings: {self.total_ratings}"

class TherapistDatabase:
    def __init__(self, db_name):
        self.engine = create_engine(f'sqlite:///{db_name}', echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def populate_sample_data(self):
        sample_therapists = [
            Therapist(name='John Opiyo', specialty='Anxiety',
                      location='Kisumu', rating=4.8, total_ratings=20),
            Therapist(name='Jane Wanjiru', specialty='Depression',
                      location='Nakuru', rating=4.5, total_ratings=15),
            Therapist(name='Faith Kamau', specialty='ADHD',
                      location='Nairobi', rating=4.8, total_ratings=10),
        ]
        self.session.add_all(sample_therapists)
        self.session.commit()

    def get_all_therapists(self):
        return self.session.query(Therapist).all()

    def filter_therapists(self, filter_option, filter_value):
        return self.session.query(Therapist).filter(getattr(Therapist, filter_option).like(f'%{filter_value}%')).all()

    def review_therapist(self, therapist_id, rating):
        therapist = self.session.query(Therapist).filter(
            Therapist.id == therapist_id).first()
        if therapist:
            therapist.total_ratings += 1
            therapist.rating = (
                therapist.rating * (therapist.total_ratings - 1) + rating) / therapist.total_ratings
            self.session.commit()
            print("Thank you for your review!")
        else:
            print("Therapist not found.")

    def __del__(self):
        self.session.close()
