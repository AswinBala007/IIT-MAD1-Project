from db import db
from flask_login import UserMixin

# from marshmallow import Schema, fields, validates, ValidationError
# from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False) 
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

class Sponsor(User):
    __tablename__ = 'sponsors'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    name = db.Column(db.String, nullable=True)
    companyName = db.Column(db.String, nullable=True)
    industry = db.Column(db.String)
    campaigns = db.relationship('Campaign', backref='sponsor', lazy=True)
    __mapper_args__ = {
        'polymorphic_identity': 'sponsor',
    }


# Many-to-many relationship table between Influencers and Niches
# influencer_niche = db.Table('influencer_niche',
#     db.Column('influencer_id', db.Integer, db.ForeignKey('influencers.id'), primary_key=True),
#     db.Column('niche_id', db.Integer, db.ForeignKey('niches.id'), primary_key=True)
# )

class Influencer(User):
    __tablename__ = 'influencers'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    name = db.Column(db.String)
    category = db.Column(db.String)
    niche = db.Column(db.String)
    followersCount = db.Column(db.Integer)
    campaignsParticipated = db.Column(db.Integer)
    ad_requests = db.relationship('AdRequest', backref='influencer', lazy=True)
    # niches = db.relationship('Niche', secondary=influencer_niche, lazy='subquery',
    #                          backref=db.backref('influencers', lazy=True))
    __mapper_args__ = {
        'polymorphic_identity': 'influencer',
    }

# class Niche(db.Model):
#     __tablename__ = 'niches'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False, unique=True)

class AdRequest(db.Model):
    __tablename__ = 'ad_requests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencers.id'))
    messages = db.Column(db.String)
    requirements = db.Column(db.String)
    payment_amount = db.Column(db.Integer)
    status = db.Column(db.String)

# Many-to-many relationship table between Campaigns and Niches
# campaign_niche = db.Table('campaign_niche',
#     db.Column('campaign_id', db.Integer, db.ForeignKey('campaigns.id'), primary_key=True),
#     db.Column('niche_id', db.Integer, db.ForeignKey('niches.id'), primary_key=True)
# )

class Campaign(db.Model):
    __tablename__ = 'campaigns'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    budget = db.Column(db.Integer)
    niche = db.Column(db.String)
    visibility = db.Column(db.String)
    goals = db.Column(db.String)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsors.id'))
    ad_requests = db.relationship('AdRequest', backref='campaigns', lazy=True)
    # niches = db.relationship('Niche', secondary=campaign_niche, lazy='subquery',
    #                          backref=db.backref('campaigns', lazy=True))