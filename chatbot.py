import os
import random
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model with specified generation configuration
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

#In the model set the systems instructuion tha will guide the AI's behavior

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction="You are a helpful AI assistant specializing in generating innovative app ideas. You will receive a user query describing a general area of interest for an app. Your task is to generate three unique app ideas related to that query."
)

# Initialize conversation history
history = []

# Example keyword lists
impact_keywords = ["innovative", "disruptive", "growth"]
feasibility_keywords = ["practical", "implementable", "scalable"]



def generate_ideas(query):
    chat_session = model.start_chat(history=history)
    response = chat_session.send_message(query)
    model_response = response.text
    ideas = [idea.strip() for idea in model_response.split("\n") if idea.strip() and ":" in idea]
    return ideas
  
#Expanding on a specific idea usin the AI modela
def expand_ideas(unique_idea):
    chat_session = model.start_chat(history=history)
    response = chat_session.send_message(f"Expand on the idea: {unique_idea}")
    return response.text.strip()

def evaluate_relevance(idea, query):
    """ Simulate AI evaluation for relevance using keyword matching. """
    return random.randint(1, 5)  

def evaluate_idea(idea, query):
    relevance = evaluate_relevance(idea, query)
    impact = sum(1 for word in impact_keywords if word in idea.lower())
    feasibility = sum(1 for word in feasibility_keywords if word in idea.lower())
    
    # Normalize scores to fit into a 1-5 scale
    impact = min(max(impact, 1), 5)
    feasibility = min(max(feasibility, 1), 5)
    
    priority_score = (relevance + impact + feasibility) / 3
    return {
        "idea": idea,
        "relevance": relevance,
        "impact": impact,
        "feasibility": feasibility,
        "priority_score": round(priority_score, 2)
    }

def rank_ideas(ideas):
    return [evaluate_idea(idea, "") for idea in ideas]


def main():
    print("Welcome to the Creative App Idea Generator! 🎉\nHow can I assist you?")
    
    query = input("You: ")

    ideas = generate_ideas(query)
    ranked_ideas = rank_ideas(ideas)
    
    print("\n ✨ Here are ranked Ideas with Priority Scores:\n")
    for ranked_idea in ranked_ideas:
      print(f"{ranked_idea['idea']} - Priority Score: {ranked_idea['priority_score']} (Relevance: {ranked_idea['relevance']}, Impact: {ranked_idea['impact']}, Feasibility: {ranked_idea['feasibility']})\n")
      
      #User Interaction

    while True:
        action = input("\nWould you like to (1) Select an idea for expansion or (2) Request an explanation of the priority score? Type 1 or 2: ")
        if action == "1":
            selection = input("Select an idea by typing its number: ")
            try:
                index = int(selection.strip()) - 1
                if 0 <= index < len(ranked_ideas):
                    idea = ranked_ideas[index]['idea']
                    suggestion = expand_ideas(idea)
                    print(f"\n🎨 Expanded Idea: {idea}")
                    print(f"Suggestion: {suggestion}")
                    break
                else:
                    print("Please select a valid idea number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif action == "2":
            selection = input("Select an idea by typing its number to explain the priority score: ")
            try:
                index = int(selection.strip()) - 1
                if 0 <= index < len(ranked_ideas):
                    explanation = ranked_ideas[index]
                    print(f"\n📊 Idea: {explanation['idea']}")
                    print(f"Priority Score: {explanation['priority_score']}")
                    print(f"Relevance: {explanation['relevance']}, Impact: {explanation['impact']}, Feasibility: {explanation['feasibility']}")
                    break
                else:
                    print("Please select a valid idea number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        else:
            print("Invalid option. Please type 1 or 2.")

if __name__ == "__main__":
    main()
