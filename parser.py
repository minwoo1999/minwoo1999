import feedparser
import datetime
import os
import json

feed_list = ["https://minwoo-it-factory.tistory.com?minwoo"]

markdown_text = """
<div align="center">
  
<a href="https://github.com/devxb/gitanimals">
<img
  src="https://render.gitanimals.org/farms/minwoo1999"
  width="600"
  height="300"
/>
</a>
</div>



## klm min woo

<span style="color:#4E5968; font-size:10px;">

### Contribution - yorkie
- Add project API key rotation to enhance security (https://github.com/yorkie-team/yorkie/pull/1296)

### Contribution - Spring boot
- Add Date and UUID deserialization support in nullSafeValue method (https://github.com/spring-projects/spring-boot/issues/42972)

- Add test for nullSafeValue with mapper transformation (https://github.com/spring-projects/spring-boot/pull/43441)

### Contribution - Spring Data Jpa
- Refactor: Remove unused query parameter in getCountQuery method(https://github.com/spring-projects/spring-data-jpa/pull/3719)

### Contribution - Redis lettuce

- replace hardcoded GT and LT with CommandKeyword enum (https://github.com/redis/lettuce/pull/3079)

- docs: update Limitations section to reflect shaded JAR deprecation (https://github.com/redis/lettuce/pull/3095)

### 최근 포스팅
<span style="color:#4E5968; font-size:10px;">

"""

lst = []
parsing_data = {}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR += "/data"
print(BASE_DIR)
uniqueKey = 0

for BLOG_URL in feed_list:
    if BLOG_URL.find("velog.io") != -1:
        feed = feedparser.parse(BLOG_URL.split("?")[0])
    elif BLOG_URL.find("medium") != -1:
        feed = feedparser.parse(BLOG_URL.split("?")[0] + "/feed")
    else:
        feed = feedparser.parse(BLOG_URL.split("?")[0] + "/rss")
      
    writer = BLOG_URL.split("?")[1]
    for i in feed['entries']:
        if BLOG_URL.find("velog.io") != -1 or BLOG_URL.find("medium") != -1:
            parsing_data["feed-" + str(uniqueKey)] = { 
                "title": i['title'],
                "link": i['link'],
                "date": datetime.datetime.strptime(i['published'], '%a, %d %b %Y %H:%M:%S %Z').strftime("%b %d, %Y"),
                "writer": writer,
            }
        else:
            parsing_data["feed-" + str(uniqueKey)] = { 
                "title": i['title'],
                "link": i['link'],
                "date": datetime.datetime.strptime(i['published'], "%a, %d %b %Y %H:%M:%S %z").strftime("%b %d, %Y"),
                "writer": writer,
            }
        uniqueKey += 1

parsing_data = dict(sorted(parsing_data.items(), key=lambda item: datetime.datetime.strptime(item[1]['date'], '%b %d, %Y'), reverse=True))

# 최근 포스팅 4개 가져오기
recent_posts = list(parsing_data.values())[:6]

for post in recent_posts:
    markdown_text += f"- [{post['title']}]({post['link']})<br>\n"

# 추가 내용
markdown_text += """

### INTRODUCE
<span style="color:#4E5968; font-size:10px;">

  
- I majored in software engineering.
- I am interested in and studying backend development.
- I have a focus on learning Spring Framework, DevOps, CI/CD, and AWS-based infrastructure.

### Currently studying 
<span style="color:#4E5968; font-size:10px;">

* aws

* mysql
 
* advanced java

### CONTACT
- Email: hmg5959@gmail.com


<br><br>
[![Solved.ac Profile](http://mazassumnida.wtf/api/v2/generate_badge?boj=kbsserver)](https://solved.ac/kbsserver/)
</div>
"""

# JSON 저장
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

with open(os.path.join(BASE_DIR, 'feed.json'), 'w+', encoding='utf-8') as json_file:
    json.dump(parsing_data, json_file, ensure_ascii=False, indent='\t')

print(parsing_data)

# README.md 저장
f = open("README.md", mode="w", encoding="utf-8")
f.write(markdown_text)
f.close()
print("성공")
