import requests

import plotly
import plotly.express as px

url = "https://api.github.com/search/repositories?q=language:python+sort:stars+stars:>10000"

headers = {"Accept": "application/vnd.github.v3+json"}
r = requests.get(url,headers=headers)
print(f"status code {r.status_code}")

response_dicts = r.json()
repo_dicts = response_dicts['items']    
repo_names,repo_links, stars, hover_texts = [], [], [], []

for repo_dict in repo_dicts:
    repo_name = (repo_dict['name'])
    repo_url = repo_dict['html_url']
    repo_link = f"<a href='{repo_url}'>{repo_name}</a>"

    owner = repo_dict['owner']['login']
    description = repo_dict['description']
    hover_text = f"{owner}<br /> {description}"

    repo_links.append(repo_link)    
    stars.append(repo_dict['stargazers_count'])
    repo_names.append(repo_name)
    hover_texts.append(hover_text)

title = "Most-Starred Python Projects on GitHub"
labels = {'x':'Repository','y':'Stars'}

fig = px.bar(x=repo_links,y=stars,title=title,labels=labels,
             hover_name=hover_texts)

fig.update_layout(title_font_size=28,xaxis_title_font_size=20,
                  yaxis_title_font_size=20)

fig.update_traces(marker_color='SteelBlue',marker_opacity=0.6)

plotly.offline.plot(fig)