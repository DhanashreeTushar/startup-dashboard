import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(layout= 'wide',page_title= 'Startup Analysis')

df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'],errors = 'coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_overall_analysis():
    st.title("Overall Analysis")

    # total invested money
    total = round(df['amount'].sum())
    # maximum value infused in startup
    max_funding =df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    # avg ticket size
    avg_funding = round(df.groupby('startup')['amount'].sum().mean())
    # startup
    Startups = df['startup'].nunique()
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Total', str(total) + ' Cr')

    with col2:
        st.metric('Max', str(max_funding) + ' Cr')

    with col3:
        st.metric('AVG', str(avg_funding) + ' Cr')

    with col4:
        st.metric('Startups', str(Startups) + ' Cr')

    st.header('MoM Graph')

    selected_option = st.selectbox('Select Type',['Total','Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['month', 'year'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['month', 'year'])['amount'].count().reset_index()

    temp_df['x-axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x-axis'], temp_df['amount'])
    st.pyplot(fig3)


def load_startup_details(startup):
    st.title(startup)
    # Startups = df['startup'].nunique()
    invested_money = df[df['startup'].str.contains(startup)].groupby('startup')['amount'].sum().sort_values(ascending = False)
    st.subheader("Invested Money")
    st.dataframe(invested_money)

    # operating in city
    city = df[df['startup'].str.contains(startup)]
    sub_city = city[['startup', 'city']]
    st.subheader("City Operating In")
    st.dataframe(sub_city)

    # vertical wise investment
    vertical_invest = df[df['startup'].str.contains(startup)].groupby(['startup','vertical'])['amount'].sum().sort_values(ascending = False).head()

    st.subheader('Vertical Wise Investment')

    fig0, ax = plt.subplots()
    ax.pie(vertical_invest, labels = vertical_invest.index,autopct = "%0.01f%%")
    st.pyplot(fig0)
def load_investor_details(investor):
    st.title(investor)
    # recent 5 transactions
    last_5transact = df[df['investors'].str.contains(investor)].head()[
        ['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investment')
    st.dataframe(last_5transact)

    col1, col2 = st.columns(2)
    with col1:
        # biggest investement
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending = False).head()
        st.subheader('Biggest Investments')

        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)

    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sector Invested in')

        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels = vertical_series.index,autopct = "%0.01f%%")
        st.pyplot(fig1)


    col1,col2 = st.columns(2)
    with col1:
        round_df = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('Round Invested in')

        fig1, ax1 = plt.subplots()
        ax1.pie(round_df, labels=round_df.index, autopct="%0.01f%%")
        st.pyplot(fig1)

    with col2:
        city_df = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('City Invested in')

        fig1, ax1 = plt.subplots()
        ax1.pie(city_df, labels= city_df.index, autopct="%0.01f%%")
        st.pyplot(fig1)

    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('Year On Year Investment')

    fig1, ax1 = plt.subplots()
    ax1.plot(year_series.index,year_series.values)
    st.pyplot(fig1)


st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'Startup':
    selected_startup = st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    if btn1:
        load_startup_details(selected_startup)
else:
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)



