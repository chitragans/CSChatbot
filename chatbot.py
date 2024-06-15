import os
import openai
from langchain import Agent, Chain, Memory, Prompt, Text

# Set up OpenAI API key
openai.api_key = 'your-openai-api-key'

class CustomerSupportChatbot:
    def __init__(self):
        # Initialize memory to store user preferences
        self.memory = Memory()
        
        # Define the prompt template for the agent
        prompt_template = """
        You are a customer support assistant. Remember the user's preferences and past interactions.
        
        Current conversation:
        {conversation}

        User's preferences:
        {preferences}

        Your response:
        """

        # Initialize the prompt with the template
        self.prompt = Prompt(template=prompt_template)

        # Initialize the agent with the prompt and memory
        self.agent = Agent(prompt=self.prompt, memory=self.memory)

    def add_preference(self, user_id, preference):
        # Add user preference to memory
        self.memory.set(f"user_{user_id}_preferences", preference)

    def get_preference(self, user_id):
        # Retrieve user preference from memory
        return self.memory.get(f"user_{user_id}_preferences")

    def chat(self, user_id, user_input):
        # Retrieve user preferences
        preferences = self.get_preference(user_id) or "No preferences provided yet."

        # Create conversation context
        conversation_context = self.memory.get("conversation_context") or ""
        conversation_context += f"\nUser: {user_input}\n"

        # Generate response
        response = self.agent.run(conversation=conversation_context, preferences=preferences)
        
        # Update conversation context in memory
        self.memory.set("conversation_context", conversation_context + f"Assistant: {response}\n")

        return response

# Example usage
if __name__ == "__main__":
    chatbot = CustomerSupportChatbot()

    # Simulate user interaction
    user_id = "user123"

    # Adding preferences
    chatbot.add_preference(user_id, "User prefers Apple products.")

    # User starts chatting
    print("Chatbot: Hello! How can I assist you today?")
    user_input = input("User: ")
    response = chatbot.chat(user_id, user_input)
    print(f"Chatbot: {response}")

    # User continues chatting
    user_input = input("User: ")
    response = chatbot.chat(user_id, user_input)
    print(f"Chatbot: {response}")
