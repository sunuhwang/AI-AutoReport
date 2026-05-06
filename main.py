"""
this is tool that ai search information and make markdown instead of me.
logic:
   1.user input topic.
   2.this code search about this topic.
   3.beautifulsoup find body or title.
   4.ai report information about body.ai summary body.
   5.if ai decide to search sub topic, then ai search about sub topic about super topic. else ai doesn't search about sub topic.
   6.repeat 2~5.
   7.make result to markdown.
"""
"""
how to use: python3 main.py {topic}
"""
import requests #that is library what get html.
from bs4 import BeautifulSoup #that is library what remove what isn't body in html.
from ddgs import DDGS #it searches about topic.
from openai import OpenAI #this is ai.
import sys
import json
#this is ai.
ai = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key=""
)
searched_thing:list[str] = []
def search(topic: str,root_topic:str, result: list[str],depth:int,searched_thing: list[str]) -> None:
    if depth > 3:
        return
    if topic in searched_thing:
        return
    #prompt what we'll use
    decide_to_keep_search_prompt =  f"""
            root: {root_topic}
            sub: {topic}
            result: {result}
            you are expert in '{root_topic}'.
            Is it 'sub({topic})' worth researching to understand 'root({root_topic})'?
            also, if you search about 'sub({topic})', do you think isn't it in 'result({result})'?
            also, isn't 'sub({topic})' is easy?
            answer in json format:
            {{
                "decision": true or false(if you think all my questions is true),
                "case_does_not_search": "(if decision is false, small information in your knowledge)"
            }}
    """
    #ask ai
    response = ai.chat.completions.create(
        model="llama3.1",
        messages=[{"role": "user", "content": decide_to_keep_search_prompt}],
        response_format={"type": "json_object"},
        temperature=0
    )
    #make response to json
    response_json = json.loads(response.choices[0].message.content)
    #if decision is false, don't search anymore
    if not response_json['decision']:
        result.append(response_json['case_does_not_search'])
        return
    else:
        #search information if decision is true
        with DDGS() as ddgs:
            print(f"🔍 [{depth}] search about '{topic}'")
            search_results = list(ddgs.text(f"{topic} in context of {root_topic}", max_results=3))
        for r in search_results:
            #pick real url
            url = r['href']
            #get body
            resp = requests.get(url,timeout=5)
            soup = BeautifulSoup(resp.text, 'html.parser')
            #delete css, js
            for s in soup(['script', 'style']): s.decompose()
            content = soup.get_text()
            #prompt for summary content
            report_prompt = f"""
    Root Topic: {root_topic}
    Current Topic: {topic}
    Content: {content}

    Task:
    1. Summarize the provided content focusing on its relationship with '{root_topic}'.
    2. Suggest exactly 2 'highly specific' sub-topics for further research.
    
    Constraint:
    - DO NOT repeat the words '{root_topic}' or '{topic}' in your suggested keywords.
    - Focus on technical components, specific APIs, or underlying mechanisms.
    - Output must be in valid JSON format.

    Output format:
    {{
        "summary": "your summary here",
        "keywords": ["specific_subtopic_1", "specific_subtopic_2"]
    }}
"""
            response = ai.chat.completions.create(
                model="llama3.1",
                messages=[{"role": "user", "content": report_prompt}],
                response_format={"type": "json_object"},
                temperature=0
            )
            response_json = json.loads(response.choices[0].message.content)
            #add a information in result
            result.append(response_json['summary'])
            for s in response_json["keywords"]:
                searched_thing.append(s)
                search(s, root_topic, result, depth + 1,searched_thing)
def make_markdown(information: list[str]) -> None:
    #make markdown file
    file = open("result.md", "w", encoding="utf-8")
    prompt = f"""
        write markdown document about {information}.
        you only need to tell me document's full content(string). 
    """
    response = ai.chat.completions.create(
        model="llama3.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    #write content
    file.write(response.choices[0].message.content)
    file.close()
topic = sys.argv[1]
result = []
search(topic, topic, result,0,searched_thing)
make_markdown(result)