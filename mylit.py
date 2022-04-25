# This project uses plotly and streamlit to provide basic dashboard and downloadable Performances Visualizations
# Basic packages
from sys import _enablelegacywindowsfsencoding
import streamlit as st
import pandas as pd
import datetime
import yfinance as yf

#Packages for plotting
import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler
plt.style.use('seaborn-bright')
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sb 
import json

import warnings
warnings.filterwarnings("ignore")



st.title('Basic Stock Performance Dashboard')

# Organize side bar including chosing a stock the information Type ( Financial Summary, Visualization)

sp500 = pd.read_csv("SP500.csv")
symbols = sp500['Symbol'].sort_values().tolist()

#Required Ticker Inputs
ticker = st.text_input('Enter a SP500 Stock Ticker', 'TSLA' )
stock= yf.Ticker(ticker)

# Show info about the Ticker:
if(ticker in symbols ):
    'Stocks Issuer:' 
    st.success( stock.info['longName'] )
else:
    st.error('This Ticker ist not in SP500')

info=st.sidebar.radio('What do you want to know?',
                      ('Stock Information','Visualization')
                      )

# Get Financial Summary
if(info=='Stock Information'):
    info_or_finsum=st.selectbox('Choose Information Type', ('Basic Information','Financial Summary'))
    if(info_or_finsum=='Basic Information'):
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
        st.subheader('Fundamental Information')
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
        
    else:
     st.subheader('Financial Reports')
     what = st.selectbox(
     'Chose report type',
     ('Quarterly reports','Annual reports'))
    
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

    st.subheader("Visualization with different libraries")

    #Ploting methods:
    type_analyze= st.selectbox('Choose analyzing type', ('Individual', 'Compare'))
    
    if(type_analyze == 'Individual'):
        
        ind_vis_lib = st.selectbox('Choose a library to visualize',('Matplotlib', 'Seaborn', 'Plotly'))
        
        #Matplotlib 
        
        if (ind_vis_lib == 'Matplotlib'):
            
            #Visualize Stock Price
            
                
            start_date= st.text_input('Enter Starting date as YYYY-MM-DD', '2021-01-01')
            end_date= st.text_input('Enter Ending date as YYYY-MM-DD', '2022-01-01')
            itv =st.selectbox('Choose an Intervall:',('1d','5d','1w','1m','3m','1y','5y'))
            'Analyzing Period: ', start_date, '-', end_date
                
            df = stock.history(intervall= itv, start= start_date, end= end_date)
            df
                
            fig = plt.figure(figsize = (6,4), dpi=50)
            
            plt.plot(df.Open,color='r')
            plt.xlabel('Date')
            plt.title('Open Price')
            plt.legend(['Open Price ($)'])
                        
                
            
            fig1= plt.figure(figsize= (6,4), dpi=50)
        
            plt.plot(df.Close, color='b')
            plt.title('Close Price')
            plt.xlabel('Date')
            plt.legend(['Close Price ($)'])
                    
            st.subheader('Volume')         
            fig2= plt.figure(figsize= (12,5), dpi= 50)
            plt.plot(df.Volume, color='g')
            plt.xlabel('Date')
            plt.legend(['Volume'])
            st.pyplot(fig2)
                
            #Visualize Daily Price Changes
                
            datevals = pd.to_datetime(df.index[1:].values)
            oldvals = df.Close[:-1].values
            newvals = df.Close[1:].values

            percent_change = (newvals-oldvals)*100/oldvals 

            fig3=plt.figure(figsize= (6,4), dpi=50)
            plt.plot(datevals, percent_change)
            plt.title('Daily Change History:')
            plt.xlabel('Date')
            plt.ylabel('Daily Change (%)')
    
                
            fig4=plt.figure(figsize=(6,4), dpi=50)
            plt.hist(percent_change, bins=100, density=True, stacked=True)
            plt.title('Daily Change Histogram:')
            plt.xlabel('Daily Change (%)')
            plt.ylabel('Probability Density Function')
                
            #Layout
            st.subheader('Stock Price in Line Graph')
            container1 = st.container()
            col1, col2 = st.columns(2)
            with container1:
                with col1:
                    fig
                with col2:
                    fig1
            st.subheader('Daily Price Changes')
            'Daily Change Statistics:'
            st.table(pd.DataFrame(percent_change).describe())
            container2 = st.container()
            col3, col4 = st.columns(2)
            with container2:
                with col3:
                    fig3
                with col4:
                    fig4
        


                
                
                
                
                
                
                
                
                
                
            
                
                
                
            
                
                
                
                
        
    
    
    
