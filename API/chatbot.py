import streamlit as st
import requests
import json

st.title('Agriculture Expert Chatbot')
st.subheader('Your AI assistant for farming and agriculture questions')

# Add a farm-themed image
st.image('https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80', caption='Sustainable Farming')

# Initialize chat history and conversation context
if "messages" not in st.session_state:
    st.session_state.messages = []
    
# Initialize conversation context to track topics discussed
if "context" not in st.session_state:
    st.session_state.context = {
        "topics_discussed": [],
        "last_question": "",
        "follow_up_suggestions": []
    }

# Add quick question buttons at the top
st.write("### Quick Questions")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🌱 Best crops for beginners?"):
        st.session_state.quick_question = "What are the best crops for beginner farmers?"

with col2:
    if st.button("💧 Water conservation tips?"):
        st.session_state.quick_question = "What are some effective water conservation techniques for farming?"

with col3:
    if st.button("🌿 Organic farming basics?"):
        st.session_state.quick_question = "What are the basic principles of organic farming?"

# Display chat messages from history on app rerun
st.write("### Conversation")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to process user input and get response
def process_input(user_input):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Update context with the last question
    st.session_state.context["last_question"] = user_input
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking... ⏳")
        
        try:
            # Send the question to the API
            response = requests.post(
                "http://localhost:8007/chat/invoke",
                json={"input": {"question": user_input}}
            )
            
            # Check if response is successful
            if response.status_code == 200:
                try:
                    assistant_response = response.json()["output"]
                    
                    # Replace the placeholder with the actual response
                    message_placeholder.markdown(assistant_response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                    
                    # Extract topics from the response to suggest follow-up questions
                    extract_topics_and_suggest_followups(user_input, assistant_response)
                    
                except json.JSONDecodeError as e:
                    message_placeholder.error(f"Error decoding response: {e}")
                    st.write(f"Response content: {response.text}")
            else:
                message_placeholder.error(f"API Error: {response.status_code}")
                st.write(f"Response content: {response.text}")
        except Exception as e:
            message_placeholder.error(f"Request Error: {str(e)}")

# Function to extract topics and suggest follow-up questions
def extract_topics_and_suggest_followups(question, response):
    # Simple keyword extraction for agricultural topics
    topics = ["soil", "crop", "irrigation", "fertilizer", "pest", "organic", 
              "sustainable", "livestock", "harvest", "seed"]
    
    # Find topics in the response
    found_topics = [topic for topic in topics if topic in response.lower()]
    
    # Add to topics discussed if not already there
    for topic in found_topics:
        if topic not in st.session_state.context["topics_discussed"]:
            st.session_state.context["topics_discussed"].append(topic)
    
    # Generate follow-up suggestions based on topics
    follow_ups = []
    if "soil" in found_topics:
        follow_ups.append("How can I improve soil fertility naturally?")
    if "crop" in found_topics:
        follow_ups.append("What crop rotation practices do you recommend?")
    if "irrigation" in found_topics:
        follow_ups.append("What are the most water-efficient irrigation systems?")
    if "fertilizer" in found_topics:
        follow_ups.append("Can you compare organic and synthetic fertilizers?")
    
    # Save up to 3 follow-up suggestions
    st.session_state.context["follow_up_suggestions"] = follow_ups[:3]

# Check for sidebar question selection
if hasattr(st.session_state, 'sidebar_question'):
    sidebar_q = st.session_state.sidebar_question
    del st.session_state.sidebar_question  # Clear it so it doesn't repeat
    process_input(sidebar_q)

# Check for quick question selection
if hasattr(st.session_state, 'quick_question'):
    quick_q = st.session_state.quick_question
    del st.session_state.quick_question  # Clear it so it doesn't repeat
    process_input(quick_q)

# Display follow-up suggestions if available
if st.session_state.context["follow_up_suggestions"]:
    st.write("### Follow-up Questions")
    follow_up_cols = st.columns(len(st.session_state.context["follow_up_suggestions"]))
    
    for i, suggestion in enumerate(st.session_state.context["follow_up_suggestions"]):
        with follow_up_cols[i]:
            if st.button(f"❓ {suggestion}", key=f"followup_{i}"):
                st.session_state.followup_question = suggestion

# Check for follow-up question selection
if hasattr(st.session_state, 'followup_question'):
    followup_q = st.session_state.followup_question
    del st.session_state.followup_question  # Clear it so it doesn't repeat
    process_input(followup_q)

# Accept user input from chat input
if prompt := st.chat_input("Ask me about farming, crops, soil, or any agricultural topic..."):
    process_input(prompt)

# Add a sidebar with information and interactive elements
with st.sidebar:
    st.header("About")
    st.write("This is an agriculture specialist chatbot using LangChain and Ollama.")
    st.write("Ask questions about farming, crops, soil, irrigation, and other agricultural topics!")
    
    # Topic explorer with expandable sections
    st.header("Topic Explorer")
    
    with st.expander("🌱 Crop Management"):
        st.markdown("""
        - **Crop Selection**: Choose crops suited to your climate and soil
        - **Crop Rotation**: Prevent soil depletion and pest buildup
        - **Planting Techniques**: Proper spacing and timing
        - **Harvesting Methods**: Optimal timing and techniques
        """)
        if st.button("Ask about crop rotation"):
            st.session_state.sidebar_question = "What is the importance of crop rotation and how should I implement it?"
    
    with st.expander("🌿 Soil Health"):
        st.markdown("""
        - **Soil Testing**: Understanding your soil composition
        - **Soil Amendments**: Improving soil structure
        - **Cover Crops**: Protecting and enriching soil
        - **Composting**: Creating nutrient-rich soil additives
        """)
        if st.button("Ask about soil testing"):
            st.session_state.sidebar_question = "How often should I test my soil and what should I test for?"
    
    with st.expander("💧 Water Management"):
        st.markdown("""
        - **Irrigation Systems**: Drip, sprinkler, flood
        - **Water Conservation**: Reducing water waste
        - **Rainwater Harvesting**: Collecting and storing rainwater
        - **Drought Management**: Strategies for dry periods
        """)
        if st.button("Ask about drip irrigation"):
            st.session_state.sidebar_question = "What are the benefits of drip irrigation and how do I set it up?"
    
    # Conversation summary
    if st.session_state.context["topics_discussed"]:
        st.header("Conversation Summary")
        st.write("Topics discussed in this conversation:")
        for topic in st.session_state.context["topics_discussed"]:
            st.markdown(f"- {topic.capitalize()}")
    
    # Clear conversation button
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.context = {
            "topics_discussed": [],
            "last_question": "",
            "follow_up_suggestions": []
        }
        st.experimental_rerun()
    
    # API Status check
    st.header("Status")
    if st.button("Check API Status"):
        try:
            response = requests.get("http://localhost:8007/")
            if response.status_code == 200:
                st.success("Agriculture Expert API is online!")
            else:
                st.error(f"API returned status code: {response.status_code}")
        except Exception as e:
            st.error(f"Could not connect to API: {str(e)}")
