import os
import requests 
from dotenv import load_dotenv

#Loading the environment variables
load_dotenv()

#Setting up OPENAI Api key 
API_KEY = os.getenv("OPENAI_API_KEY")
API_URL = "https://api.openai.com/v1/chat/completions"

def generate_ideas(query):
  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
  }
  
  data = {
    "model":"gpt-4o-mini",
    "store": True,
    "message" :[
      {"role":"system", "content": "You are a helpful assistent that generates unique app ideas with priority "},
      {"role":"user", "content": f"Generate 3 unique app ideas based on this {query}. for each idea, provide a priority score (1-5, with 1 being the highest priority) based on relevance, potential impact and feasibility. Also, provode a brief explanation for the priority score"}
      
      ]
  }
  response = requests.post(API_URL, headers=headers, json=data) 
  #error handling if request fails, a exception is raised 
  response.raise_for_status()
  
  #Process the response, convert into JSON object and cleaning up
  
  ideas = response.json()['choices'][0]['message']['content'].strip().split('\n\n')
  return [idea.strip() for idea in ideas if idea.strip()]


  #For Expanding the idea even further 
  
  def expand_ideas(unique_idea):
    
    headers = {
      "Content-Type" : "application/json",
      "Authorization": f"Bearer {API_KEY}"
    }
    
    data = {
      "model" :"gpt-4o-mini",
      "store":True,
      "messages": [
        {"role": "system", "content": "You are a helpful assistant that provides detailed suggestions for app ideas."},
        {"role": "user", "content": f"Provode a detailed suggestion for this app idea:{unique_idea}"}
      ]
    }
    response = requests.post(API_URL, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["chocies"][0]["message"]['content'].strip()
  
def parse_idea(idea_text):
  #Split input text in lines
  lines =idea_text.split('\n')
  
  #Extracting specific text individually 
  idea = lines[0].split(":", 1)[1]
  priorty = int(lines[1].split(': ')[1].split('/')[0])
  explanation = lines[2].split(': ',1)[1]
  return {'idea':idea, 'priorty':priorty, 'Explanation':explanation}
  
  
  
  
  