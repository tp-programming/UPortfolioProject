from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField


class PortfolioForm(FlaskForm):
    amount = FloatField()
    sell = SubmitField()

class SearchStock(FlaskForm):
    ticker_symbol = StringField()
    submit = SubmitField()


class BuyStock(FlaskForm):
    stock_amount = FloatField()
    submit = SubmitField()

class Listofstocks(FlaskForm):
    submit = SubmitField()