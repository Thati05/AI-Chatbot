import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setting up OpenAI API key
API_KEY = os.getenv("OPENAI_API_KEY")
API_URL = "https://api.openai.com/v1/chat/completions"

def generate_ideas(query):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "model": "gpt-4o-mini",
        "store": True,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that generates unique app ideas with priority rankings."},
            {"role": "user", "content": f"Generate 3 unique app ideas based on this query: {query}. For each idea, provide a priority score (1-5, with 1 being the highest priority) based on relevance, potential impact, and feasibility. Also, provide a brief explanation for the priority score."}
        ]
    }
    response = requests.post(API_URL, headers=headers, json=data)
    response.raise_for_status()

    # Process the response, convert into JSON object, and clean up
    ideas = response.json()['choices'][0]['message']['content'].strip().split('\n\n')
    return [idea.strip() for idea in ideas if idea.strip()]

def expand_ideas(unique_idea):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "model": "gpt-4o-mini",
        "store": True,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that provides detailed suggestions for app ideas."},
            {"role": "user", "content": f"Provide a detailed suggestion for this app idea: {unique_idea}"}
        ]
    }
    response = requests.post(API_URL, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]['content'].strip()

def parse_idea(idea_text):
    # Split input text into lines
    lines = idea_text.split('\n')

    # Extracting specific text individually
    idea = lines[0].split(": ", 1)[1]
    priority = int(lines[1].split(': ')[1].split('/')[0])
    explanation = lines[2].split(': ', 1)[1]
    return {'idea': idea, 'priority': priority, 'explanation': explanation}

def main():
    query = "What new app should I build?"
    print(f"Query: {query}")

    ideas_text = generate_ideas(query)
    ideas = [parse_idea(idea_text) for idea_text in ideas_text]

    print("\nGenerated Ideas (sorted by priority):")
    for i, idea in enumerate(sorted(ideas, key=lambda x: x['priority']), 1):
        print(f"{i}. (Priority: {idea['priority']}/5) {idea['idea']}")

    while True:
        action = input("\nEnter 'select' to choose ideas or 'explain' to get a priority explanation: ").lower()
        if action == 'select':
            selection = input("Please choose two ideas by typing their numbers (e.g., 1, 3): ")
            try:
                selected_indices = [int(x.strip()) for x in selection.split(',')]
                if len(selected_indices) == 2 and all(1 <= i <= len(ideas) for i in selected_indices):
                    break
                else:
                    print("Please select exactly two valid ideas.")
            except ValueError:
                print("Invalid input. Please enter two numbers separated by a comma.")
        elif action == 'explain':
            idea_num = input("Enter the number of the idea you want explained: ")
            try:
                idea_index = int(idea_num) - 1
                if 0 <= idea_index < len(ideas):
                    print(f"\nPriority Explanation for '{ideas[idea_index]['idea']}':")
                    print(ideas[idea_index]['explanation'])
                else:
                    print("Invalid idea number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        else:
            print("Invalid action. Please enter 'select' or 'explain'.")

    print("\nDetailed suggestions for selected ideas:")
    for index in selected_indices:
        idea = ideas[index - 1]['idea']
        suggestion = expand_ideas(idea)
        print(f"\nIdea: {idea}")
        print(f"Suggestion: {suggestion}")

if __name__ == "__main__":
    main()
