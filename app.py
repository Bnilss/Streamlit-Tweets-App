import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt

TITLE = "Sentiment Analysis of US airline Tweets"
DESCRIPTION = 'This App is a Streamlite app used to analyse the sentiments of tweets from US Airline ✈️'
DATA_URL = "/home/rhyme/Desktop/Project/Tweets.csv"

# Add a title and a description
st.title(TITLE)
st.sidebar.title(TITLE)

st.markdown(DESCRIPTION)
st.sidebar.markdown(DESCRIPTION)

# Load data and saving it as cache to avoid loading it evrey time we click something
@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()

# Add Random Tweets selected and allowing the user to select em by sentiment
st.sidebar.subheader("Show a Random Tweet")
random_tweet = st.sidebar.radio('Sentiment',('positive','neutral','negative'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[['text']].sample(n=1).iat[0,0])

# Add Plots and dropdown list of plots options
st.sidebar.markdown('### Number of Tweets by sentiments')
select = st.sidebar.selectbox('Visualization type',['Histogram','Pie Chart'],key=1)

sentiments_count = data['airline_sentiment'].value_counts()
sentiments_count = pd.DataFrame({'Sentiment':sentiments_count.index,
                'Tweets':sentiments_count.values})

if not st.sidebar.checkbox('Hide',True):
    st.markdown("### Number of Tweets by sentiments")
    if select == 'Histogram':
        fig = px.bar(sentiments_count, x="Sentiment",y="Tweets",color="Tweets",
            height = 500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiments_count, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)

st.sidebar.subheader('When and where users are tweeting from?')
hour = st.sidebar.slider("Hour of day",0,23)
modified_data = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox("Close",True, key=1):
    st.markdown("### Tweets Location by the hour of day")
    st.markdown(f'{len(modified_data)} tweets between {hour}:00 and {(hour+1)%24}:00')
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)

st.sidebar.subheader("Breaking down ariline tweets by sentiments")
choice = st.sidebar.multiselect("Pick Airlines",('US Airways','United','American',
        'Southwest','Delta','Virgin America'), key='0')

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x='airline',y='airline_sentiment', histfunc='count',
            color='airline_sentiment', facet_col='airline_sentiment', labels={'airline_sentiment':'tweets'},
            height=600, width=800)
    st.plotly_chart(fig_choice)

st.sidebar.subheader("Word Cloud")
word_sent = st.sidebar.radio('Display word cloud for what sentiment', ('positive','negative','neutral'))
if not st.sidebar.checkbox("Close", True,key='3'):
    st.header(f'Word Cloud for {word_sent.upper()} sentiment')
    df = data[data['airline_sentiment'] == word_sent]['text'].tolist()
    process_words = ' '.join([word for word in df if 'http' not in word
                        and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white',
            height=640, width=800).generate(process_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()
