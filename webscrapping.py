#Scrapping-project for GITHUB TOPICS
# Pick a website and describe your objective",
# - Browse through different sites and pick on to scrape. Check the Project Ideas section for inspiration.
# - Identify the information you'd like to scrape from the site. Decide the format of the output CSV file.
# - Summarize your project idea and outline your strategy in a Jupyter notebook.
# PROJECT OUTL
# We are going to scrape https://github.com/topics

# We'll get a list of topics. For each topic, we'll get topic title, topic page URL and topic description
# For each topic, we'll get the top 20 repositories in the topic from the topic page
# For each repository, we'll grab the repo name, username, stars and repo URL
# For each topic we'll create a CSV file in the following format
# Repo name,Username,Stars,Repo URL
# three.js,mrdoob,89200,https://github.com/mrdoob/three.js"
# Use the requests library to download web pages
# !pip install requests --upgrade --quiet

import requests
import io
import pandas as pd
import os

topics_url='https://github.com/topics'

response=requests.get(topics_url)

response.status_code

len(response.text)

response.text[:400]
page_content=response.text

page_content[:1000]

with io.open('webpage.html','w',encoding="utf-8") as f:
    f.write(page_content)
    # Use Beautiful Soup to parse and extract information
    #!pip install beautifulsoup4 --upgrade --quiet

from bs4 import BeautifulSoup

doc=BeautifulSoup(page_content,'html.parser')

len(doc.text)

type(doc)

topic_title_tags=doc.find_all('p',{'class':"f3 lh-condensed mb-0 mt-1 Link--primary"})

len(topic_title_tags)

topic_title_tags
topic_desc_tags=doc.find_all('p',{'class':"f5 color-fg-muted mb-0 mt-1"})

topic_desc_tags

topic_desc_tags

topic_title_link_tags=doc.find_all('a',{'class':"no-underline flex-1 d-flex flex-column"})

topic_title_link_tags
topic_title=[]
for tag in topic_title_tags:
   topic_title.append(tag.text)
topic_desc=[]
for tag in topic_desc_tags:
    topic_desc.append(tag.text.strip())
topic_link=[]
base_url="https://github.com"
for tag in topic_title_link_tags:
    topic_link.append(base_url+tag['href'])

topic_link
#!pip install pandas --quiet
### Displaying data in CSV file
topics_dict={'title':topic_title,
          'description': topic_desc,
         'url':topic_link }

topics_df=pd.DataFrame(topics_dict)

topics_df
topics_df.to_csv('topics.csv',index=None)
# Getting information out of a topic page¶
topic_page_url=topic_link[0]

topic_page_url

response=requests.get(topic_page_url)

response.status_code

len(response.text)

response.text
topic_doc=BeautifulSoup(response.text,'html.parser')

repo_tags=topic_doc.find_all('h3',{'class':'f3 color-fg-muted text-normal lh-condensed'})

len(repo_tags)

a_tags=repo_tags[0].find_all('a')

a_tags[0]


a_tags[0].text.strip()



a_tags[1]
a_tags[1].text.strip()
a_tags[1]['href']


base_url="https://github.com"
repo_url=base_url+a_tags[1]['href']
print(repo_url)

star_tags=topic_doc.find_all('span',{'id':'repo-stars-counter-star'})
len(star_tags)

star_tags[0].text.strip()
def parse_star_count(star_str):
    star_str=star_str.strip()
    if star_str[-1]=='k':
        return int(float(star_str[:-1])*1000)
    return int(star_str)

parse_star_count(star_tags[0].text.strip())

def get_repo_info(h3_tag,star_tag):
    a_tags=h3_tag.find_all('a')
    username=a_tags[0].text.strip()
    repo_name=a_tags[1].text.strip()
    repo_url=base_url+a_tags[1]['href']
    stars=parse_star_count(star_tag.text.strip())
    return username,repo_name,stars,repo_url
get_repo_info(repo_tags[0],star_tags[0])
topic_repos_dict={
    'username':[],
    'repo_name':[],
    'stars':[],
    'repo_url':[]
}
for i in range(len(repo_tags)):
    repo_info=get_repo_info(repo_tags[i],star_tags[i])
    topic_repos_dict['username'].append(repo_info[0])
    topic_repos_dict['repo_name'].append(repo_info[1])
    topic_repos_dict['stars'].append(repo_info[2])
    topic_repos_dict['repo_url'].append(repo_info[3])
topic_repos_dict['username']
trd=pd.DataFrame(topic_repos_dict)
trd
def get_topic_page(topic_url):
    response=requests.get(topic_url)
    if response.status_code!=200:
        raise Exception('Failed to load page {}'.format(topic_url))
    topic_doc=BeautifulSoup(response.text,'html.parser')
    return topic_doc

def get_repo_info(h3_tag,star_tag):
    a_tags=h3_tag.find_all('a')
    username=a_tags[0].text.strip()
    repo_name=a_tags[1].text.strip()
    repo_url=base_url+a_tags[1]['href']
    stars=parse_star_count(star_tag.text.strip())
    return username,repo_name,stars,repo_url
def get_topic_repos(topic_url):
    h3_selection_class='f3 color-fg-muted text-normal lh-condensed'
    repo_tags=topic_doc.find_all('h3',{'class':h3_selection_class})
    star_tags=topic_doc.find_all('span',{'id':'repo-stars-counter-star'})
    topic_repos_dict={
        'username':[],
        'repo_name':[],
        'stars':[],
        'repo_url':[]
    }
    for i in range(len(repo_tags)):
        repo_info=get_repo_info(repo_tags[i],star_tags[i])
        topic_repos_dict['username'].append(repo_info[0])
        topic_repos_dict['repo_name'].append(repo_info[1])
        topic_repos_dict['stars'].append(repo_info[2])
        topic_repos_dict['repo_url'].append(repo_info[3])
    return pd.DataFrame(topic_repos_dict) 

def scrape_topic(topic_url,path):
    if os.path.exists(path):
        print("The file {} already exists. Skipping......".format(path))
        return 
    topic_df=get_topic_repos(get_topic_page(topic_url))
    topic_df.to_csv(path+'.csv',index=None)
topic_link
Repo1=get_topic_repos(topic_link[1])
df1=pd.DataFrame(Repo1)
df1.to_csv('ajax.csv',index=None)
Repo4=get_topic_repos(topic_link[4])
df4=pd.DataFrame(Repo4)
df4
# Write a single funcion to:
# Get the list of topics from the topics page
# Get the list of top repos from the individual topic pages
# For each topic, create a CSV of the top repos for the topic
def get_topic_titles(doc):
    selection_class="f3 lh-condensed mb-0 mt-1 Link--primary"
    topic_title_tags=doc.find_all('p',{'class':selection_class})
    topic_titles=[]
    for tag in topic_title_tags:  
        topic_titles.append(tag.text)
    return topic_titles
        
    
def get_topic_descs(doc):
    topic_desc_tags=doc.find_all('p',{'class':"f5 color-fg-muted mb-0 mt-1"})
    topic_descs=[]
    for tag in topic_desc_tags:
            topic_descs.append(tag.text.strip())
    return topic_descs

def get_topic_urls(doc):
    topic_link_tags=doc.find_all('a',{'class':'no-underline flex-1 d-flex flex-column'})
    topic_urls=[]
    base_url='https://github.com'
    for tag in topic_link_tags:
        topic_urls.append(base_url+tag['href'])
    return topic_urls     
    
def scrape_topics():
    topics_url='https://github.com/topics'
    response=requests.get(topics_url)
    if response.status_code!=200:
        raise Exception('Failed to load page {}'.format(topic_url))
    topics_dict={
        'title':get_topic_titles(doc),
        'description':get_topic_descs(doc),
        'url':get_topic_urls(doc)
    }
    return pd.DataFrame(topics_dict)
scrape_topics()
def scrape_topics_repos():
    print('Scrapping list of topics')
    topics_df=scrape_topics()
    os.makedirs('data',exist_ok=True)
    for index,row in topics_df.iterrows():
        print('Scrapping top repositories for "{}" '.format(row['title']))
        scrape_topic(row['url'],'data/{}.csv'.format(row['title']))
for index,row in topics_df.iterrows():
    print(row['title'],row['description'])
scrape_topics_repos()




