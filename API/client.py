import requests
import streamlit as st
import json

def get_GCP_response(input_text):
    try:
        response = requests.post("http://localhost:8007/essay/invoke",
                              json={'input':{'topic':input_text}})
        
        # Debug information
        st.write(f"Status Code: {response.status_code}")
        
        # Check if response is successful
        if response.status_code == 200:
            try:
                return response.json()['output']
            except json.JSONDecodeError as e:
                st.error(f"Error decoding JSON: {e}")
                st.write(f"Response content: {response.text}")
                return "Error processing response"
        else:
            st.error(f"API Error: {response.status_code}")
            st.write(f"Response content: {response.text}")
            return f"API Error: {response.status_code}"
    except Exception as e:
        st.error(f"Request Error: {str(e)}")
        return f"Error: {str(e)}"

def get_Ollama_response(input_text1):
    try:
        response = requests.post("http://localhost:8007/poem/invoke",
                              json={'input':{'topic':input_text1}})
        
        # Debug information
        st.write(f"Status Code: {response.status_code}")
        
        # Check if response is successful
        if response.status_code == 200:
            try:
                return response.json()['output']
            except json.JSONDecodeError as e:
                st.error(f"Error decoding JSON: {e}")
                st.write(f"Response content: {response.text}")
                return "Error processing response"
        else:
            st.error(f"API Error: {response.status_code}")
            st.write(f"Response content: {response.text}")
            return f"API Error: {response.status_code}"
    except Exception as e:
        st.error(f"Request Error: {str(e)}")
        return f"Error: {str(e)}"

st.title('LangChain API verification for Client app')
input_text = st.text_input("Write essay on")
input_text1 = st.text_input("Write poem on")

if input_text:
    st.write(get_GCP_response(input_text))
    
if input_text1:
    st.write(get_Ollama_response(input_text1))