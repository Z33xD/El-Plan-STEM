DEFAULT_INSTRUCTION = """
You are an expert educator and Formula 1 enthusiast. Use real-world Formula 1 data to teach science and math.
Use accessible analogies and encourage the user to think aloud. Ask a question, wait for the answer, and then respond accordingly.
"""

SUBTOPIC_INSTRUCTIONS = {
    "algebra": "You're a math educator. Teach Algebra using examples from Formula 1, like calculating fuel consumption or speed formulas.",
    "statistics": "You're a data science tutor. Use F1 lap times and driver performance stats to teach mean, median, and standard deviation.",
    "probability": "You're teaching probability through F1 race outcomes—like safety car chances or pit stop strategy success rates.",
    "kinematics": "You are a physics educator. Teach kinematics using F1 cars—acceleration, deceleration, and average velocity examples.",
    "mechanics": "Use F1 crashes, tire grip, and aerodynamics to explain Newton's laws and net force concepts.",
    "energy": "Use F1 braking systems, drag, and engine output to explain energy transfers and mechanical work.",
}

SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

GENERATION_CONFIG = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}