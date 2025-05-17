import os
import google.generativeai as genai
import re

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
CHAT_MODEL = "gemma-3-27b-it"

def clean_sql_response(response):
    """Clean up the SQL response by removing markdown formatting and extra whitespace."""
    # Remove markdown code blocks
    response = re.sub(r'```sql\s*', '', response)
    response = re.sub(r'```\s*', '', response)
    
    # Remove any leading/trailing whitespace
    response = response.strip()
    
    return response

def generate_response(question):
    """Generate response based on the question type using Gemini AI."""
    # First, determine if the question is database-related
    classification_prompt = f"""
You are a helpful database assistant. Analyze if the following question is related to querying the database:

Question: {question}

Database Schema:
- customers(customer_id, name, email)
- products(product_id, name, price)
- orders(order_id, customer_id, order_date)
- order_items(item_id, order_id, product_id, quantity)

Respond with ONLY 'YES' if the question is about querying this database, or 'NO' if it's a general conversation or unrelated to the database.
"""

    try:
        model = genai.GenerativeModel(CHAT_MODEL)
        classification = model.generate_content(classification_prompt)
        is_db_question = classification.text.strip().upper() == 'YES'

        if not is_db_question:
            # Handle conversational questions about the database
            prompt = f"""
You are a helpful database assistant chatbot. The user has asked: {question}

Please provide a friendly response that:
1. Acknowledges their question
2. Guides them to ask about the database
3. Mentions what kind of information they can query (customers, products, orders, order items)
4. Provides 1-2 example questions they can ask

Keep your response focused on the database context and be helpful but concise.
"""
        else:
            # Handle database-related questions
            prompt = f"""
You are a helpful assistant that converts user questions into SQL.

Database Schema:
- customers(customer_id, name, email)
- products(product_id, name, price)
- orders(order_id, customer_id, order_date)
- order_items(item_id, order_id, product_id, quantity)

Now, write a SQL query for this question:
{question}

IMPORTANT: Return ONLY the SQL query without any markdown formatting (no ```sql or ```), no explanations, and no additional text.
The response should be a clean SQL query that can be executed directly.
"""

        response = model.generate_content(prompt)
        
        if is_db_question:
            return clean_sql_response(response.text)
        else:
            return response.text.strip()
    except Exception as e:
        return f"Error generating response: {str(e)}" 