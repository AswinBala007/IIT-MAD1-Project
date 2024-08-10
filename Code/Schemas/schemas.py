from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, validate=validate.Length(min=6))
    type = fields.Str(dump_only=True)

class RegisterSchema(UserSchema):
    role = fields.Str(required=True, validate=validate.OneOf(['influencer', 'sponsor']))
    name = fields.Str(required=True)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))


class SponsorSchema(UserSchema):
    name = fields.Str()
    companyName = fields.Str()
    industry = fields.Str()
    campaigns = fields.Nested('CampaignSchema', many=True, exclude=('sponsor',), dump_only=True)

class NicheSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class InfluencerSchema(UserSchema):
    name = fields.Str()
    category = fields.Str()
    followersCount = fields.Int()
    campaignsParticipated = fields.Int()
    niches = fields.Nested(NicheSchema, many=True)
    ad_requests = fields.Nested('AdRequestSchema', many=True, exclude=('influencer',), dump_only=True)

class AdRequestSchema(Schema):
    id = fields.Int(dump_only=True)
    campaign_id = fields.Int(required=True)
    influencer_id = fields.Int(required=True)
    messages = fields.Str()
    requirements = fields.Str()
    payment_amount = fields.Int()
    status = fields.Str()
    campaign = fields.Nested('CampaignSchema', exclude=('ad_requests',))
    influencer = fields.Nested(InfluencerSchema, exclude=('ad_requests',))

class CampaignSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    budget = fields.Int(required=True)
    visibility = fields.Str(required=True, validate=validate.OneOf(["public", "private"]))
    goals = fields.Str(required=True)
    sponsor_id = fields.Int(required=True)
    niches = fields.Nested(NicheSchema, many=True)
    ad_requests = fields.Nested(AdRequestSchema, many=True, exclude=('campaign',), dump_only=True)
    sponsor = fields.Nested(SponsorSchema, exclude=('campaigns',))

    # @validates('end_date')
    # def validate_end_date(self, value):
    #     if 'start_date' in self.context and value < self.context['start_date']:
    #         raise ValidationError('End date must be after start date.')

    # @validates('start_date')
    # def validate_start_date(self, value):
    #     if value < datetime.now().date():
    #         raise ValidationError('Start date cannot be in the past.')

# Input schemas (for creating/updating)
class UserInputSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

class SponsorInputSchema(UserInputSchema):
    name = fields.Str()
    companyName = fields.Str()
    industry = fields.Str()

class InfluencerInputSchema(UserInputSchema):
    name = fields.Str()
    category = fields.Str()
    followersCount = fields.Int()
    campaignsParticipated = fields.Int()
    niches = fields.List(fields.Str(), required=False)

class AdRequestInputSchema(Schema):
    campaign_id = fields.Int(required=True)
    influencer_id = fields.Int(required=True)
    messages = fields.Str()
    requirements = fields.Str()
    payment_amount = fields.Int()
    status = fields.Str()

class CampaignInputSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    budget = fields.Int(required=True)
    visibility = fields.Str(required=True, validate=validate.OneOf(["public", "private"]))
    goals = fields.Str(required=True)
    niches = fields.List(fields.Str(), required=False)

    @validates('end_date')
    def validate_end_date(self, value):
        if 'start_date' in self.context and value < self.context['start_date']:
            raise ValidationError('End date must be after start date.')

    @validates('start_date')
    def validate_start_date(self, value):
        if value < datetime.now().date():
            raise ValidationError('Start date cannot be in the past.')