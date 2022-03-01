from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import login_required, current_user
import yfinance as yf
from app import db
from models import Stock, User
from portfolio.forms import PortfolioForm, SearchStock, BuyStock
from portfolio.search import searchforstock
import csv

portfolio_blueprint = Blueprint('portfolio', __name__, template_folder='templates')

#Page for the portfolio.

@portfolio_blueprint.route('/portfolio', methods=('GET', 'POST'))
@login_required
def portfolio():
    form = PortfolioForm()
    transactions = Stock.query.filter_by(id=current_user.id).all()

    #Update all the transactions current prices and therefore the profit amount.
    for i in transactions:

        new_price = searchforstock(f'{i.stock_symbol}')
        profit = (new_price-i.bought_price)*i.amount
        i.current_price=new_price
        i.profit_loss = profit
        db.session.commit()

    money = current_user.money

    if form.validate_on_submit():


        stockid = request.form.get("stockid","")

        stockQuery = Stock.query.filter_by(stock_id=stockid).all()

        #Checks if amount entered is suitable and then peforms the change.

        for i in stockQuery:

            if i.amount < form.amount.data:
                return redirect(url_for('portfolio.portfolio'))
            if i.amount == form.amount.data:

                totalprofit = i.amount * i.current_price
                current_user.money = current_user.money+totalprofit
                Stock.query.filter_by(stock_id=stockid).delete()
                db.session.commit()
                return redirect(url_for('portfolio.portfolio'))

            if i.amount > form.amount.data:
                totalprofit = form.amount.data * i.current_price
                current_user.money = current_user.money+totalprofit
                i.amount = i.amount - form.amount.data
                db.session.commit()

        return redirect(url_for('portfolio.portfolio'))

    return render_template('portfolio.html', form=form, transactions=transactions, money=money)


@portfolio_blueprint.route('/searchstock', methods=('GET', 'POST'))
@login_required
def searchstock():
    form = SearchStock()
    if form.validate_on_submit():

        output = searchforstock(f'{form.ticker_symbol.data}')

        #This checks that the search for stock wasn't found and if so queries the nasdaq database to find a potential match.

        if isinstance(output,str) == True:

            global list_stocks
            list_stocks = []

            global list_stocks_name
            list_stocks_name = []

            with open('nasdaq_screener.csv', newline='') as csvfile:
                data = list(csv.reader(csvfile))

            edited_user_input = form.ticker_symbol.data.lower()

            for i in data:

                string = ' '.join([str(item) for item in i])
                lower_string = string.lower()
                if edited_user_input in lower_string:
                    print(i[1])
                    print('The ticker symbol is: ' + i[0])
                    list_stocks.append(i[0])
                    list_stocks_name.append(i[1])

            #If there are no list of stocks then it will just reload the page.

            if list_stocks == []:
                return render_template('searchstock.html', form=form)

            return redirect(url_for('portfolio.listofstocks', list_stocks=list_stocks, list_stocks_name=list_stocks_name))



        global price
        price = float(output)
        global ticker
        ticker = form.ticker_symbol.data

        return redirect(url_for('portfolio.foundstock', ticker=ticker, price=price))
    return render_template('searchstock.html', form=form)

@portfolio_blueprint.route('/listofstocks', methods=('GET', 'POST'))
@login_required
def listofstocks():

    if request.method == 'POST':

        #By looping through in the HTML the submittion button is also assigned to whichever ticker symbol is presented.

        whichstock = request.form.get('whichstock')

        global ticker
        ticker = whichstock
        global price
        price = float(searchforstock(f'{ticker}'))

        return redirect(url_for('portfolio.foundstock', ticker=ticker, price=price))


    return render_template('listofstocks.html', output=list_stocks, output2=list_stocks_name)





@portfolio_blueprint.route('/foundstock', methods=('GET', 'POST'))
@login_required
def foundstock():
    form = BuyStock()

    money = current_user.money

    ticker_symbol = yf.Ticker(f'{ticker}')

    longName = 'longName'

    stock_long_name = ticker_symbol.info.get(longName)

    if stock_long_name:
        company_name = ticker_symbol.info['longName']
    else:
        company_name = ticker.upper()

    if form.validate_on_submit():

        new_transaction = Stock(id=current_user.id, stock_name=company_name, stock_symbol=ticker, amount=form.stock_amount.data, bought_price=price, current_price=price, profit_loss=0)

        userinformation = User.query.filter_by(id=current_user.id).all()

        for i in userinformation:
            if i.money < (form.stock_amount.data*price):
                return render_template('foundstock.html', output=price, company_name=company_name, form=form, ticker=ticker)
            old_money = i.money
            i.money = old_money-(form.stock_amount.data*price)
            db.session.add(new_transaction)
            db.session.commit()


        return redirect(url_for('portfolio.portfolio'))

    return render_template('foundstock.html', output=price, company_name=company_name, form=form, money=money)