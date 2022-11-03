# Pendora's Bot
### Author: James Mok       
### Date Created: 5 October 2022

![Sheesh](https://i.ytimg.com/vi/FvShFQ-EhZI/hqdefault.jpg)
##### Sheeeeeeeeesh

Purpose: A Discord bot to keep up with all the latest tweets from @EliraPendora and @3W1W4. Perfect for those who don't check Twitter regularly.

Elira Pendora's Socials:
* [Youtube](https://www.youtube.com/channel/UCIeSUTOTkF9Hs7q3SGcO-Ow)
* [@EliraPendora](https://twitter.com/EliraPendora)
* [@3W1W4](https://twitter.com/3W1W4)

<!-- If you want to make it in C++, try using Discord++ (DiscordPP) and twitcurl (swatkat). Or don't, I didn't look too deep into these APIs-->
Using discord.py and tweepy

---

Now before you judge my code, consider the following:

* discord.py is only asynchronous to my knowledge, forcing the tweepy to be asynchronous.
* discord.py is event driven to my knowledge, meaning that in order for any code to be executed an event has to occur.
  * This means I can't just have the discord client fire off tweets by calling a function,
          the two APIs have to be coupled in on_ready.
* I like using classes, but the circular dependency of the code forces me to not use discord.py's classes.
* The tweepy overload functions reference things that happen after it because it can't have the function output(tweet)
    before it.
  * output(tweet) must be its own function to properly interact with the discord channels.
  * output(tweet) must be after the Twitter client object is called in order to gain access to client's functions.

* I hate using global variables because of my upbringing, but it is easier to edit users at the top instead of
  somewhere I can't see it.

Summary: Combining two APIs is really hard.

Future Improvements:
* Proper error checking
* Handle retweets, images, and videos