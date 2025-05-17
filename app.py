from dotenv import load_dotenv
load_dotenv()  # Load environment variables

import streamlit as st
import os
import pandas as pd
from src.database import initialize_database, execute_query, get_sample_data
from src.chatbot import generate_response
from src.utils import format_query_results

# Initialize Streamlit app
st.set_page_config(
    page_title="SQL Query Generator Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("SQL Query Generator Chatbot")
st.markdown("""
This chatbot helps you generate SQL queries from natural language questions.
The database contains information about customers, products, orders, and order items.
""")

# Check for API key
if not os.getenv("GOOGLE_API_KEY"):
    st.error("Please set your GOOGLE_API_KEY in the .env file")
    st.stop()

# Initialize session state for chat history and database
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize database
if "engine" not in st.session_state:
    try:
        st.session_state.engine = initialize_database()
        # Get and display sample data
        sample_data = get_sample_data(st.session_state.engine)
        
        st.success("Database initialized successfully!")
        
        # Display sample data in tables
        st.subheader("Sample Data")
        for table_name, data in sample_data.items():
            with st.expander(f"📊 {table_name.upper()} Table"):
                df = pd.DataFrame(data['rows'], columns=data['columns'])
                st.dataframe(df, use_container_width=True)
                
    except Exception as e:
        st.error(f"Error initializing database: {str(e)}")
        st.stop()

# Display database schema
with st.expander("Database Schema"):
    st.markdown("""
    The database has the following tables:
    - customers(customer_id, name, email)
    - products(product_id, name, price)
    - orders(order_id, customer_id, order_date)
    - order_items(item_id, order_id, product_id, quantity)
    """)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about the database"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Generate response
        response = generate_response(prompt)
        
        if response.startswith("Error"):
            st.error(response)
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Error: {response}"
            })
        else:
            # Check if the response is a SQL query by looking for SQL keywords
            is_sql_query = any(keyword in response.upper() for keyword in ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP', 'ALTER'])

            with st.chat_message("assistant"):
                if is_sql_query:
                    # Execute the SQL query
                    results = execute_query(st.session_state.engine, response)
                    formatted_results = format_query_results(results)

                    st.markdown("Generated SQL Query:")
                    st.code(response, language="sql")
                    st.markdown("Query Results:")
                    if isinstance(formatted_results, list):
                        df = pd.DataFrame(formatted_results)
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.write(formatted_results)

                    # Add assistant response to chat history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": f"Generated SQL Query:\n```sql\n{response}\n```\n\nQuery Results:\n{formatted_results}"
                    })
                else:
                    # Display conversational response
                    st.markdown(response)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response
                    })
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Error: {str(e)}"
        }) 