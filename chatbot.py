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
      {"role":"user", "content":"Generate 3 unique app ideas based on this {query}. for each idea, provide a priority score (1-5, with 1 being the highest priority) based on relevance, potential impact and feasibility. Also, provode a brief explanation for the priority score"}
      
      ]
  }
  response = requests.post(API_URL, headers=headers, json=data) 
  #error handling if request fails, a exception is raised 
  response.raise_for_status()
  
  #Process the response, convert into JSON object and cleaning up
  
  ideas = response.json()['choices'][0]['message']['content'].strip().split('\n\n')
  
  