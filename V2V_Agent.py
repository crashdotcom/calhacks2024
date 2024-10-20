# fetch.ai agent to take a transcript from vapi, process it, and turn it into a json for a vapi post request

# actually: what this process is I think...is I will try to do the uh. call insurance stuff bc it's lowk just copying that guy's code

from uagents import Agent, Context, Bureau
from uagents.experimental.dialogues import Dialogue, Edge, Node

agent = Agent(name="V2V", seed="calhaxV2V", endpoint="http://localhost:8001/submit")


##########################
# Initializing our nodes #
##########################

default_state = Node(
    name="default_state",
    description=(
        "This is the default state of the dialogue. Every session starts in "
        "this state and is automatically updated once the dialogue starts."
    )
)

init_state = Node(
    name="init_state",
    description=(
        "This is where Vapi greets the service provider and informs them"
        "of our request."
    )
)

info_state = Node(
    name="info_state",
    description=(
        "This is the looping state in which Vapi may provide information"
        "to the hospital if they need our information."
    )
)

insist_state = Node(
    name="insist_state",
    description=(
        "This is the looping state where, if the hospital refuses for"
        "some reason to give a bill, we insist and continue to ask."
    )
)

gathering_state = Node(
    name="gathering_state",
    description=(
        "This is where, regardless of the previous outcome, we ask for"
        "the information of the person who helped us for our records."
    )
)

end_state = Node(
    name="end_state",
    description=(
        "The ending stage, after which we end the call."
    )
)

##########################
# Initializing our edges #
##########################

start_interaction = Edge(
    name = "start_interaction",
    description = "Transition from saying hi to request",
    parent = None,
    child = init_state
)


request_success = Edge(
    name = "request_success",
    description = "Successful asking for bill",
    parent = init_state,
    child = info_state
)

request_fail = Edge(
    name = "request_fail",
    description = "Failed asking for bill",
    parent = init_state,
    child = insist_state
)

info_gathering = Edge(
    name = "info_gathering",
    description = "Looping giving info to provider",
    parent = info_state,
    child = info_state
)

insist = Edge(
    name = "insist",
    description = "Looping insisting for info",
    parent = insist_state,
    child = insist_state
)

doc_from_info = Edge(
    name = "doc_from_info",
    description = "Going from info to documentation",
    parent = info_gathering,
    child = gathering_state
)

doc_from_insist = Edge(
    name = "doc_from_insist",
    description = "Going from insist to documentation",
    parent = insist_state,
    child = gathering_state
)

conclusion = Edge(
    name = "conclusion",
    description = "Going from documentation to conclusion",
    parent = gathering_state,
    child = end_state
)

class VapiDialogue(Dialogue):
    def __init__(
        self,
        version: str | None = None,
        agent_address: str | None = None
    ) -> None:
        super().__init__(
            name=VapiDialogue,
            version=version,
            agent_address=agent_address,
            nodes=[
                default_state,
                init_state,
                info_state,
                insist_state,
                gathering_state,
                end_state
            ],
            edges=[
                start_interaction,
                request_success,
                request_fail,
                info_gathering,
                insist,
                doc_from_info,
                doc_from_insist,
                conclusion
            ]
        )