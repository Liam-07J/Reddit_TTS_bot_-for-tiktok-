import requests as req
import bs4 as bs
from gtts import gTTS
from pytube import YouTube
import os
import random
import time
import re 
from playwright.sync_api import Page, expect
from selenium import webdriver

def findPost(subreddit):
    print("Now searching through the " + subreddit + " subreddit")
    url = 'https://www.reddit.com/r/' + subreddit + "/comments/"
    # check if subreddit exists
    if req.get(url).status_code == 404:
        print("subreddit not found")
        findPost(input("Enter a VALID subreddit: "))
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"}
    html_doc = req.get(url, headers=headers).text
    soup = bs.BeautifulSoup(html_doc, 'html.parser')

    # find "r/python/comments"
    i=0
    postsArray = []
    while i<len("reddit.txt"):
        link = (soup.find_all('a', class_='title')[i].get('href'))
        print(link)
        # if link includes "r/python/comments"
        if "comments" in link:
            postLinks = "https://reddit.com" + link
            postsArray.append(postLinks)
        i+=1
    # remove duplicates
    postsArray = list(dict.fromkeys(postsArray))
    return postsArray


def findComments(postLinks):
    print("finding comments from " + postLinks)
    # get text from post
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"}
    html_doc = req.get(postLinks, headers=headers).text
    soup = bs.BeautifulSoup(html_doc, 'html.parser')
    text  = str(soup.findAll('p'))
    if text == "":
        print("no post found")
        return 0 
    # edit text to remove html tags
    text = text.replace('</p>, <p class="_1qeIAgB0cPwnLhDF9XSiJM">', '\nComments: ')
    text = text.replace('<p class="_22W-auD0n8kTKDVe0vWuyK" id="IdCard--CurrentlyViewing--undefined--t5_2qjni">Online</p>]', '')    
    text = text.replace('</p>, <p class="_22W-auD0n8kTKDVe0vWuyK" id="IdCard--Subscribers--undefined--t5_2qjni">Members</p>, ', '')
    text = text.replace('<em class="_7s4syPYtk5hfUIjySXcRE">who/whom</em> ', '')
    text = text.replace('[<p class="_1qeIAgB0cPwnLhDF9XSiJM">', '')
    text = text.replace('<em class="_7s4syPYtk5hfUIjySXcRE">', '')
    text = text.replace('<a class="_3t5uN8xUmg0TOwRCOGQEcU"', '')
    print(text)
    # remove https://reddit.com/r/
    name = postLinks.replace('https://reddit.com/r/', '') + ".txt"
    name = name.replace('/', '_')
    print("saving to " + name)
    # write text to file
    with open(name, 'a', encoding="utf8") as f:
        f.write(text)
    


def txtToSpeech(name):
    name = name.replace('https://reddit.com/r/', '')
    name = name.replace('/', '_')
    # open file and save text
    with open(name + ".txt", 'r', encoding="utf8") as f:
        text = f.read()
    # convert text to speech
    print("TExt is " + text)
    text = str(text)
    tts = gTTS(text=text, lang='en')
    tts.save(name + ".mp3")
    print("text has been converted to speech")

def randomVideo(name):
    print("getting random video")
    name = name.replace('https://reddit.com/r/', '')
    name = name.replace('/', '_')
    # randomly selects an element from the array
    videoArray = ["mcvid.mp4","mcvid2.mp4", "mcvid3.mp4", "mcvid4.mp4"]         # ADD MORE VIDEOS HERE
    video = random.choice(videoArray)
    print("video selected: " + video)
    # open mcvid.mp4 and save to name.mp4
    with open(video, 'rb') as f:
        data = f.read()
    with open(name + ".mp4", 'wb') as f:
        f.write(data)
    print("video has been saved")

def savefile():
    print("We have now generated all of the text files and the audio files and found a video file now we have to chosse whether we went this data or not")
    # search through files and find only .txt
    files = os.listdir()
    txtFiles = []
    for file in files:
        if file.endswith(".txt"):
            txtFiles.append(file)
    print(txtFiles)
    for file in txtFiles:
        if file == "reddit.txt":
            print("reddit.txt has been found")
            return 0
        Filename = file.replace(".txt", "")
        print("files have been kept")
        # create a new folder and move the files to the new folder
        os.mkdir(Filename)
        # move files to new folder 
        os.rename(Filename + ".mp4", Filename+"/" + Filename + ".mp4")
        os.rename(Filename + ".mp3", Filename+"/" + Filename + ".mp3")
        os.rename(Filename + ".png", Filename+"/"  + Filename + ".png")
        os.rename(Filename + ".txt", Filename+"/"  + Filename + ".txt")


def screenshot(name):
    post = name
    name = name.replace('https://reddit.com/r/', '')
    name = name.replace('/', '_')
    driver = webdriver.Chrome('chromedriver.exe') 
    driver.get(post)
    driver.save_screenshot(name + ".png")
    print("screenshot saved")

def searchSubReddit(subreddit):
    redditPosts = findPost(subreddit)
    for post in redditPosts:
        if findComments(post):
            print("no post found")
        else:
            txtToSpeech(post)
            randomVideo(post)
            screenshot(post)

subReddits = input("Enter the subreddit you want to search: ")
searchSubReddit(subReddits)
savefile()
print("Now you can edit them up together for your video")