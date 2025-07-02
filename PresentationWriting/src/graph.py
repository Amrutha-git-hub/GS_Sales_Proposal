from langgraph.graph import StateGraph,START,END
from .states import State
from .nodes import clean_data
from .sections import create_sections
from .proposal import write_sales_proposal


builder = StateGraph(State)
builder.add_node(create_sections)
builder.add_node(write_sales_proposal)
builder.add_node(clean_data)


builder.add_edge(START,'create_sections')
builder.add_edge('create_sections','write_sales_proposal')
builder.add_edge('write_sales_proposal','clean_data')
builder.add_edge('clean_data',END)


graph = builder.compile()
