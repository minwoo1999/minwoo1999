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


<div align="center">

# 👨‍💻 Minwoo Kim | Software Engineer

A software engineer who enjoys collaboration and embraces new challenges.  
I strive to deeply understand both technology and product context to build meaningful services.

</div>

---

## 🧑‍💼 Org / Career

- **(Apr 2023 – Nov 2023)** Trainee, **SW Maestro 14th**
- **(Apr 2023 – Nov 2024)** Member, **LikeLion (멋쟁이사자처럼)**
- **(Apr 2024 – Jun 2024)** Backend Intern, **Mobile App Development Cooperative**
- **(Jan 2025 – Jun 2025)** Java Developer, **Seculayer Inc.**
- **(May 2024 – Oct 2025)** Member, **YAPP Tech Community**

---

## 📜 Certificates & Tests

- **(Apr 2025)** AWS Certified Solutions Architect – Associate – *Amazon Web Services* – ✅ Pass  
- **(Apr 2025)** Engineer Information Processing – *QNet (HRDK)* – ✅ Pass  
- **(Mar 2023)** SQL Developer (SQLD) – *KData* – ✅ Pass  
- **(Nov 2022)** Network Administrator Level 2 – *ICQA* – ✅ Pass  
- **(Mar 2022)** Computer Specialist in Spreadsheet & Database Level 2 – ✅ Pass  

---

## 🔒 Private (Toy) Projects

- **TeamPlanner** *(Apr 2023 – Nov 2023)*  
  → *Spring Boot, MySQL, Layered Architecture, React*

- **FlowBit** *(May 2024 – Dec 2024)*  
  → *Spring Boot, Microservices Architecture, MongoDB, MySQL, Docker*

---

## 🏅 Awards & Contributions

- 🥇 **K-PaaS Cloud Platform Contest** – Korea Cloud Association President’s Award *(2024)*  
- 🏆 **Kangnam University Academic Festival** – 1st Place *(2023)*  
- 🚀 **Wanted Pre-Onboarding Backend Challenge** – *(2024)*

### 🔧 Open Source Contributions

- [`yorkie`](https://github.com/yorkie-team/yorkie/pull/1296) – Add project API key rotation for enhanced security  
- [`spring-boot`](https://github.com/spring-projects/spring-boot/issues/42972) – Add Date/UUID deserialization to `nullSafeValue`  
- [`spring-boot`](https://github.com/spring-projects/spring-boot/pull/43441) – Add test for mapper transformation with `nullSafeValue`  
- [`spring-data-jpa`](https://github.com/spring-projects/spring-data-jpa/pull/3719) – Refactor: remove unused query parameter in `getCountQuery`  
- [`redis/lettuce`](https://github.com/redis/lettuce/pull/3079) – Replace hardcoded `GT`/`LT` with `CommandKeyword` enum  
- [`redis/lettuce`](https://github.com/redis/lettuce/pull/3095) – Update documentation for shaded JAR deprecation

---




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
