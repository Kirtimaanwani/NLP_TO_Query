# SQL Query Generator Chatbot

A Streamlit-based chatbot that uses Google's Gemini AI to generate SQL queries from natural language questions.

## Features

- Natural language to SQL query conversion
- Interactive chat interface
- Real-time query execution
- In-memory SQLite database with sample data
- Query results formatting

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd sql_chatbot
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided URL (usually http://localhost:8501)

3. Start asking questions about the database, for example:
- "Show me all customers and their orders"
- "What is the total value of orders for each customer?"
- "List all products ordered by Alice"

## Project Structure

```
sql_chatbot/
│
├── .env
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
│   ├── database.py
│   ├── chatbot.py
│   └── utils.py
└── app.py
```

## Database Schema

The application uses an in-memory SQLite database with the following schema:

- customers(customer_id, name, email)
- products(product_id, name, price)
- orders(order_id, customer_id, order_date)
- order_items(item_id, order_id, product_id, quantity)

## Dependencies

- streamlit==1.31.1
- google-generativeai==0.3.2
- sqlalchemy==2.0.27
- python-dotenv==1.0.1 