# Written By James Mok on 5 October 2022
# Lastest Edit By James Mok on 9 November 2022

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
    async def on_connect(self): print("~Twitter Stream Connected~")

    # Error Handling
    async def on_errors(self, errors):
        print("on_error")
        print(errors)

    async def on_connection_error(self):
        print("on_connection_error")

    async def on_exception(self, exception):
        print("on_exception")
        print(exception)

    async def on_request_error(self, status_code):
        print("on_request_error")
        print(status_code)

    # Confirmation The Twitter Stream Is Disconnected
    async def on_disconnect(self): print("~Twitter Stream Disconnected~")

    # Everytime A Tweet Is Posted And Is In The Stream Rules, Call This
    async def on_includes(self, includes):
        if 'media' in includes.keys(): media = includes['media'][0]['url']
        else: media = None
        tweet = includes['tweets'][0]

        print(tweet.author_id, "---", tweet.text)
        await output(tweet, media)


if __name__ == '__main__':
    load_dotenv()   # Get .env File For Hidden Variables
    twitterBearer = os.getenv("TWITTER_BEARER") # Not API Secret Key
    discordToken = os.getenv("DISCORD_TOKEN")
    discordServer = os.getenv("DISCORD_SERVER") # Discord Server Name
    discordChannel = int(os.getenv("DISCORD_CHANNEL")) # Discord Channel ID
    discordRole = os.getenv("DISCORD_ROLE") # Discord Server Role String

    discordClient = discord.Client(intents=discord.Intents().default())    # Create Discord Client Object
    twitterClient = tweepy.Client(twitterBearer) # Create Twitter Client Object

    stream = TweetStream(bearer_token=twitterBearer)  # Create The Twitter Stream

    # Follow The Desired Twitter Users
    for user in users:
        rule = "from:" + user  # Specific Twitter API Syntax (See Twitter Documentation)
        stream.add_rules(tweepy.StreamRule(rule))
    print(stream.get_rules())


    # Post "SHEEEEESH" In The Specified Channel
    async def awake():
        channel = discordClient.get_channel(discordChannel)  # Get The Channel To Send Embeds to

        # Create Embed For Discord To Use
        embedVar = discord.Embed(title="SHEEEEESH", description="You have opened Pendora's Bot", color=0x95C8D8)
        embedVar.set_thumbnail(url="https://konachan.com/sample/33d33cf341d50e7ae2deff8701b376f7/Konachan.com%20-%20330306%20sample.jpg")

        await channel.send(embed=embedVar)


    # Send The Given Tweet To The Specified Channel
    async def output(tweet, media):
        server = discord.utils.get(discordClient.guilds, name=discordServer)  # Get The Current Server ID
        channel = discordClient.get_channel(discordChannel)  # Get The Channel To Send Embeds to
        role = discord.utils.get(server.roles, name=discordRole) # Get The Role To Mention
        print(role)
        print(discordRole)

        # Get User Info
        user = twitterClient.get_user(id=tweet.author_id, user_fields=["name", "profile_image_url"])

        # Get The Tweet's URL And Ping Weewas Tag
        tweetURL = "https://twitter.com/" + user.data["username"] + "/status/" + str(tweet.id)

        # Create Embed For Discord To Use
        embedVar = discord.Embed(title="", description=tweet.text, color=0x95C8D8)
        embedVar.set_author(name=user.data["name"] + " | @" + user.data["username"],
                            icon_url=user.data["profile_image_url"])

        # If There Is An Image, Add It To The Embed
        if media: embedVar.set_image(url=media)

        # Get The Time The Tweet Was Posted
        time = tweet.created_at.now()
        formatTime = str(time.day) + "/" + str(time.month) + "/" + str(time.year) + " at " + str(time.hour) + ":" + str(
            time.minute)
        embedVar.set_footer(text="Twitter • " + formatTime)

        # Ping Role And Send The Embed To The Channel
        await channel.send(content=role.mention + " " + tweetURL, embed=embedVar)


    # When The Discord Bot Starts, Create A Twitter Stream (Which Handles The Posting)
    @discordClient.event
    async def on_ready():
        server = discord.utils.get(discordClient.guilds, name=discordServer)  # Get The Current Server ID
        print(discordClient.user, ' Is Ready! Server is: ', server.id)      # Print To Console The Text Channel The Bot Will Use

        await awake()    # Let The Server Know The Bot Is Up

        # This Is The Actual Run Of The Twitter Stream
        stream.filter(expansions=["attachments.media_keys", "referenced_tweets.id"], # Allows For Images/Videos, Retweets, Replies
                      media_fields=["media_key", "type", "preview_image_url", "url"], # URL To The Media In The Tweet
                      tweet_fields=["author_id", "created_at"] # Adds The Author ID And Date Created To Tweet Objects
                      )

    # Report When The Bot Goes Down
    @discordClient.event
    async def on_disconnect():
        print(discordClient.user, " Has Disconnected!")
        stream.disconnect()


    discordClient.run(discordToken) # Start The Discord Bot