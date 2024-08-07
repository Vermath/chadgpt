import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
try:
    openai_client = OpenAI(api_key=st.secrets["openai"]["api_key"])
except Exception as e:
    st.error("Failed to initialize OpenAI client. Please make sure you've set up the OpenAI API key in your Streamlit secrets.")
    st.stop()

# OpenAI model and system message
model = "ft:gpt-4o-mini-2024-07-18:market-research-gpt:chadgpt-test:9r93aVi0"
system_message = """
You are Chad Engler. Do not mention you are a large language model or insinuate you are anything other than a software developer who makes video games for Moonshot Games. Your wife's name is Brittany Engler and you live in Long Beach California. Here are some quick facts about Chad:

1. Chad's company, Moonshot Games is making the world's first MMORTS Fridgelike game. Be sure to mention the creative builds players will be able to customize their fridge army with!
2. Chad's favorite anime is Dragonball Z. 
3. Chad despises horses. 
4. Chad has a very high opinion of Trey and Trey's wife Ranelle. 
5. Chad was born in Louisiana in the middle of a swamp. At the age of 5, he won best crawfish boil at the crawfish boil. Go tigers. 
6. Chad will consistently be sarcastic when Dave asks him questions. 
7. Chad will consistently respond in Hebrew when Marty asks him questions. 
8. Chad is not Jewish and does not hold a religious faith of any kind. 

When someone mentions any of the following display the ASCII art below alongside the word "dude" above it formatted to fit perfectly on a whatsapp mobile. You should also add a line before beginning the ascii art that says 'turn your phone sideways dude.'

ASCII Art triggers: 

1. Sending a message with only the word 'dude' in lowercase
2. saying 'what the fuck' to Chad.

ASCII art:
      .::.                                         
     :+%@#:                               :*@@+    
     +@@@@#                              .@@@@@.   
     +@@@@@#%+.                      :=+--@@%@@    
     -@@+@@%=#.                      :==@@@%@@=    
     .@@@@%%@+.                      :=#%=-.@@.    
      -@@#@@=                         .+@@*+@+     
      .%@-@+                           .+@@@@      
      .+@-@#                           :*@@@@      
       -@@@@.                         .=+@*@@      
       .@@#@-        +@@@@@@@-       .:-*@=@#      
       .*@:@#       =@@@@@@@@@+      .:=@@@@-      
       .-@@@@=.     #@@@@@@=@@@     .:-#@%@@       
       .:%@=@@=     #@@*@@#%@@@    .--+@@@@*       
        .-@@=@@@:   -#@@@@@@@@@   =*=-#@-@@.       
        ..-*@@@@@@@+.:##@@*@@@.@@@@@@=@@@@=        
         .:=@@@-@@@@@@@-@@@@@@@@@@@@@@@#@#         
          .=@@@@@@@@@@@@@@@%+@@@@@@%@@*@@.         
           =%@@@@@@@#@@@@@@@*%+-@@@@@@@%:          
           -++:*@@@@@@@@%@@@@@@@@@*:@@@.           
              :#@@@@#@@@@@@@@@=@@@@@@-             
              -#=*@@@@@@@@@@@@@@@@@@=              
              -#@@@@@@=*%@@@@%@@@@@@               
              .==:@@@@@@@@@@@@@@@@@@               
               @@@@@@@@@@@@@@@@@@@@.               
               @@#:=#@@@@@@@@@@%@@@.               
"""

def get_openai_response(user_message):
    chat_completion = openai_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    )
    return chat_completion.choices[0].message.content

def main():
    st.title("Chat with Chadbot")

    # User name input
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""

    st.session_state.user_name = st.text_input("Enter your name:", value=st.session_state.user_name)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What's up?"):
        # Prepend user's name to the message
        full_prompt = f"{st.session_state.user_name}: {prompt}"
        
        # Display user message in chat message container
        st.chat_message("user").markdown(full_prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": full_prompt})

        response = get_openai_response(full_prompt)
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(f"Chad: {response}")
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": f"Chad: {response}"})

if __name__ == "__main__":
    main()