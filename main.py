# Written By James Mok on 5 October 2022

# Get tweets from @EliraPendora id=1390620618001838086 and @3W1W4 id=1507066475638673422 and send them through discord

# Used In Twitter Stream Connection
import asyncio
import tweepy
import tweepy.asynchronous as asynchronous

# Used In Discord API Connection
import discord

# Used In .env Variable Collection
import os
from dotenv import load_dotenv

users = ['EliraPendora', '3W1W4']

# Twitter Streaming Class
# Takes In The Twitter Bearer Token (str), Returns Stream Connection To Twitter
# Overloads Base AsyncStreamingClient Class
class TweetStream(asynchronous.AsyncStreamingClient):
    # First Message Displayed When Twitter Stream Connects Successfully
    async def on_connect(self): print("~Connected~")


    # Everytime A Tweet Is Posted And Is In The Stream Rules, Call This
    async def on_tweet(self, tweet):
        print(tweet.author_id, "---", tweet.text)
        print(tweet.data)
        await output(tweet)


if __name__ == '__main__':
    load_dotenv()   # Get .env File For Hidden Variables
    twitterBearer = os.getenv("TWITTER_BEARER") # Not API Secret Key
    discordToken = os.getenv("DISCORD_TOKEN")
    discordServer = os.getenv("DISCORD_SERVER") # Discord Server Name
    discordChannel = int(os.getenv("DISCORD_CHANNEL")) # Discord Channel ID

    discordClient = discord.Client(intents=discord.Intents().default())    # Create Discord Client Object
    twitterClient = tweepy.Client(twitterBearer) # Create Twitter Client Object


    # Post "SHEEEEESH" In The Specified Channel
    async def awake():
        channel = discordClient.get_channel(discordChannel)

        # Create Embed For Discord To Use
        embedVar = discord.Embed(title="SHEEEEESH", description="You have opened Pendora's Bot", color=0x95C8D8)
        embedVar.set_thumbnail(url="https://konachan.com/sample/33d33cf341d50e7ae2deff8701b376f7/Konachan.com%20-%20330306%20sample.jpg")

        await channel.send(embed=embedVar)


    # Send The Given Tweet To The Specified Channel
    async def output(tweet):
        channel = discordClient.get_channel(discordChannel)

        # Get User Info
        user = twitterClient.get_user(id=tweet.author_id, user_fields=["name", "profile_image_url"])
        print("User Data:")
        print(user.data)

        # Get The Tweet's URL
        tweetURL = "https://twitter.com/" + user.data["username"] + "/status/" + str(tweet.id) + " @everyone"

        # Create Embed For Discord To Use
        embedVar = discord.Embed(title="", description=tweet.text, color=0x95C8D8)
        embedVar.set_author(name=user.data["name"] + " | @" + user.data["username"], icon_url=user.data["profile_image_url"])

        time = tweet.created_at.now()
        formatTime = str(time.day) + "/" + str(time.month) + "/" + str(time.year) + " at " + str(time.hour) + ":" + str(time.minute)
        embedVar.set_footer(text="Twitter • " + formatTime)


        # embedVar.set_thumbnail(url=user.data["profile_image_url"]) •
        # embedVar.add_field(name="Link", value=tweetURL, inline=False)
        #TODO set_author

        await channel.send(content=tweetURL, embed=embedVar)


    # When The Discord Bot Starts, Create A Twitter Stream (Which Handles The Posting)
    @discordClient.event
    async def on_ready():
        server = discord.utils.get(discordClient.guilds, name=discordServer)   # Get The Current Server ID
        print(discordClient.user, ' Is Ready! ', server.id)      # Print To Console The Text Channel The Bot Will Use

        await awake()    # Let The Server Know The Bot Is Up

        stream = TweetStream(bearer_token=twitterBearer)    # Create The Twitter Stream

        # Follow The Desired Twitter Users
        for user in users:
            rule = "from:" + user       # Specific Twitter API Syntax (See Twitter Documentation)
            await stream.add_rules(tweepy.StreamRule(rule))
        print(await stream.get_rules())
        stream.filter(tweet_fields=["author_id", "created_at"])         # This Is The Actual Run Of The Stream, Adds "author_id" To Tweets



    discordClient.run(discordToken) # Start The Discord Bot