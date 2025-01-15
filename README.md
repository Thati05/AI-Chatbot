# Creative App Idea Generator

This project is an AI-driven application designed to generate and prioritize innovative app ideas based on user queries. By leveraging a generative AI model, users can input a general area of interest, and the application will return three unique app ideas, along with their relevance, impact, feasibility, and overall priority scores.

## Features

- **Generate App Ideas**: Receive three unique app ideas based on your query.
- **Rank Ideas**: Ideas are ranked by relevance, impact, and feasibility.
- **Expand Ideas**: Select two ideas to receive detailed expansions.
- **Priority Score Explanation**: Understand the scoring logic behind each idea's ranking.

## Setup Instructions

1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Create a `.env` file in the project root and add your API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
4. Run the application using:
   ```
   python chatbot.py
   ```

## Usage

1. Input a query to generate app ideas.
2. View the ranked list of ideas with their priority scores.
3. Choose two ideas for detailed expansion or request an explanation of the priority score for an idea.
4. Continue exploring or exit the application based on your preferences.

## Prioritization Logic

The prioritization of app ideas is based on a calculated **Priority Score**, which combines three key metrics:

1. **Relevance**: Simulated using random values to represent how well an idea matches the user's query.
2. **Impact**: Measured by the presence of keywords such as "innovative" or "disruptive," indicating the potential for significant market influence.
3. **Feasibility**: Evaluated by identifying practical terms like "scalable" or "implementable" to ensure the idea can be realistically developed.

Each metric is normalized to a 1-5 scale. The Priority Score is the average of the relevance, impact, and feasibility scores, providing a balanced view of an idea’s potential value.



