# Creative App Idea Generator

This project is a Creative App Idea Generator that utilizes Google's Generative AI API to generate, rank, and expand on innovative app ideas based on user input. The system ranks the generated ideas based on their relevance, impact, and feasibility, providing priority scores to help users select the most promising ideas.

## Features

- **Generate App Ideas**: Users can input a query describing a general area of interest, and the AI will generate three unique app ideas related to that query.
- **Rank Ideas**: The generated ideas are evaluated and ranked based on relevance, impact, and feasibility, resulting in a priority score.
- **Expand Ideas**: Users can select two ideas to receive an expanded explanation and suggestions for each.
- **Priority Score Explanation**: Users can request an explanation of the priority score for a specific idea.

## Requirements

- Python 3.x
- `google-generativeai` package
- `python-dotenv` package
- An API key for Google's Generative AI service

## Setup

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```
2. Install the required packages:
    ```bash
    pip install google-generativeai python-dotenv
    ```
3. Set up your environment variables:
    - Create a `.env` file in the root directory.
    - Add your API key in the `.env` file:
    ```
    GEMINI_API_KEY=your_api_key_here
    ```
4. Run the application:
    ```bash
    python chatbot.py
    ```

## Usage

1. **Start the application**: Run `chatbot.py` to start the idea generator.
2. **Input a query**: Type in a general area of interest for an app, and the system will generate three related app ideas.
3. **View ranked ideas**: The system displays the ideas ranked by priority score along with relevance, impact, and feasibility scores.
4. **Select actions**:
    - **Expand Ideas**: Select two ideas for a detailed expansion by typing their numbers separated by commas (e.g., `1,2`).
    - **Priority Score Explanation**: Select an idea by typing its number to get a detailed explanation of its priority score.




