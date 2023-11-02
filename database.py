from sqlalchemy import create_engine, Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()


therapist_specialty_association = Table('therapist_specialty_association', Base.metadata,
                                       Column('therapist_id', Integer, ForeignKey('therapists.id')),
                                       Column('specialty_id', Integer, ForeignKey('specialties.id'))
                                       )


class Therapist(Base):
    __tablename__ = 'therapists'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    rating = Column(Float)
    total_ratings = Column(Integer)
    specialties = relationship("Specialty",
                               secondary=therapist_specialty_association,
                               back_populates="therapists")

    def __str__(self):
        return f"Therapist ID: {self.id}, Name: {self.name}, Location: {self.location}, Rating: {self.rating}, Total Ratings: {self.total_ratings}"


class Specialty(Base):
    __tablename__ = 'specialties'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    therapists = relationship("Therapist",
                             secondary=therapist_specialty_association,
                             back_populates="specialties")

    def __str__(self):
        return f"Specialty ID: {self.id}, Name: {self.name}"


class TherapistDatabase:
    def __init__(self, db_name):
        self.engine = create_engine(f'sqlite:///{db_name}', echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def populate_sample_data(self):
        specialty1 = Specialty(name='Anxiety')
        specialty2 = Specialty(name='Depression')
        specialty3 = Specialty(name='ADHD')

        therapist1 = Therapist(name='John Opiyo', location='Kisumu', rating=4.8, total_ratings=20)
        therapist1.specialties.append(specialty1)

        therapist2 = Therapist(name='Jane Wanjiru', location='Nakuru', rating=4.5, total_ratings=15)
        therapist2.specialties.append(specialty2)

        therapist3 = Therapist(name='Faith Kamau', location='Nairobi', rating=4.8, total_ratings=10)
        therapist3.specialties.append(specialty3)

        self.session.add_all([therapist1, therapist2, therapist3])
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





















# #import os
# from sqlalchemy import create_engine, Column, Integer, String, Float
# from sqlalchemy.orm import declarative_base
# from sqlalchemy.orm import sessionmaker

# Base = declarative_base()


# class Therapist(Base):
#     __tablename__ = 'therapists'

#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     specialty = Column(String)
#     location = Column(String)
#     rating = Column(Float)
#     total_ratings = Column(Integer)

#     def __str__(self):
#         return f"Therapist ID: {self.id}, Name: {self.name}, Specialty: {self.specialty}, Location: {self.location}, Rating: {self.rating}, Total Ratings: {self.total_ratings}"

# class TherapistDatabase:
#     def __init__(self, db_name):
#         self.engine = create_engine(f'sqlite:///{db_name}', echo=True)
#         Base.metadata.create_all(self.engine)
#         self.Session = sessionmaker(bind=self.engine)
#         self.session = self.Session()

#     def populate_sample_data(self):
#         sample_therapists = [
#             Therapist(name='John Opiyo', specialty='Anxiety',
#                       location='Kisumu', rating=4.8, total_ratings=20),
#             Therapist(name='Jane Wanjiru', specialty='Depression',
#                       location='Nakuru', rating=4.5, total_ratings=15),
#             Therapist(name='Faith Kamau', specialty='ADHD',
#                       location='Nairobi', rating=4.8, total_ratings=10),
#         ]
#         self.session.add_all(sample_therapists)
#         self.session.commit()

#     def get_all_therapists(self):
#         return self.session.query(Therapist).all()

#     def filter_therapists(self, filter_option, filter_value):
#         return self.session.query(Therapist).filter(getattr(Therapist, filter_option).like(f'%{filter_value}%')).all()

#     def review_therapist(self, therapist_id, rating):
#         therapist = self.session.query(Therapist).filter(
#             Therapist.id == therapist_id).first()
#         if therapist:
#             therapist.total_ratings += 1
#             therapist.rating = (
#                 therapist.rating * (therapist.total_ratings - 1) + rating) / therapist.total_ratings
#             self.session.commit()
#             print("Thank you for your review!")
#         else:
#             print("Therapist not found.")

#     def __del__(self):
#         self.session.close()
