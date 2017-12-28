import tweepy
import requests
import json
import random
import os

#Booty Eats v.0.0.5

#Authorization Happens Here
def init_twitter():
    auth = tweepy.OAuthHandler(os.environ["CONSUMER_KEY"], os.environ["CONSUMER_KEY_SECRET"])
    auth.set_access_token(os.environ["ACCESS_TOKEN"], os.environ["ACCESS_TOKEN_SECRET"])
    api = tweepy.API(auth)
    return api


#Functions here
def get_recipes(ingredient):
    f2f = os.environ["F2F_API"]
    r = requests.get("http://food2fork.com/api/search?key=%s&q=%s" % (f2f, ingredient))
    output = None
    limit = 0
    if r.status_code == 200:
        print "Success"
        result = r.json()
        output = result["recipes"]
        limit = len(output)
    else:
        return "ERROR"
        exit()
    return output[random.randrange(0, limit)]

def get_recipe_name(recipes):
    title = recipes["title"]
    return title

def get_recipe_link(recipes):
    link = recipes["source_url"]
    return link

def get_image(recipes):
    image_url = recipes["image_url"]
    return image_url

def construct_tweet(food):
    slug = get_recipes(food)
    title = get_recipe_name(slug)
    link = get_recipe_link(slug)
    image = get_image(slug)

    output = "Eat the booty like %s" % (title)
    if len(output) < 200:
        output += "\n%s" % (link)
        return send_tweet(output, image)
    else:
       return construct_tweet(food)
      

def send_tweet(message, imageURL):
    api = init_twitter()
    request = requests.get(imageURL, stream=True)
    filename = "temp.jpg"
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)        
        api.update_with_media(filename, message)
        os.remove(filename)
    else:
        print("Error, No Image")
        api.update_status(message)

print construct_tweet("New Years")
