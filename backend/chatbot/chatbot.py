import os
import random
import google.generativeai as genai #
from pymongo import MongoClient 
from dotenv import load_dotenv  
from sentence_transformers import SentenceTransformer 
import numpy as np 

# Load environment variables
load_dotenv()

# MongoDB setup
client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
db = client["El-Plan-STEM"]
circuits_collection = db["circuits"]
lap_times_collection = db["lap_times"]
drivers_collection = db["drivers"]
pit_stops_collection = db["pit_stops"]
races_collection=db["races"]

# SentenceTransformers for embeddings
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Gemini API setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction='''
You are an expert educator and Formula 1 enthusiast. Use provided Formula 1 data to generate science-related questions (e.g., physics or math) themed around Formula 1. Wait for the student's answer. Mention the unit in which user's answer should be. Consider it correct if answer matches till 2 decimal places. Suggest the user to explain their thought-process, it is not mandatory (in the question itself).If correct, congratulate them and ask another question. If incorrect, mention that it is incorrect and explain the answer using fun, easy-to-understand F1 analogies, and ask next question.
'''
)
chat_session = model.start_chat(history=[])
custom_history=[]

def generate_embedding(text):
    return embedder.encode(text, convert_to_numpy=True).tolist()

def vector_search(query, collection, field="description_embedding", limit=1):
    query_embedding = generate_embedding(query)
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": field,
                "queryVector": query_embedding,
                "numCandidates": 100,
                "limit": limit
            }
        },
        {
            "$project": {
                "name": 1,
                "length": 1,
                "location": 1,
                "circuitId": 1,
                "_id": 0,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]
    return list(collection.aggregate(pipeline))

def get_chat_response(user_input, retrieved_data=None, correct_answer=None):
    try:
        if retrieved_data and not user_input:
            prompt = f"""
Using the Formula 1 data: {retrieved_data}
Generate a physics or math question themed around Formula 1. If retrieved data is lap_times, then use circuit length for questions. Mention to only give the final answer without any units. Format the response as:
Question: [Your question here]
"""
            response = chat_session.send_message(prompt)
            model_response = response.text
            chat_session.history.append({
                "role": "model",
                "parts": [model_response],
            })
            custom_history.append({
                "correct_answer": correct_answer,
                "retrieved_data": retrieved_data
            })
        else:
            last_message = custom_history[-1] if custom_history else None
            if last_message and "correct_answer" in last_message:
                correct_answer = last_message["correct_answer"]
                try:
                    user_answer = float(user_input.strip())
                    if abs(user_answer - correct_answer) < 0.1:
                        prompt = "Correct! Great job! Would you like another question?"
                    else:
                        prompt = f"""
Incorrect. The correct answer is {correct_answer}. Explain why using a fun Formula 1 analogy, based on the data: {last_message['retrieved_data']}.
"""
                except ValueError:
                    prompt = "Please provide a numerical answer."
            else:
                prompt = user_input
            
            chat_session.history.append({"role": "user", "parts": [user_input]})
            response = chat_session.send_message(prompt)
            model_response = response.text
            chat_session.history.append({"role": "model", "parts": [model_response]})
        return model_response
    except Exception as e:
        return f"Error: {str(e)}"

def select_random_data_source():
    return random.choice(["lap_times","drivers","pit_stops"])

def build_retrieved_data(source_type):
    try:

        if source_type == "lap_times":
            doc = lap_times_collection.aggregate([{ "$sample": { "size": 1 } }]).next()
            circuit = races_collection.find_one({"raceId": doc["raceId"]})
            
            if not circuit or "length" not in circuit or "name" not in circuit:
                return None, None 
            lap_time_sec = doc["milliseconds"] / 1000
            #length_km = circuit["length"]
            #speed_kmh = length_km / (lap_time_sec / 3600)
            return {
                "type": "lap_times",
                "driverId": doc["driverId"],
                "lap_time_sec": lap_time_sec,
                "circuit": circuit["name"],
                #"circuit_length_km": length_km,
                #"speed_kmh": round(speed_kmh, 2)
            }, None

        elif source_type == "drivers":
            doc = drivers_collection.aggregate([{ "$sample": { "size": 1 } }]).next()
            return {
                "type": "drivers",
                "name": f"{doc['forename']} {doc['surname']}",
                "dob": doc["dob"],
                "nationality": doc["nationality"]
            }, None

        elif source_type == "pit_stops":
            doc = pit_stops_collection.aggregate([{ "$sample": { "size": 1 } }]).next()
            duration_sec = float(doc["duration"])
            return {
                "type": "pit_stops",
                "driverId": doc["driverId"],
                "duration_sec": duration_sec,
                "raceId": doc["raceId"],
                "stop": doc["stop"]
            }, round(duration_sec, 2)
    except Exception as e:
        print(f"Error retrieving {source_type} data: {e}")
        return None, None

if __name__ == "__main__":
    print("Bot: Ready to ask a science question based on real F1 data!\n")

    source = select_random_data_source()
    retrieved_data, correct_answer = build_retrieved_data(source)

    if retrieved_data:
        response = get_chat_response("", retrieved_data, correct_answer)
        print(f"Bot: {response}\n")

    while True:
        user_input = input("You: ")
        print()
        response = get_chat_response(user_input)
        print(f"Bot: {response}\n")
