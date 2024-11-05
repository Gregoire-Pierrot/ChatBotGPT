import os

from langchain_fireworks import ChatFireworks
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, trim_messages


##############################################################
                        # Model #
##############################################################


#langchain api key : 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
#fireworks api key : fw_3Zdp27tVsoJ5B13uME2UDCWw

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["FIREWORKS_API_KEY"] = "fw_3Zdp27tVsoJ5B13uME2UDCWw"



####################################################
# Define the model
#####################################################

model = ChatFireworks(model="accounts/fireworks/models/llama-v3p1-70b-instruct")

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are the robot of a chatbot. You must answer conciently. Answer all questions to the best of your ability in {language}.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

trimmer = trim_messages(
    max_tokens=65,
    strategy="last",
    token_counter=model,
    include_system=True,
    allow_partial=False,
    start_on="human",
)

messages = [
    SystemMessage(content="you're a good assistant")
]

####################################################