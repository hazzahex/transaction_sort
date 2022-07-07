import json
import os

import pandas as pd  # to perform data manipulation and analysis
import numpy as np  # to cleanse data
from datetime import datetime  # to manipulate dates
import plotly.express as px  # to create interactive charts
import plotly.graph_objects as go  # to create interactive charts
from jupyter_dash import JupyterDash  # to build Dash apps from Jupyter environments
from dash import dcc  # to get components for interactive user interfaces
from dash import html

dateparse = lambda x: datetime.strptime(x, '%d/%m/%Y')

df = pd.read_csv('./data/transactions.csv', encoding_errors='ignore', parse_dates=['Date'], date_parser=dateparse)
df = df.drop(['Number', 'Account'], axis=1)


# amexdf = pd.read_csv('data/amex/activity.csv')


def collate_transactions():
    global df
    for filename in os.listdir('data/lloyds'):
        f = os.path.join('data/lloyds', filename)
        print(f"Add {f}")
        dflloyds = pd.read_csv(f, encoding_errors='ignore',
                               parse_dates=['Date'], date_parser=dateparse)
        dflloyds.rename(columns={"Description": "Memo"}, inplace=True)
        dflloyds.drop(['Date entered', 'Reference', 'Unnamed: 5'], inplace=True, axis=1)
        print(dflloyds.shape)
        df = pd.concat([df, dflloyds], axis=0, ignore_index=True)
    for filename in os.listdir('data/amex'):
        f = os.path.join('data/amex', filename)
        print(f"Add {f}")
        dfamex = pd.read_csv(f, encoding_errors='ignore',
                             parse_dates=['Date'], date_parser=dateparse)
        dfamex.rename(columns={"Description": "Memo"}, inplace=True)
        print(dfamex.shape)
        df = pd.concat([df, dfamex], axis=0, ignore_index=True)


collate_transactions()

print(df)

titles = ["Mortgage", "Income", 'Car', 'Parking', 'Phone', 'Credit card', 'Pay Pal', 'Milk',
          'Eating out', 'Leisure', 'Travel', 'House expense', 'Subscriptions', 'Monzo', 'Transport', 'Transfer',
          'Work snack', 'Camera', 'Parents', 'Cash', 'Supermarket', 'Coffee', 'Books', 'Elise', 'Fuel', 'Sport']
df['Subcategory'] = np.where(df['Memo'].str.contains('BGC'), 'Transfer', df['Subcategory'])
df['Subcategory'] = np.where(
    df['Memo'].str.contains(
        'BG SERVICES|BRITISH GAS|TV LICENCE|BRISTOLWESSEXWATER|BRISTOL CC L TAX|BT CONSUMER|BG CONSUMER'), 'Transport',
    df['Subcategory'])
df['Subcategory'] = np.where(df['Memo'].str.contains('SKIPTON'), 'Mortgage', df['Subcategory'])
df['Subcategory'] = np.where(df['Memo'].str.contains('DYSON TECHNOLOGY L'), 'Income', df['Subcategory'])
df['Subcategory'] = np.where(df['Memo'].str.contains('VWFS|AUDI ASALES|Hand Car Wash|HALFORDS|ADMIRAL'), 'Car',
                             df['Subcategory'])
df['Subcategory'] = np.where(df['Memo'].str.contains('SERVICE ST|DELAMERE|STN|STATION|FILLING|SERVICE STA|Shell|SHELL|ASDA FILLING'),
                             'Fuel', df['Subcategory'])
df['Subcategory'] = np.where(df['Memo'].str.contains('BRISTOL CITY COUNC|JUSTPARK|CAR PARK|PARKING'), 'Parking',
                             df['Subcategory'])
df['Subcategory'] = np.where(df['Memo'].str.contains('H3G|KLARNA|Tech Pack Fee'), 'Phone', df['Subcategory'])
df['Subcategory'] = np.where(df['Memo'].str.contains(
    'AMERICAN EXPRESS|LLOYDS STANDARD|AMERICANEXPRESS|AMERICAN EXP|AMERICANEXP|PAYMENT RECEIVED'), 'Credit card',
                             df['Subcategory'])
df['Subcategory'] = np.where(df['Memo'].str.contains('PAYPAL'), 'Pay Pal', df['Subcategory'])
df['Subcategory'] = np.where(df['Memo'].str.contains('MILK AND'), 'Milk', df['Subcategory'])
df['Subcategory'] = np.where(
    df['Memo'].str.contains(
        'QUEENS HEAD|SEAMUS|Crown|INN|HATCHET|TAPROOM|TAP ROOM|LOUNGE|WILD BEER|PITCHER|SLUG AND LETTUCE|FIVE GUYS|BURGER KING|KFC|NANDOS|LEFT HANDED|WOKYKO|SMALL BAR|BOCABAR|GBK|HONEST BURGERS|THE PONY BISTRO|Rolling Ita|PIZZA WORKSHOP|THERIVERSIDEINN|THE SPOTTED COW|PRET A MANGER|THE HORSE GUARDS INN|URBAN MASALA|PONY|KING STREET|EATCHU|GREGGS|COMMERCIAL ROOMS|BEER EMPORIUM|BURGER|MCDONALD'),
    'Eating out', df['Subcategory'])
df['Subcategory'] = np.where(df['Memo'].str.contains('SHOWCASE'), 'Leisure', df['Subcategory'])
df['Subcategory'] = np.where(df['Memo'].str.contains(
    'AIRBNB|UBER|AIRPORT|Air|TFL|GWR|RAILW|BELGIUM|easyjet|FIRST WEST OF|thetrainline|THAMESLINK|EASYJET|NON-STERLING|EUROSTAR|Stockel|STIB|STOCKEL|easyJet|RENTALCAR'),
                             'Travel', df['Subcategory'])
df['Subcategory'] = np.where(df['Memo'].str.contains('Eden Hardwood|TIMPSON|RIVERSIDE GARDEN|B & Q|IKEA'),
                             'House expense', df['Subcategory'])
df['Subcategory'] = np.where(df['Memo'].str.contains('NETFLIX|APPLE|SPOTIFY'), 'Subscriptions', df['Subcategory'])
df['Subcategory'] = np.where(df['Memo'].str.contains('Monzo|MONZO'), 'Monzo', df['Subcategory'])
df['Subcategory'] = np.where(df['Memo'].str.contains('DYSON LTD|WCVS'), 'Work snack', df['Subcategory'])
df['Subcategory'] = np.where(df['Memo'].str.contains('EVERSURE'), 'Camera', df['Subcategory'])
df['Subcategory'] = np.where(df['Memo'].str.contains('HEXTALL W'), 'Parents', df['Subcategory'])
df['Subcategory'] = np.where(df['Memo'].str.contains(
    'M&S|SAINSBURY|TESCO|CO|SOUTHVILLE DELI|ALDI|Zero Green|WH SMITH|WAITROSE|MARKS BREAD|ASHTON FRUIT SHOP|PARSONS|RARE|SPENCER|ASDA|BOOTS|FIVE ACRE FARM|MOIST'),
                             'Supermarket', df['Subcategory'])
df['Subcategory'] = np.where(df['Memo'].str.contains('COSTA|CAFFE NERO|STARBUCK|SOCIETY|Little Victori|CAFE'), 'Coffee',
                             df['Subcategory'])
df['Subcategory'] = np.where(df['Memo'].str.contains('STORYSMITH|WATERSTONES'), 'Books', df['Subcategory'])
df['Subcategory'] = np.where(df['Memo'].str.contains('LEBEAUX|ELISE'), 'Elise', df['Subcategory'])
df['Subcategory'] = np.where(df['Memo'].str.contains('GOLF|OAKSEY'), 'Sport', df['Subcategory'])
# df['Subcategory'] = np.where(df['Subcategory'].str.contains('CASH'), 'Cash', df['Subcategory'])
df.loc[~df["Subcategory"].isin(titles), "Subcategory"] = "Other"

df['year_month'] = df['Date'].dt.strftime('%Y-%m')


def build_charts():
    Net_Worth_Table = df.groupby('year_month')['Amount'].sum().reset_index(name='sum')
    Net_Worth_Table['cumulative sum'] = Net_Worth_Table['sum'].cumsum()

    Net_Worth_Chart = go.Figure(
        data=go.Scatter(x=Net_Worth_Table["year_month"], y=Net_Worth_Table["cumulative sum"]),
        layout=go.Layout(
            title=go.layout.Title(text="Net Worth Over Time")
        )
    )
    Net_Worth_Chart.update_layout(
        xaxis_title="Date",
        yaxis_title="Net Worth (£)",
        hovermode='x unified'
    )
    Net_Worth_Chart.update_xaxes(
        tickangle=45)
    Net_Worth_Chart.show()

    # df = df[df['Subcategory'] != "Income"]
    df.amount = df['Amount'] * (-1)
    Total_Monthly_Expenses_Table = df.groupby('year_month')['Amount'].sum().reset_index(name='sum')
    Total_Monthly_Expenses_Table = Total_Monthly_Expenses_Table.rename(
        columns={'year_month': 'DATE', 'sum': 'TOTAL EXPENSE'})

    Total_Monthly_Expenses_Chart = px.bar(Total_Monthly_Expenses_Table, x="DATE", y="TOTAL EXPENSE",
                                          title="Total Monthly Expenses")
    Total_Monthly_Expenses_Chart.update_yaxes(title='Expenses (£)', visible=True, showticklabels=True)
    Total_Monthly_Expenses_Chart.update_xaxes(title='Date', visible=True, showticklabels=True)

    Total_Monthly_Expenses_Chart.show()

    Expenses_Breakdown_Table = pd.pivot_table(df, values=['Amount'], index=['Subcategory', 'Date'],
                                              aggfunc=sum).reset_index()
    Expenses_Breakdown_Table.columns = [x.upper() for x in Expenses_Breakdown_Table.columns]
    Expenses_Breakdown_Table = Expenses_Breakdown_Table.rename(columns={'Date': 'DATE'})
    Expenses_Breakdown_Table = Expenses_Breakdown_Table[['DATE', 'SUBCATEGORY', 'AMOUNT']]
    # Creation of a df with all dates within the range we have data for each category /
    # (e.g. for cash withdrawal there are no transactions between MArch 2020 and August 2020 /
    # so there is not data point in the graph for those dates and I have to fix that)

    Expenses_Breakdown_Table_All_Dates = Expenses_Breakdown_Table.set_index(
        ['DATE', 'SUBCATEGORY']
    ).unstack(
        fill_value=0
    ).asfreq(
        'M', fill_value=0
    ).stack().sort_index(level=1).reset_index()

    Expenses_Breakdown_Table_All_Dates['DATE'] = pd.to_datetime(Expenses_Breakdown_Table_All_Dates['DATE'])
    Expenses_Breakdown_Table_All_Dates['DATE'] = Expenses_Breakdown_Table_All_Dates['DATE'].dt.strftime('%Y-%m')
    # Appending all dates to the original df

    Expenses_Breakdown_Table_Final = Expenses_Breakdown_Table.append(Expenses_Breakdown_Table_All_Dates,
                                                                     ignore_index=True)
    Expenses_Breakdown_Table_Final = Expenses_Breakdown_Table_Final.drop_duplicates(subset=['DATE', 'SUBCATEGORY'],
                                                                                    keep='first')
    Expenses_Breakdown_Table_Final = Expenses_Breakdown_Table_Final.sort_values(['DATE', 'SUBCATEGORY'],
                                                                                ascending=[True, False],
                                                                                ignore_index=True)
    # creating a df only for the latest date
    # I need it to add 0s in case in the latest date there was no transaction for a specific category
    # otherwise again the data point for the latest date will not appear in the chart
    # (before I fixed only the dates within the date range of the transactions, not the latest date)

    latest_date = Expenses_Breakdown_Table_Final['DATE'].max()
    df_latest_date = Expenses_Breakdown_Table_Final.loc[Expenses_Breakdown_Table_Final['DATE'] == latest_date]
    missing_cat_latest_date = pd.DataFrame({'SUBCATEGORY': list(set(df_latest_date['SUBCATEGORY']) ^ set(titles))})
    missing_cat_latest_date['AMOUNT'] = 0.0
    missing_cat_latest_date['DATE'] = df_latest_date['DATE'].max()
    missing_cat_latest_date = missing_cat_latest_date[['DATE', 'SUBCATEGORY', 'AMOUNT']]

    # Appending the categories with no transactions for the latest date to the final df for this chart

    Expenses_Breakdown_Table_Final = Expenses_Breakdown_Table_Final.append(missing_cat_latest_date)
    Expenses_Breakdown_Chart = px.line(Expenses_Breakdown_Table_Final, x='DATE', y="AMOUNT", title="Expenses Breakdown",
                                       color='SUBCATEGORY')
    Expenses_Breakdown_Chart.update_yaxes(title='Expenses (£)', visible=True, showticklabels=True)
    Expenses_Breakdown_Chart.update_xaxes(title='Date', visible=True, showticklabels=True)

    Expenses_Breakdown_Chart.show()
    # Build App
    app = JupyterDash(__name__)

    app.layout = html.Div([

        html.Div([
            html.H1(str(latest_date) + " Personal Finance Summary", style={'text-align': 'center'}),
            dcc.Graph(figure=Net_Worth_Chart)
        ]),

        html.Div([
            dcc.Graph(figure=Total_Monthly_Expenses_Chart)
        ]),

        html.Div([
            dcc.Graph(figure=Expenses_Breakdown_Chart)

        ])
    ])

    # Run app and display result
    app.run_server(mode='external')

    # CLick on the link below to access the "Personal Finances Summary"


# df = df[~df['Subcategory'].isin(titles)]
df_size = df.shape

# build_charts()
bananas = 5
