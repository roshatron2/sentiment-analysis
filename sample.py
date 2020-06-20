import csv
import json
import requests

# fetched_tweets_filename = "tweets.csv"
# field = [1, "a", "e", "b", 1]

# with open(fetched_tweets_filename, "a") as csvfile:
#     csvwriter = csv.writer(csvfile, delimiter=",", quotechar="'", quoting=csv.QUOTE_ALL)
#     csvwriter.writerow(["twitter_id", "text", "location", "place", "sentiment"])
#     csvwriter.writerow(field)

response = requests.get("https://jsonplaceholder.typicode.com/todos")
todos = json.loads(response.text)
print(todos[0]["title"])
