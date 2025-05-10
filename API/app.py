from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from langchain.prompts import ChatPromptTemplate
from langserve import add_routes
import uvicorn
import os
from langchain_community.llms import Ollama
from dotenv import load_dotenv
import json
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from .env
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API Server"
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Define root route
@app.get("/")
def root():
    return {"message": "Welcome to LangChain API"}

# Create a simple direct API endpoint for essay generation
@app.post("/essay/invoke")
async def generate_essay(request: Request):
    try:
        # Parse the request body
        body = await request.json()
        topic = body.get("input", {}).get("topic", "general topic")
        
        # Try different models in order of preference
        models_to_try = ["llama3.2", "llama3", "llama2", "mistral"]
        last_error = None
        
        for model in models_to_try:
            try:
                # Initialize Ollama with the current model
                llm = Ollama(model=model)
                
                # Create prompt
                prompt = f"Write me an essay about {topic} with 100 words."
                
                # Generate response
                response = llm.invoke(prompt)
                
                # Return formatted response if successful
                return JSONResponse(content={"output": response})
            except Exception as e:
                last_error = str(e)
                continue
        
        # If we get here, all models failed - provide a fallback response
        fallback_response = f"This is a fallback response since no Ollama models are available. Here's a brief essay about {topic}:\n\n"
        fallback_response += f"{topic.capitalize()} is a fascinating subject that has captured the interest of many people around the world. "
        fallback_response += f"When exploring {topic}, it's important to consider various perspectives and approaches. "
        fallback_response += f"Many experts have studied {topic} extensively and have developed theories and methodologies to better understand it. "
        fallback_response += f"In conclusion, {topic} remains an important area for further research and discussion."
        
        # Log the error but return a successful response with the fallback text
        print(f"Warning: Using fallback response. Error was: {last_error}")
        return JSONResponse(content={"output": fallback_response})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

# Create a simple direct API endpoint for test case generation
@app.post("/poem/invoke")
async def generate_test_cases(request: Request):
    try:
        # Parse the request body
        body = await request.json()
        topic = body.get("input", {}).get("topic", "general topic")
        
        # Try different models in order of preference
        models_to_try = ["llama3.2", "llama3", "llama2", "mistral"]
        last_error = None
        
        for model in models_to_try:
            try:
                # Initialize Ollama with the current model
                llm = Ollama(model=model)
                
                # Create prompt
                prompt = f"Write me test case scenarios for {topic} with 20 steps."
                
                # Generate response
                response = llm.invoke(prompt)
                
                # Return formatted response if successful
                return JSONResponse(content={"output": response})
            except Exception as e:
                last_error = str(e)
                continue
        
        # If we get here, all models failed - provide a fallback response
        fallback_response = f"This is a fallback response since no Ollama models are available. Here are some test case scenarios for {topic}:\n\n"
        fallback_response += f"Test Case 1: Basic Functionality\n"
        fallback_response += f"1. Initialize {topic} with default parameters\n"
        fallback_response += f"2. Verify that {topic} loads correctly\n"
        fallback_response += f"3. Test basic operations with {topic}\n"
        fallback_response += f"4. Validate output formats\n\n"
        
        fallback_response += f"Test Case 2: Edge Cases\n"
        fallback_response += f"1. Test {topic} with minimum input values\n"
        fallback_response += f"2. Test {topic} with maximum input values\n"
        fallback_response += f"3. Test {topic} with invalid inputs\n"
        fallback_response += f"4. Verify error handling\n\n"
        
        fallback_response += f"Test Case 3: Performance\n"
        fallback_response += f"1. Measure response time of {topic}\n"
        fallback_response += f"2. Test {topic} under load\n"
        fallback_response += f"3. Verify resource usage\n"
        
        # Log the error but return a successful response with the fallback text
        print(f"Warning: Using fallback response. Error was: {last_error}")
        return JSONResponse(content={"output": fallback_response})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

# Create a chatbot endpoint for agriculture-related question answering
@app.post("/chat/invoke")
async def chat(request: Request):
    try:
        # Parse the request body
        body = await request.json()
        question = body.get("input", {}).get("question", "Tell me something about agriculture")
        
        # Check if the question is agriculture-related
        agriculture_keywords = [
            "agriculture", "farming", "crop", "harvest", "soil", "plant", "seed", "fertilizer",
            "irrigation", "pesticide", "farm", "farmer", "cultivation", "livestock", "organic",
            "sustainable", "yield", "grain", "vegetable", "fruit", "dairy", "cattle", "poultry",
            "greenhouse", "compost", "hydroponics", "agroforestry", "permaculture", "tractor"
        ]
        
        # Check if the question contains any agriculture keywords
        is_agriculture_related = any(keyword in question.lower() for keyword in agriculture_keywords)
        
        if not is_agriculture_related:
            return JSONResponse(content={
                "output": "I'm an agriculture specialist chatbot. Please ask me questions related to farming, crops, soil, irrigation, or other agricultural topics."
            })
        
        # Use llama3.2 model directly since it's now installed
        try:
            # Initialize Ollama with llama3.2
            llm = Ollama(model="llama3.2")
            
            # Create enhanced prompt with agriculture context and conversation style
            prompt = f"""You are an agricultural expert assistant with deep knowledge of farming, crops, soil science, irrigation, livestock, and sustainable agriculture practices. 

Provide a helpful, informative, and detailed response to the following question about agriculture. Use markdown formatting where appropriate to make your answer more readable.

Question: {question}

Answer (be concise but thorough, and format your response with markdown where appropriate):"""
            
            # Generate response
            response = llm.invoke(prompt)
            
            # Return formatted response if successful
            return JSONResponse(content={"output": response})
        except Exception as e:
            last_error = str(e)
        
        # If we get here, all models failed - provide agriculture-specific fallback responses
        fallback_responses = {
            "soil": "Soil health is fundamental to successful farming. Good soil contains a balance of minerals, organic matter, air, water, and microorganisms. Regular soil testing is recommended to monitor pH levels and nutrient content.",
            "crop": "Crop selection should be based on your local climate, soil conditions, and market demand. Crop rotation is an important practice to maintain soil health and reduce pest problems.",
            "irrigation": "Efficient irrigation is crucial for water conservation. Drip irrigation and precision sprinklers can reduce water usage while ensuring crops receive adequate moisture.",
            "fertilizer": "Balanced fertilization is key to crop health. Organic fertilizers improve soil structure while providing nutrients, while synthetic fertilizers offer precise nutrient control.",
            "pest": "Integrated Pest Management (IPM) combines biological controls, habitat manipulation, and resistant crop varieties with judicious pesticide use for effective and environmentally sensitive pest control.",
            "organic": "Organic farming avoids synthetic fertilizers and pesticides, focusing instead on crop rotation, green manure, compost, and biological pest control to maintain soil productivity and control pests.",
            "sustainable": "Sustainable agriculture aims to meet society's food needs while preserving the environment through practices like conservation tillage, water management, and diverse crop rotations.",
            "livestock": "Livestock management involves proper housing, nutrition, health care, and breeding practices to ensure animal welfare and productive farming operations.",
            "harvest": "Proper harvest timing is critical for crop quality. Most crops have optimal harvest windows based on maturity indicators specific to each plant type.",
            "seed": "Seed selection is a crucial decision for farmers. Consider factors like yield potential, disease resistance, and adaptability to local conditions when choosing seeds."
        }
        
        # Find which keywords are in the question
        matched_keywords = [keyword for keyword in fallback_responses.keys() if keyword in question.lower()]
        
        if matched_keywords:
            # Use the first matched keyword's response
            fallback_response = fallback_responses[matched_keywords[0]]
        else:
            # General agriculture response if no specific matches
            fallback_response = "Agriculture is the science and art of cultivating plants and livestock. Modern agriculture includes aspects of environmental conservation, soil management, crop rotation, and technological innovation. Sustainable farming practices aim to meet current food needs while ensuring resources for future generations."
        
        # Log the error but return a successful response with the fallback text
        print(f"Warning: Using agriculture fallback response. Error was: {last_error}")
        return JSONResponse(content={"output": fallback_response})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

# Start the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8007)
