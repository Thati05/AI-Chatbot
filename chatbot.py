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

def generate_ideas(query):
    chat_session = model.start_chat(history=history)
    response = chat_session.send_message(query)
    model_response = response.text
    ideas = [
        idea.split(":", 1)[0].strip() + ":" + idea.split(":", 1)[1].strip().split("\n", 1)[0]
        for idea in model_response.strip().split("\n") if ":" in idea
    ]
    return [idea for idea in ideas if idea.strip()]

def expand_ideas(unique_idea):
    chat_session = model.start_chat(history=history)
    response = chat_session.send_message(f"Expand on the idea: {unique_idea}")
    return response.text.strip()

def mock_evaluate_idea(idea):
    """ Mock AI evaluation returning random scores for demonstration purposes. """
    relevance = random.randint(1, 5)
    impact = random.randint(1, 5)
    feasibility = random.randint(1, 5)
    priority_score = (relevance + impact + feasibility) / 3
    return {
        "idea": idea,
        "relevance": relevance,
        "impact": impact,
        "feasibility": feasibility,
        "priority_score": round(priority_score, 2)
    }

def rank_ideas(ideas):
    ranked_ideas = [mock_evaluate_idea(idea) for idea in ideas]
    ranked_ideas.sort(key=lambda x: x["priority_score"])
    return ranked_ideas

def main():
    query = "What new app should I build?"
    print(f"Query: {query}")

    ideas = generate_ideas(query)
    ranked_ideas = rank_ideas(ideas)

    print("\nRanked Ideas with Priority Scores:")
    for i, ranked_idea in enumerate(ranked_ideas, 1):
        print(f"{i}. {ranked_idea['idea']} - Priority Score: {ranked_idea['priority_score']} (Relevance: {ranked_idea['relevance']}, Impact: {ranked_idea['impact']}, Feasibility: {ranked_idea['feasibility']})")

    while True:
        selection = input("\nSelect two ideas by typing their numbers (e.g., 1, 3): ")
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
