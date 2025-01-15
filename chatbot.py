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

def expand_ideas(unique_idea):
    chat_session = model.start_chat(history=history)
    response = chat_session.send_message(f"Expand on the idea: {unique_idea}")
    return response.text.strip()

def evaluate_relevance(idea, query):
    """ Simulate AI evaluation for relevance using keyword matching for simplicity. """
    return random.randint(1, 5)  # Replace with actual AI relevance evaluation

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
    print("Hello :) How can I assist you?")
    
    query = input("You: ")

    ideas = generate_ideas(query)
    ranked_ideas = rank_ideas(ideas)

    print("\nRanked Ideas with Priority Scores:")
    for ranked_idea in ranked_ideas:
        print(f"{ranked_idea['idea']} - Priority Score: {ranked_idea['priority_score']} (Relevance: {ranked_idea['relevance']}, Impact: {ranked_idea['impact']}, Feasibility: {ranked_idea['feasibility']})\n")

    while True:
        selection = input("\nSelect two ideas by typing their numbers for further explanation (e.g., 1, 3): ")
        try:
            selected_indices = [int(x.strip()) for x in selection.split(',')]
            if len(selected_indices) == 2 and all(1 <= i <= len(ranked_ideas) for i in selected_indices):
                break
            else:
                print("Please select exactly two valid ideas.")
        except ValueError:
            print("Invalid input. Please enter two numbers separated by a comma.")

    print("\nDetailed suggestions for selected ideas:")
    for index in selected_indices:
        idea = ranked_ideas[index - 1]['idea']
        suggestion = expand_ideas(idea)
        print(f"\nIdea: {idea}")
        print(f"Suggestion: {suggestion}")

if __name__ == "__main__":
    main()
