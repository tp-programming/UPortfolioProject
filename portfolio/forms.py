from flask_wtf import FlaskForm
from wtforms import StringField,  FloatField, SubmitField
from wtforms.validators import InputRequired, NumberRange

#Forms for everything to do with the portfolio section.

class PortfolioForm(FlaskForm):
    amount = FloatField(validators=[InputRequired(), NumberRange(min=0, max=9999999, message='Please enter a positive amount')])
    sell = SubmitField()

class SearchStock(FlaskForm):
    ticker_symbol = StringField()
    submit = SubmitField()


class BuyStock(FlaskForm):
    stock_amount = FloatField(validators=[InputRequired(), NumberRange(min=0, max=9999999, message='Please enter a positive amount')])
    buy = SubmitField()

class Listofstocks(FlaskForm):
    submit = SubmitField()