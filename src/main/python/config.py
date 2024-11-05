from state import State
from model import prompt, model, trimmer, messages

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph


##############################################################
                        # Configuration #
##############################################################



####################################################
# Define the function that calls the model
####################################################

def call_model(state: State):
    chain = prompt | model
    trimmed_messages = trimmer.invoke(state["messages"])
    response = chain.invoke(
        {"messages": trimmed_messages, "language": state["language"]}
    )
    return {"messages": [response]}


####################################################
# Define the function to send a message to the model
####################################################

def sendMessage(message, language, config):
    input_messages = messages + [HumanMessage(message)]
    #for chunk, metadata in app.stream({"messages": input_messages, "language": language}, config, stream_mode="messages"):
    #    if isinstance(chunk, AIMessage):  # Filter to just model responses
    #        print(chunk.content, end="|")
    
    output = app.invoke({"messages": input_messages, "language": language}, config)
    output["messages"][-1].pretty_print()  # output contains all messages in state
    return output["messages"][-1].content


####################################################
# Define some variables
####################################################

# Define a new graph
workflow = StateGraph(state_schema=State)

# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Add memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# per user
config = {"configurable": {"thread_id": "abc123"}}

####################################################