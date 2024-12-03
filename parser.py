import feedparser
import datetime
import os
import json

feed_list = ["https://minwoo-it-factory.tistory.com/?minwoo"]

markdown_text = """
<div align="center">
  
<img src="https://render.gitanimals.org/lines/klmhyeonwoo?pet-id=590059497944971134" width="1000" height="240"/>

</div>

## klm min woo

<span style="color:#4E5968; font-size:10px;">

### 최근 포스팅
"""

lst = []
parsing_data = {}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR += "/data"
print(BASE_DIR)
uniqueKey = 0

for BLOG_URL in feed_list:
    if (BLOG_URL.find("velog.io") != -1):
        feed = feedparser.parse(BLOG_URL.split("?")[0])
    elif (BLOG_URL.find("medium") != -1):
        feed = feedparser.parse(BLOG_URL.split("?")[0]+"/feed")
    else:
        feed = feedparser.parse(BLOG_URL.split("?")[0]+"/rss")
      
    writer = BLOG_URL.split("?")[1]
    for i in feed['entries']:
        # print(i)
        if (BLOG_URL.find("velog.io") != -1 or BLOG_URL.find("medium") != -1):
          parsing_data["feed-" + str(uniqueKey)] = { 
              "title" : i['title'],
              "link" : i['link'],
              "date" : datetime.datetime.strptime(i['published'], '%a, %d %b %Y %H:%M:%S %Z').strftime("%b %d, %Y"),
              "writer" : writer,
          }
        else:
            parsing_data["feed-" + str(uniqueKey)] = { 
              "title" : i['title'],
              "link" : i['link'],
              "date" : datetime.datetime.strptime(i['published'], "%a, %d %b %Y %H:%M:%S %z").strftime("%b %d, %Y"),
              "writer" : writer,
            }
        print("-", i['link'], i['title'])
        uniqueKey += 1

parsing_data = dict(sorted(parsing_data.items(), key=lambda item: datetime.datetime.strptime(item[1]['date'], '%b %d, %Y'), reverse=True))

feed = feedparser.parse(feed_list[0].split("?")[0]+"/rss")
for i in feed['entries']:
    # print(i)
    markdown_text += f"- [{i['title']}]({i['link']})<br>\n"
  
with open(os.path.join(BASE_DIR, 'feed.json'), 'w+',encoding='utf-8') as json_file:
    json.dump(parsing_data, json_file, ensure_ascii = False, indent='\t')

print(parsing_data)

f = open("README.md", mode="w", encoding="utf-8")
f.write(markdown_text)
f.close()
print("성공")
