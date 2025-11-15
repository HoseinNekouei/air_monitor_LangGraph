from langgraph.graph import StateGraph, END
from state import State
from nodes import (
    fetch_data_node, 
    validate_node, 
    advice_node,
    logger_node
    )


# Build Graph
graph = StateGraph(State)

graph.add_node('fetch',fetch_data_node)
graph.add_node('validate', validate_node)
graph.add_node('advice', advice_node)
graph.add_node('logger', logger_node)   

# Flow:
# fetch -> validate -> advice -> log -> END
graph.add_edge('fetch', 'validate')
graph.add_edge('validate', 'advice')
graph.add_edge('advice', 'logger')
graph.add_edge('logger', END)

# set entry point
graph.set_entry_point('fetch')

app= graph.compile()


