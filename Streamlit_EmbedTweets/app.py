import streamlit as st
import streamlit.components.v1 as components
import requests

def theTweet(tweet_url):
    api = "https://publish.twitter.com/oembed?url={}".format(tweet_url)
    response = requests.get(api)
    res = response.json()["html"]
    return res

input = st.text_input("Enter your tweet url")
if input:
    res = theTweet(input)
    st.write(res)
    components.html(res,height= 700)
