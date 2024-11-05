from typing import Sequence
from typing_extensions import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


##############################################################
                        # State #
##############################################################


class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    language: str


##############################################################