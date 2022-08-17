A bot that can be used to download all file for a reddit tiktok/youtube account automatic

To run the bot run main.py in the terminal (You may have to install some pip package)

Also add chromedriver.exe to the same directory as the bot  (https://chromedriver.chromium.org/downloads)
The bot will:
    Ask you for the subreddit you want to take from

    It will then download all the files from the subreddit, including a .txt copy of the text, a .mp4 copy of the video, and a .jpg copy of the post and randomly select a video to play

    After all files are downloaded, the bot will show you the files and ask if you want to save them, if not the bot will delete the files

To add more video files to the bot, just add them to the array of videos in "main.py" on line 82 and in the current directory 

Additionaly the text to speech feature can give back a 429 error if the bot is used too much, so you could change your i.p address to a different one using a vpn

Furture:
    Allow user to enter an array of subreddits to download from
    Fix bug on line 27 (not allowing site to be loaded)
    Automatically move all "saved" files to other folder named after the post and subreddit
    Make the screenshots higher quality