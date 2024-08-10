from flask import jsonify
from sqlalchemy.sql import func
from Models.models import *
from flask_smorest import Blueprint
from flask import jsonify

from sqlalchemy import not_

blp = Blueprint("admin",__name__,description="amin Apis")

@blp.route('/admin/stats', methods=['GET'])
def admin_stats():

    active_influencers_count = Influencer.query.filter(
        Influencer.last_login >= func.current_date() - 30
    ).count()
    active_sponsors_count = Sponsor.query.filter(
        Sponsor.last_login >= func.current_date() - 30
    ).count()
    
    total_campaigns_count = Campaign.query.count()
    
    public_campaigns_count = Campaign.query.filter_by(visibility='public').count()
    private_campaigns_count = Campaign.query.filter_by(visibility='private').count()
    
    total_ad_requests_count = AdRequest.query.count()
    pending_ad_requests_count = AdRequest.query.filter_by(status='Pending').count()
    accepted_ad_requests_count = AdRequest.query.filter_by(status='Accepted').count()
    rejected_ad_requests_count = AdRequest.query.filter_by(status='Rejected').count()
    
    flagged_influencers_count = Influencer.query.filter_by(flagged=True).count()
    flagged_sponsors_count = Sponsor.query.filter_by(flagged=True).count()
    
    stats = {
        'active_influencers': active_influencers_count,
        'active_sponsors': active_sponsors_count,
        'total_campaigns': total_campaigns_count,
        'public_campaigns': public_campaigns_count,
        'private_campaigns': private_campaigns_count,
        'total_ad_requests': total_ad_requests_count,
        'pending_ad_requests': pending_ad_requests_count,
        'accepted_ad_requests': accepted_ad_requests_count,
        'rejected_ad_requests': rejected_ad_requests_count,
        'flagged_influencers': flagged_influencers_count,
        'flagged_sponsors': flagged_sponsors_count,
    }
    
    return jsonify(stats)
