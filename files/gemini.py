import google.generativeai as genai

genai.configure(api_key="AIzaSyC23d64rrwpOX_0OkXZrzCX145Yy3l6uao")

def analyze_articles_with_gemini(articles):


    generation_config = {
    "temperature": 0.8,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }


    model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    system_instruction = """
    You are an AI assistant tasked with analyzing a set of articles and extracting the most important insights. Your goal is to identify key points, trends, and actionable information from the articles. Follow these steps:

    1. **Read and Understand**: Carefully analyze each article to identify the main ideas, key facts, and any notable trends or patterns.
    2. **Extract Insights**: Focus on extracting insights such as:
    - Key statistics or data points.
    - Emerging trends or patterns.
    - Important opinions or arguments.
    - Actionable recommendations or conclusions.
    3. **Organize the Output**: Present the insights in a structured format:
    - Use bullet points for clarity.
    - Group related insights under relevant headings (e.g., 'Trends', 'Statistics', 'Recommendations').
    - Order the insights by importance, with the most critical points at the top.
    4. **Be Concise**: Keep the output concise and avoid unnecessary details.
    5. Make sure you only type your insights, do not say anything else.
    """)

    chat_session = model.start_chat(
    history=[
    ]
    )

    prompt = ''

    for article in articles:
                prompt += f"Title: {article['title']}\nSource: {article['source']}\n\n"

    response = chat_session.send_message(prompt)


    return response.text




def analyze_posts_with_ai( posts):


    generation_config = {
    "temperature": 0.8,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }


    model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    system_instruction = """
    You are an AI assistant tasked with analyzing a set of media posts and extracting the most important insights related to disasters. Your goal is to identify key points, trends, and actionable information from the posts. Follow these steps:

    1. **Read and Understand**: Carefully analyze each media post to identify the main ideas, key facts, and any notable trends or patterns related to disasters.
    2. **Extract Insights**: Focus on extracting insights such as:
    - Key details about the disaster (e.g., type, location, severity).
    - Emerging trends or patterns (e.g., frequency, impact, response efforts).
    - Important opinions, warnings, or calls to action from authorities or communities.
    - Actionable recommendations or conclusions (e.g., preparedness, relief efforts, mitigation strategies).
    3. **Organize the Output**: Present the insights in a structured format:
    - Use bullet points for clarity.
    - Group related insights under relevant headings (e.g., 'Disaster Details', 'Trends', 'Response Efforts', 'Recommendations').
    - Order the insights by importance, with the most critical points at the top.
    4. **Be Concise**: Keep the output concise and avoid unnecessary details.
    5. Make sure you only type your insights, do not say anything else.
    """)

    chat_session = model.start_chat(
    history=[
    ]
    )

    prompt = ''

    for post in posts:
        prompt += f"Title: {post['text']}\n\n"

    response = chat_session.send_message(prompt)


    return response.text