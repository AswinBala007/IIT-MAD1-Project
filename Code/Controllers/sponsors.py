from flask import  app, redirect, render_template ,request,abort
from db import db
from datetime import datetime
from flask_smorest import Blueprint
from flask import jsonify
from flask_login import *
from sqlalchemy import and_, not_
from Models.models import *
from Schemas.schemas import *
from sqlalchemy.exc import SQLAlchemyError
from flask.views import MethodView

blp = Blueprint("sponsors",__name__,description="sponsors Apis")
   
@blp.route("/sponsor")
@login_required
def sponsor_home():
    sponsor = Sponsor.query.filter_by(id = current_user.id).first()
    campaign = Campaign.query.filter_by(sponsor_id=current_user.id).all()
    if campaign is None:
        return render_template('sponsor_home.html', sponsor=sponsor)
    return render_template("sponsors.html",user=current_user,sponsor=sponsor,campaign = campaign )

@blp.route('/sponsor/campaigns',methods=["GET","POST","DELETE"])
@login_required
def sponsor_campaigns():
    if request.method=="POST":
        campaign = Campaign.query.filter_by(sponsor_id = current_user.id).first()
        if not campaign:
            abort(404, message="Sponsor's campaign not found")
        campaign.name = request.form.get('name')
        campaign.description = request.form.get('description')
        campaign.start_date = datetime.strptime(request.form.get('start_date'),"%Y-%m-%d")
        campaign.end_date = datetime.strptime(request.form.get('end_date'),"%Y-%m-%d")
        campaign.budget = request.form.get('budget')
        campaign.visibility = request.form.get('visibility')
        campaign.goals = request.form.get('goals')

        try:
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating the campaign.")
        
        return redirect('/sponsor/campaigns')
    return render_template("sponsors.html",campaign = Campaign.query.filter_by(sponsor_id=current_user.id).all())

@blp.route('/sponsor/delete_campaign/<int:campaign_id>')
def delete_campaign(campaign_id):
    camp_id = Campaign.query.get(campaign_id)
    db.session.delete(camp_id)
    db.session.commit()
    return redirect('/sponsor/campaigns')

@blp.route('/sponsor/campaigns/<int:campaign_id>/delete_ad/<int:ad_id>')
def delete_campaign(campaign_id,ad_id):
    ad_id = AdRequest.query.get(ad_id)
    db.session.delete(ad_id)
    db.session.commit()
    return redirect('/sponsor/campaigns/'+str(campaign_id))

@blp.route('/sponsor/campaigns/<int:camp_id>',methods=["GET","POST"])
@login_required
def view_campaign(camp_id):
    camp = Campaign.query.filter_by(id=camp_id).first()
    comb = and_(AdRequest.campaign_id==camp.id,AdRequest.status=='pending')
    act_comb = and_(AdRequest.campaign_id==camp.id,AdRequest.status=="active")
    act = AdRequest.query.filter(act_comb).all()
    req_comb = and_(AdRequest.campaign_id==camp.id,AdRequest.status=="sent") 
    req = AdRequest.query.filter(req_comb).all()
    ad = AdRequest.query.filter(comb).all()
    inf = Influencer.query.all()
    return render_template("sponsors.html", camp=camp,ads = ad,inf=inf,actions=act,received_ads = req)

@blp.route('/sponsor/campaigns/<int:camp_id>/accept/<int:ad_id>')
@login_required
def req_accept(camp_id,ad_id):
    ad_id = AdRequest.query.get(ad_id)
    ad_id.status = "active"
    db.session.commit()
    return redirect('/sponsor/campaigns/'+str(camp_id))

@blp.route('/sponsor/campaigns/<int:camp_id>/reject/<int:ad_id>')
@login_required
def req_reject(camp_id,ad_id):
    ad_id = AdRequest.query.get(ad_id)
    ad_id.status = "rejected"
    db.session.commit()
    return redirect('/sponsor/campaigns/'+str(camp_id))

@blp.route('/sponsor/sponsor_stat')
@login_required
def sponsor_stat():
    public = Campaign.query.filter_by(visibility="public").count()
    private = Campaign.query.filter_by(visibility="private").count()
    sport = Campaign.query.filter_by(niche="Sport",sponsor_id=current_user.id).count()
    an = Campaign.query.filter_by(niche="Animal",sponsor_id=current_user.id).count()
    tr = Campaign.query.filter_by(niche = "Travel",sponsor_id=current_user.id).count()
    food = Campaign.query.filter_by(niche="Food",sponsor_id=current_user.id).count()
    ent = Campaign.query.filter_by(niche="Entertainment",sponsor_id=current_user.id).count()
    ot = Campaign.query.filter_by(niche="Others",sponsor_id=current_user.id).count()
    return render_template("sponsors.html",pub=public,pri=private,sport=sport,an=an,tr=tr,food=food,ot=ot,en=ent)

@blp.route('/sponsor/add_campaign',methods=["GET","POST"])
@login_required
def add_campaign():
    if request.method == "POST":
        cname = request.form['name']
        cdescription = request.form['description']
        cstart_date = datetime.strptime(request.form['start_date'],"%Y-%m-%d")
        cend_date = datetime.strptime(request.form['end_date'],"%Y-%m-%d")
        cbudget = request.form['budget']
        cvisibility = request.form['visibility']
        cgoals = request.form['goals']
        cniche = request.form.get('niche')
        campaign = Campaign(name=cname, description=cdescription, start_date=cstart_date, end_date=cend_date,niche=cniche, budget=cbudget, visibility=cvisibility, goals=cgoals, sponsor_id=current_user.id)
        db.session.add(campaign)
        db.session.commit()
        return redirect('/sponsor/campaigns')
    return render_template("sponsors.html")

@blp.route('/sponsor/edit_campaigns/<int:ca_id>',methods=["GET","POST"])
@login_required
def edit_campaign(ca_id):
    ca = Campaign.query.filter_by(id=ca_id).first()
    if request.method=="POST":
        ca.name = request.form['name']
        ca.description = request.form['description']
        ca.start_date = datetime.strptime(request.form['start_date'],"%Y-%m-%d")
        ca.end_date = datetime.strptime(request.form['end_date'],"%Y-%m-%d")
        ca.budget = request.form['budget']
        ca.visibility = request.form['visibility']
        ca.goals = request.form['goals']
        ca.niche = request.form["niche"]
        db.session.commit()
        return redirect('/sponsor/campaigns')
    return render_template("sponsors.html",camp = Campaign.query.filter_by(id=ca_id).first())


@blp.route("/sponsor/campaigns/<int:ca_id>/add_requests",methods=["GET","POST"])
@login_required
def add_requests(ca_id):
    ca = Campaign.query.filter_by(id=ca_id).first()
    inf = Influencer.query.filter_by(niche=ca.niche).all()
    if request.method == "POST":
        inf_id = request.form['influencer_id']
        adname = request.form['adname']
        admsg = request.form["messages"]
        # adreq = request.form["requirements"]
        adpay = ca.budget
        # adreqstatus = request.form["status"]
        ad=AdRequest(campaign_id=ca_id,influencer_id=inf_id,name=adname,messages=admsg,requirements="",payment_amount=adpay,status="pending")
        db.session.add(ad)
        db.session.commit()
        return redirect('/sponsor/campaigns/'+str(ca_id))
    
    return render_template("sponsors.html",inf=inf,camp=ca)

@blp.route('/sponsor/edit_profile')
class SponsorProfile(MethodView):
    @login_required
    def get(self):
        return render_template("sponsors.html",user=current_user,sponsor=Sponsor.query.filter_by(id=current_user.id).first())

    @login_required
    def post(self):
        sponsor = Sponsor.query.filter_by(id=current_user.id).first()
        if not sponsor:
            abort(404, message="Sponsor not found")
        name = request.form.get('name')
        company = request.form.get('company')
        industry = request.form.get('industry')

        sponsor.name = name
        sponsor.companyName = company
        sponsor.industry = industry

        try:
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating the influencer profile.")
        
        return redirect('/sponsor')

@blp.route('/sponsor/find_influencers/request/<int:id>',methods=["GET","POST"])
def sponsor_request(id):
    inf = Influencer.query.filter_by(id=id).first()
    camp = Campaign.query.filter_by(niche=inf.niche).all()
    return render_template("sponsors.html",i=inf,camp=camp,ad =inf)
    # --------------------- ads ----------------------


@blp.route('/sponsor/find_influencers', methods=['GET', 'POST'])
def find_influencers():
    search_query = "%"+request.args.get('search', '')+"%"
    inf = Influencer.query.filter(Influencer.name.like(search_query)).all()
    print(search_query)
    print(inf)
    return render_template('sponsors.html', inf=inf)