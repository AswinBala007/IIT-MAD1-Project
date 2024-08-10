from flask import  redirect, render_template, request, jsonify, url_for
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_login import current_user, login_required
from sqlalchemy import and_, intersect
from sqlalchemy.exc import SQLAlchemyError
from Models.models import Influencer, AdRequest , Campaign
from db import db

blp = Blueprint("influencers", __name__, description="Influencer APIs")

@blp.route("/influencer")
@login_required
def influener_home():
    # comb = and_(Campaign.niche == current_user.niche , AdRequest.influencer_id==current_user.id,AdRequest.status=="on process")
    camp = db.session.query(Campaign).join(AdRequest,AdRequest.campaign_id==Campaign.id).filter(AdRequest.influencer_id==current_user.id,AdRequest.status=="active").all()
    camp_req = db.session.query(AdRequest).join(Campaign,AdRequest.campaign_id==Campaign.id).filter(AdRequest.influencer_id==current_user.id,AdRequest.status=="pending").all()
    # print(camp_req[:])
    return render_template("influencer.html",user=current_user,influencer=Influencer.query.filter_by(id=current_user.id).first(),campaign =  camp,campaign_req = camp_req)


@blp.route('/influencer/find_campaigns',methods=["GET","POST"])
@login_required
def influencer_find_influencers():
    # print(current_user.niche)
    # combined = and_((Campaign.niche==current_user.niche),(Campaign.visibility=="public"))
    search_query = "%"+request.args.get('search', '')+"%"
    # camp = db.session.query(Campaign).join(AdRequest,AdRequest.campaign_id==Campaign.id).filter(AdRequest.influencer_id==current_user.id,AdRequest.status!="active",AdRequest.status=='pending').all()
    camp = db.session.query(Campaign).join(AdRequest,AdRequest.campaign_id==Campaign.id).filter(AdRequest.influencer_id==current_user.id,AdRequest.status!="active").filter(Campaign.name.like(search_query)).all()
    camp =Campaign.query.filter(Campaign.name.like(search_query)).all()
    return render_template("influencer.html",camp = camp)

# @blp.route('/influencer/influencer_stat')
# @login_required
# def influencer_stat():
#     return render_template("influencer.html")

@blp.route('/influencer/edit_profile')
class InfluencerProfile(MethodView):
    @login_required
    def get(self):
        influencer = Influencer.query.filter_by(id=current_user.id).first()
        return render_template("influencer.html", user=current_user, influencer=influencer)
    
    @login_required
    def post(self):
        influencer = Influencer.query.filter_by(id=current_user.id).first()
        if not influencer:
            abort(404, message="Influencer not found.")
        name = request.form.get('name')
        followersCount = request.form.get('followersCount')
        category = request.form.get('category')
        niche = request.form.get('niche')
        influencer.name = name
        influencer.followersCount = followersCount
        influencer.category = category
        influencer.niche = niche
        
        try:
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating the influencer profile.")
        
        return redirect('/influencer')

@blp.route("/influencer/find_campaigns/sentreq/<int:id>")
@login_required
def sentreq(id):
    camp = Campaign.query.filter_by(id=id).first()
    name = camp.name + str(id)
    ad = AdRequest(name=name,campaign_id=camp.id,payment_amount=camp.budget,influencer_id=current_user.id,status="sent")
    db.session.add(ad)
    db.session.commit()
    return redirect('/influencer/find_campaigns')
    
@blp.route('/influencer/accept/<int:id>')
@login_required
def accept(id):
    ad = AdRequest.query.filter_by(id=id).first()
    ad.status = "active"
    db.session.commit()
    return redirect('/influencer')


@blp.route('/influencer/find_campaigns/negotiate/<int:campaign_id>', methods=['POST',"GET"])
def negotiate_payment(campaign_id):
    if request.method=="POST":
        payment_amount = request.form['payment']
        # db.session.query(AdRequest).filter(campaign_id=campaign_id,influencer_id=current_user.id).update({'requirements': payment_amount,'status':"negotiating"})
        ad = AdRequest.query.filter_by(id=campaign_id,influencer_id=current_user.id).first()
        ad.requirements = payment_amount
        ad.status = "negotiating"
        db.session.commit()
        return redirect('/influencer/find_campaigns')
    return redirect('/influencer/find_campaigns')

@blp.route('/influencer/influencer_stat')
def inf_chart():
    # sp = .query.filter_by(niche="Sport",sponsor_id=current_user.id).count()
    # an = Influencer.query.filter_by(niche="Animal",sponsor_id=current_user.id).count()
    # tr = Influencer.query.filter_by(niche = "Travel",sponsor_id=current_user.id).count()
    # food = Influencer.query.filter_by(niche="Food",sponsor_id=current_user.id).count()
    # ent = Influencer.query.filter_by(niche="Entertainment",sponsor_id=current_user.id).count()
    # ot = Influencer.query.filter_by(niche="Others",sponsor_id=current_user.id).count()
    # return render_template('inf_chart.html',sp=sp,an =an,tr=tr,food=food,ot=ot,ent=ent)
    act = AdRequest.query.filter_by(influencer_id=current_user.id,status="active").count()
    inact = AdRequest.query.filter_by(influencer_id=current_user.id).count() - act
    return render_template('influencer.html',act=act,inact=inact)