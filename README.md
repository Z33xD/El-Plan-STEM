# El Plan STEM

El Plan STEM is a Django-based web application that combines the excitement of Formula 1 with engaging, AI-powered STEM education. Whether you're a student learning physics through lap times or an F1 enthusiast curious about race analytics, this project delivers a powerful, interactive experience.

---

## Features

### F1-Themed Educational Chatbot
- Teaches STEM concepts (Science, Technology, Engineering, Mathematics) using real F1 data.
- Auto-generates quiz-style questions based on:
  - Lap times
  - Pit stops
  - Driver statistics
- Evaluates answers with explanations using Formula 1 analogies.
- Maintains conversational history for context-rich feedback.

### General F1 Assistant
- Chat with a bot to retrieve real-time facts and data about drivers, races, and circuits.
- Uses semantic vector search with sentence embeddings for intelligent query handling.

### Notes System
- Lets users create, save, and manage notes for studying or strategy planning.

### Graphing Module
- Visualizes F1 data such as speed trends, pit stop frequencies, or momentum shifts.

---

## Tech Stack

- **Backend:** Django 5.2.1
- **Database:** MongoDB (via `django-mongodb-backend`)
- **AI Integration:** Google Gemini (Gemini 1.5 Flash)
- **Machine Learning:** scikit-learn, TensorFlow, sentence-transformers
- **Frontend:** Django templates + static files (CSS/JS)

---

## AI and ML Details

- Chatbot uses Google's Gemini model for generating and evaluating questions.
- Semantic search powered by `sentence-transformers` for intelligent data retrieval.
- ML models include:
  - `turn_severity_rf_model.joblib`: Turn severity predictions
  - `momentum_lstm_model.h5`: Momentum analysis
  - `f1_momentum_model.h5`: Momentum-based forecasting

---

## Project Structure

```
El-Plan-STEM/
│
├── backend/
│ ├── core/ # General site logic
│ ├── chatbot/ # Chatbot and AI logic
│ ├── ml_models/ # Legacy ML code (merged into chatbot)
│ ├── templates/ # HTML templates
│ ├── static/ # CSS, JS, images
│ └── manage.py
├── requirements.txt
└── .env (your environment variables)
```

---

## Setup Instructions

1. **Install Python 3.11**

2. **Create virtual environment**
   ```bash
   py -3.11 -m venv venv
   ```

3. **Activate the environment**
   ```bash
   .\venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the server**
   ```bash
   cd backend
   python manage.py runserver
   ```

6. **Stop the server**
   ```mathematica
   ctrl + C
   ```

7. **Deactivate the environment**
   ```bash
   deactivate
   ```

---

## Routes Overview

| Route                    | Description                       |
| ------------------------ | --------------------------------- |
| `/chatbot/`              | Main chatbot interface            |
| `/chatbot/chat/`         | Chat endpoint for educational bot |
| `/chatbot/general/`      | General F1 assistant UI           |
| `/chatbot/general/chat/` | General assistant chat endpoint   |
| `/`                      | Home page                         |
| `/about/`                | About the project                 |

---

## Special Thanks

Thanks to the teams behind:
- Google Generative AI
- Ergast's Formula 1 open datasets
- Django & MongoDB communities

---

> "Learning STEM at full throttle with the power of Formula 1!"

---