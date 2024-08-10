# from flask import jsonify
# from flask_smorest import Blueprint, abort
# from flask.views import MethodView
# from flask_login import login_required, current_user
# from sqlalchemy.exc import SQLAlchemyError

# from db import db
# # from Models.models import Sponsor, Influencer, Niche
# from Schemas.schemas import *

# blp = Blueprint("profile", __name__, description="Profile APIs")

# @blp.route('/edit_sponsor')
# class EditSponsorProfile(MethodView):
#     @login_required
#     @blp.arguments(SponsorInputSchema)
#     @blp.response(200, description="Sponsor profile updated successfully")
#     @blp.alt_response(403, description="Only sponsors can edit sponsor profiles")
#     @blp.alt_response(500, description="An error occurred while updating the profile")
#     def put(self, data):
#         if not isinstance(current_user, Sponsor):
#             abort(403, message="Only sponsors can edit sponsor profiles.")

#         try:
#             for field in ['name', 'companyName', 'industry']:
#                 if field in data:
#                     setattr(current_user, field, data[field])

#             db.session.commit()
#         except SQLAlchemyError as e:
#             db.session.rollback()
#             abort(500, message=str(e))

#         return {"message": "Sponsor profile updated successfully."}


# @blp.route('/edit_influencer')
# class EditInfluencerProfile(MethodView):
#     @login_required
#     @blp.arguments(InfluencerInputSchema)
#     @blp.response(200, description="Influencer profile updated successfully")
#     @blp.alt_response(403, description="Only influencers can edit influencer profiles")
#     @blp.alt_response(500, description="An error occurred while updating the profile")
#     def put(self, data):
#         if not isinstance(current_user, Influencer):
#             abort(403, message="Only influencers can edit influencer profiles.")

#         try:
#             for field in ['name', 'category', 'followersCount', 'campaignsParticipated']:
#                 if field in data:
#                     setattr(current_user, field, data[field])

#             if 'niches' in data:
#                 current_user.niches.clear()
#                 for niche_name in data['niches']:
#                     niche = Niche.query.filter_by(name=niche_name).first()
#                     if not niche:
#                         niche = Niche(name=niche_name)
#                         db.session.add(niche)
#                     current_user.niches.append(niche)

#             db.session.commit()
#         except SQLAlchemyError as e:
#             db.session.rollback()
#             abort(500, message=str(e))

#         return {"message": "Influencer profile updated successfully."}