from langgraph.graph import StateGraph, END
from state import SensorState
from nodes import (
    fetch_data_node, 
    validate_node, 
    analyze_node,
    logger_node
    )


# Build Graph
graph = StateGraph(SensorState)

graph.add_node('fetch',fetch_data_node)
graph.add_node('validate', validate_node)
graph.add_node('analyze', analyze_node)
graph.add_node('logger', logger_node)   

# Flow:
# fetch -> validate -> analyze -> log -> END
graph.add_edge('fetch', 'validate')
graph.add_edge('validate', 'analyze')
graph.add_edge('validate', 'logger')
graph.add_edge('logger', END)

app= graph.compile()


