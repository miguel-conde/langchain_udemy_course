from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langchain_core.messages import SystemMessage
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.checkpoint.memory import MemorySaver
from typing import List, Callable, Dict


class LGBasicAgent():
    """
    A basic language chain agent that utilizes a language model and a set of tools to perform tasks.
    
    Methods:
        __init__(tools: List[Callable], llm=ChatOpenAI(model="gpt-4o"), sys_prompt: str = None)
        
        _assistant(state: MessagesState):
            Node function for the assistant that processes messages using the language model.
            
        invoke(state: MessagesState, config: Dict):
            Invokes the state graph with memory checkpointing to process the given state and configuration.
    """
    
    def __init__(self, tools: List[Callable], llm = ChatOpenAI(model="gpt-4o"), sys_prompt: str = None) -> None:
        """
        Initializes the basic language chain agent.
        
        Args:
            tools (List[Callable]): A list of callable tools that the agent can use.
            llm (ChatOpenAI, optional): The language model to be used. Defaults to ChatOpenAI(model="gpt-4o").
            sys_prompt (str, optional): The system prompt message. Defaults to None.
            
        Attributes:
            llm_with_tools (ChatOpenAI): The language model bound with the provided tools.
            tools (List[Callable]): The list of tools provided.
            sys_msg (SystemMessage): The system message for the assistant.
            builder (StateGraph): The state graph builder for managing control flow.
            memory (MemorySaver): The memory saver for checkpointing.
            react_graph_memory (StateGraph): The compiled state graph with memory checkpointing.
        """
        
        self.tools = tools
        self.llm_with_tools = llm.bind_tools(tools)
        
        # System message
        if sys_prompt is None:
            self.sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs.")
            
        self._build_graph()
        
    def set_tools(self, tools: List[Callable]) -> None:
        """
        Sets the tools for the agent.
        
        Args:
            tools (List[Callable]): A list of callable tools.
        """
        self.tools = tools
        self.llm_with_tools = self.llm_with_tools.bind_tools(tools)
        self._build_graph()
        
    def set_system_prompt(self, sys_prompt: str) -> None:
        """
        Sets the system prompt message.
        
        Args:
            sys_prompt (str): The system prompt message.
        """
        self.sys_msg = SystemMessage(content=sys_prompt)
        self._build_graph()
        
    def set_llm(self, llm: ChatOpenAI) -> None:
        """
        Sets the language model for the agent.
        
        Args:
            llm (ChatOpenAI): The language model.
        """
        self.llm_with_tools = llm.bind_tools(self.tools)
        self._build_graph()
        

    # Node
    def _assistant(self, state: MessagesState):
        return {"messages": [self.llm_with_tools.invoke([self.sys_msg] + state["messages"])]}
    
    def _build_graph(self):
        # Graph
        self.builder = StateGraph(MessagesState)

        # Define nodes: these do the work
        self.builder.add_node("assistant", self._assistant)
        self.builder.add_node("tools", ToolNode(self.tools))
        
        # Define edges: these determine how the control flow moves
        self.builder.add_edge(START, "assistant")
        self.builder.add_conditional_edges(
            "assistant",
            # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
            # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
            tools_condition,
        )
        self.builder.add_edge("tools", "assistant")
        
        self.memory = MemorySaver()
        
        self.react_graph_memory = self.builder.compile(checkpointer=self.memory)
    
    def invoke(self, state: MessagesState, config: Dict):
        return self.react_graph_memory.invoke(state, config)




import importlib
import inspect

def import_tools(module_name: str) -> List[Callable]:
    """
    Imports all callable tools from the specified module.
    
    Args:
        module_name (str): The name of the module to import tools from.
        
    Returns:
        List[Callable]: A list of callable tools from the module.
    """
    module = importlib.import_module(module_name)
    tools = [func for name, func in inspect.getmembers(module, inspect.isfunction)]
    return tools

# Example usage
tools = import_tools('example_tools')