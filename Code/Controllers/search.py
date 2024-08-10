from flask import jsonify, request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_login import current_user, login_required
from sqlalchemy import or_
from Models.models import Influencer, Campaign, AdRequest

blp = Blueprint("search", __name__, description="Search APIs")

@blp.route('/search/campaigns')
class CampaignSearch(MethodView):
    @login_required
    def get(self):
        if not isinstance(current_user, Influencer):
            abort(403, message="Only influencers can search for campaigns.")

        niche = request.args.get('niche')
        campaign_name = request.args.get('name')

        campaigns_query = Campaign.query.filter_by(visibility='public')

        if niche:
            campaigns_query = campaigns_query.filter(Campaign.goals.ilike(f'%{niche}%'))
        
        if campaign_name:
            campaigns_query = campaigns_query.filter(Campaign.name.ilike(f'%{campaign_name}%'))

        campaigns = campaigns_query.all()

        campaigns_data = [
            {
                'id': campaign.id,
                'name': campaign.name,
                'description': campaign.description,
                'start_date': campaign.start_date,
                'end_date': campaign.end_date,
                'budget': campaign.budget,
                'visibility': campaign.visibility,
                'goals': campaign.goals,
                'sponsor': campaign.sponsor.name if campaign.sponsor else None
            }
            for campaign in campaigns
        ]

        return jsonify({'campaigns': campaigns_data}), 200

@blp.route('/ad_requests/pending')
class PendingAdRequests(MethodView):
    @login_required
    def get(self):
        if not isinstance(current_user, Influencer):
            abort(403, message="Only influencers can view pending ad requests.")

        pending_ad_requests_query = AdRequest.query.filter_by(influencer_id=current_user.id, status='Pending')

        campaign_name = request.args.get('campaign_name')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        min_budget = request.args.get('min_budget', type=int)
        max_budget = request.args.get('max_budget', type=int)

        if campaign_name:
            pending_ad_requests_query = pending_ad_requests_query.join(Campaign).filter(Campaign.name.ilike(f'%{campaign_name}%'))
        
        if start_date:
            pending_ad_requests_query = pending_ad_requests_query.join(Campaign).filter(Campaign.start_date >= start_date)
        
        if end_date:
            pending_ad_requests_query = pending_ad_requests_query.join(Campaign).filter(Campaign.end_date <= end_date)
        
        if min_budget is not None:
            pending_ad_requests_query = pending_ad_requests_query.join(Campaign).filter(Campaign.budget >= min_budget)
        
        if max_budget is not None:
            pending_ad_requests_query = pending_ad_requests_query.join(Campaign).filter(Campaign.budget <= max_budget)
        
        pending_ad_requests = pending_ad_requests_query.all()

        pending_ad_requests_data = [
            {
                'id': ad_request.id,
                'campaign_id': ad_request.campaign_id,
                'campaign_name': ad_request.campaign.name,
                'messages': ad_request.messages,
                'requirements': ad_request.requirements,
                'payment_amount': ad_request.payment_amount,
                'status': ad_request.status
            }
            for ad_request in pending_ad_requests
        ]

        return jsonify({'pending_ad_requests': pending_ad_requests_data}), 200
    
    

    
    
# blp = Blueprint("search", __name__, description="Search APIs")

# @blp.route('/search/campaigns')
# class CampaignSearch(MethodView):
#     @login_required
#     def get(self):
#         if not isinstance(current_user, Influencer):
#             abort(403, message="Only influencers can search for campaigns.")

#         # Start with a base query
#         query = Campaign.query.filter_by(visibility='public')

#         # Define all possible filters
#         filters = {
#             'name': lambda x: Campaign.name.ilike(f'%{x}%'),
#             'niche': lambda x: Campaign.goals.ilike(f'%{x}%'),
#             'min_budget': lambda x: Campaign.budget >= float(x),
#             'max_budget': lambda x: Campaign.budget <= float(x),
#             'start_date': lambda x: Campaign.start_date >= datetime.strptime(x, '%Y-%m-%d'),
#             'end_date': lambda x: Campaign.end_date <= datetime.strptime(x, '%Y-%m-%d'),
#             'sponsor': lambda x: Campaign.sponsor.has(name=x)
#         }

#         # Apply filters based on query parameters
#         for param, filter_func in filters.items():
#             value = request.args.get(param)
#             if value:
#                 query = query.filter(filter_func(value))

#         # Pagination
#         page = request.args.get('page', 1, type=int)
#         per_page = request.args.get('per_page', 20, type=int)
#         paginated_campaigns = query.paginate(page=page, per_page=per_page, error_out=False)

#         campaigns_data = [
#             {
#                 'id': campaign.id,
#                 'name': campaign.name,
#                 'description': campaign.description,
#                 'start_date': campaign.start_date.isoformat(),
#                 'end_date': campaign.end_date.isoformat(),
#                 'budget': campaign.budget,
#                 'visibility': campaign.visibility,
#                 'goals': campaign.goals,
#                 'sponsor': campaign.sponsor.name if campaign.sponsor else None
#             }
#             for campaign in paginated_campaigns.items
#         ]

#         return jsonify({
#             'campaigns': campaigns_data,
#             'total': paginated_campaigns.total,
#             'pages': paginated_campaigns.pages,
#             'page': page
#         }), 200


# @blp.route('/ad_requests/pending')
# class PendingAdRequests(MethodView):
#     @login_required
#     def get(self):
#         if not isinstance(current_user, Influencer):
#             abort(403, message="Only influencers can view pending ad requests.")

#         query = AdRequest.query.filter_by(influencer_id=current_user.id, status='Pending')

#         filters = {
#             'campaign_name': lambda x: Campaign.name.ilike(f'%{x}%'),
#             'start_date': lambda x: Campaign.start_date >= datetime.strptime(x, '%Y-%m-%d'),
#             'end_date': lambda x: Campaign.end_date <= datetime.strptime(x, '%Y-%m-%d'),
#             'min_budget': lambda x: Campaign.budget >= float(x),
#             'max_budget': lambda x: Campaign.budget <= float(x),
#         }

#         for param, filter_func in filters.items():
#             value = request.args.get(param)
#             if value:
#                 query = query.join(Campaign).filter(filter_func(value))

#         # Add pagination here as well

#         pending_ad_requests = query.all()

#         # Format the response...

#         return jsonify({'pending_ad_requests': pending_ad_requests_data}), 200