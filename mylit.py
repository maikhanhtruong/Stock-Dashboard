# This project uses plotly and streamlit to provide basic dashboard and downloadable Performances Visualizations

from sys import _enablelegacywindowsfsencoding
import streamlit as st
import pandas as pd
import matplotlib as plt
import datetime
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from bs4 import BeautifulSoup

st.title('Basic Stock Performance Dashboard')

# Organize side bar including chosing a stock the information Type ( Financial Summary, Visualization)
symbols={'TSLA','GME' }

ticker= st.sidebar.radio('Chose a Stock from below'
                         , symbols)

info=st.sidebar.radio('What do you want to know?',
                      ('Basic Information','Financial Summary','Stock performance')
                      )

#Define makeGraph Function (from IBM Python Project for Data Analyse)

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

# Get Financial Summary

stock=yf.Ticker(ticker)


if(info=='Basic Information'):
    st.title('Company Profile')
    st.subheader(stock.info['longName'])
    st.info(stock.info['longBusinessSummary'])
    basicinfo={
        'Sector': stock.info['sector'],
        'Industry': stock.info['industry'],
        'Country': stock.info['country'],
        'Website': stock.info['website'],
        }

    
    basicinfoDF = pd.DataFrame.from_dict(basicinfo, orient='index')
    basicinfoDF = basicinfoDF.rename(columns={0: ''})
    st.subheader('Fundamental Info')
    st.table(basicinfoDF)
    
    fundInfo = {
            'Enterprise Value (USD)': stock.info['enterpriseValue'],
            'Enterprise To Revenue Ratio': stock.info['enterpriseToRevenue'],
            'Enterprise To Ebitda Ratio': stock.info['enterpriseToEbitda'],
            'Net Income (USD)': stock.info['netIncomeToCommon'],
            'Profit Margin Ratio': stock.info['profitMargins'],
            'Forward PE Ratio': stock.info['forwardPE'],
            'PEG Ratio': stock.info['pegRatio'],
            'Price to Book Ratio': stock.info['priceToBook'],
            'Forward EPS (USD)': stock.info['forwardEps'],
            'Beta ': stock.info['beta'],
            'Book Value (USD)': stock.info['bookValue'],
            'Payout Ratio': stock.info['payoutRatio']
        }
    
    fundDF = pd.DataFrame.from_dict(fundInfo, orient='index')
    fundDF = fundDF.rename(columns={0: 'Value'})
    st.subheader('More Information') 
    st.table(fundDF)
 # show financials
elif(info=='Financial Summary'):
    
    what = st.selectbox(
    'Chose report type',
     ('Quarterly reports','Annual reports')
     )
    if (what=='Quarterly reports'):
        st.subheader('Quarterly Financial Report')
        stock.quarterly_financials
        st.subheader('Quarterly Balance Sheet')
        stock.quarterly_balance_sheet
        st.subheader('Quarterly Cashflow')
        stock.quarterly_cashflow
        st.subheader('Quarterly Earnings')
        stock.quarterly_earnings
    else:
        st.subheader('Financial Report')
        stock.financials
        st.subheader('Balance Sheet')
        stock.balance_sheet
        st.subheader('Cashflow')
        stock.cashflow
        st.subheader('Earnings')
        stock.earnings
else:
    
    if(ticker=='TSLA'):
        #yfinance 
        tesla=yf.Ticker('TSLA')
        tesla_data=tesla.history(period='max')
        tesla_data.reset_index(inplace=True)
        #webscraping
        url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
        html_data  = requests.get(url).text
        soup = BeautifulSoup(html_data, 'html5lib')
        tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])
        
        for row in soup.find("tbody").find_all('tr'):
            col = row.find_all("td")
            date = col[0].text
            revenue = col[1].text
            tesla_revenue = tesla_revenue.append({"Date":date, "Revenue":revenue}, ignore_index=True) 
            tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")
            tesla_revenue.dropna(inplace=True)
            tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
        make_graph(tesla_data, tesla_revenue, 'Tesla')
    else:
        gme=yf.Ticker('GME')
        gme_data=gme.history(period='max')
        gme_data.reset_index(inplace=True)
        
        url = " https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
        html_data= requests.get(url).text
        soup = BeautifulSoup(html_data, 'html5lib')
        gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])
        
        for row in soup.find("tbody").find_all('tr'):
            col = row.find_all("td")
            date = col[0].text
            revenue = col[1].text
            gme_revenue = gme_revenue.append({"Date":date, "Revenue":revenue}, ignore_index=True)  
            # Remove Comma and dollar sign  from the Revenue column
            gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"")
            # Remove an null or empty strings in the Revenue column
            gme_revenue.dropna(inplace=True)
            gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]
        make_graph(gme_data, gme_revenue, 'GameStop')
        
    
        
