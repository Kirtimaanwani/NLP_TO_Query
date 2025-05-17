def format_query_results(results):
    """Format query results for display."""
    if isinstance(results, str) and results.startswith("Error"):
        return results
    
    if not results:
        return "No results found."
    
    # Convert results to a list of dictionaries
    formatted_results = []
    for row in results:
        formatted_results.append(dict(row._mapping))
    
    return formatted_results 