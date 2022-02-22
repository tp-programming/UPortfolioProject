from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import login_required, current_user
import yfinance as yf
from app import db
from models import Stock, User
from portfolio.forms import PortfolioForm, SearchStock, BuyStock
from portfolio.search import searchforstock

portfolio_blueprint = Blueprint('portfolio', __name__, template_folder='templates')

@portfolio_blueprint.route('/portfolio', methods=('GET', 'POST'))
@login_required
def portfolio():
    form = PortfolioForm()

    transactions = Stock.query.filter_by(id=current_user.id).all()


    for i in transactions:

        new_price = searchforstock(f'{i.stock_symbol}')
        profit = (new_price-i.bought_price)*i.amount
        i.current_price=new_price
        i.profit_loss = profit
        db.session.commit()

    userinformation = User.query.filter_by(id=current_user.id).all()

    if form.validate_on_submit():
        print(form.amount.data)

        stockid = request.form.get("stockid","")
        print(stockid)

        thequery = Stock.query.filter_by(stock_id=stockid).all()

        print(thequery)
        for i in thequery:
            if i.amount < form.amount.data:
                return render_template('portfolio.html', form=form, transactions=transactions, userinformation=userinformation)
            if i.amount == form.amount.data:
                totalprofit = i.amount * i.current_price
                current_user.money = current_user.money+totalprofit
                db.session.commit()

                Stock.query.filter_by(stock_id=stockid).delete()
                db.session.commit()
            if i.amount > form.amount.data:
                totalprofit = form.amount.data * i.current_price
                current_user.money = current_user.money+totalprofit
                i.amount = i.amount - form.amount.data
                db.session.commit()





        return render_template('index.html')




    return render_template('portfolio.html', form=form, transactions=transactions, userinformation=userinformation)


@portfolio_blueprint.route('/searchstock', methods=('GET', 'POST'))
@login_required
def searchstock():
    form = SearchStock()
    if form.validate_on_submit():
        output = searchforstock(f'{form.ticker_symbol.data}')
        if isinstance(output,str) == True:
            return render_template('searchstock.html', form=form)
        global price
        price = float(output)
        global ticker
        ticker = form.ticker_symbol.data

        return redirect(url_for('portfolio.foundstock'))
    return render_template('searchstock.html', form=form)

@portfolio_blueprint.route('/foundstock', methods=('GET', 'POST'))
@login_required
def foundstock():
    form = BuyStock()
    searchstock()

    ticker_symbol = yf.Ticker(f'{ticker}')

    longName = 'longName'

    this = ticker_symbol.info.get(longName)

    if this:
        company_name = ticker_symbol.info['longName']
    else:
        company_name = ticker.upper()

    if form.validate_on_submit():

        new_transaction = Stock(id=current_user.id, stock_name=company_name, stock_symbol=ticker, amount=form.stock_amount.data, bought_price=price, current_price=price, profit_loss=0)

        userinformation = User.query.filter_by(id=current_user.id).all()

        for i in userinformation:
            if i.money < (form.stock_amount.data*price):
                return render_template('foundstock.html', output=price, company_name=company_name, form=form)
            oldcash = i.money
            newcash = oldcash-(form.stock_amount.data*price)
            i.money = newcash
            db.session.add(new_transaction)
            db.session.commit()


        return render_template('index.html')

    return render_template('foundstock.html', output=price, company_name=company_name, form=form)