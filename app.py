from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai
import os
import traceback

# Load environment variables

load_dotenv()

# Create Flask application

app = Flask(**name**)

# Allow frontend to communicate with backend

CORS(app)

# Get Gemini API key

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
print("ERROR: GEMINI_API_KEY not found", flush=True)
raise ValueError("GEMINI_API_KEY is missing")

print("GEMINI_API_KEY found", flush=True)

# Create Gemini client

client = genai.Client(api_key=api_key)

@app.route("/")
def home():
return "AI Tourist Tracker Backend is Running"

@app.route("/plan", methods=["POST"])
def plan():

```
try:
    data = request.get_json()

    print("Received data:", data, flush=True)

    if not data:
        return jsonify({
            "error": "No data received"
        }), 400

    destination = str(
        data.get("destination", "")
    ).strip()

    days = data.get("days")
    budget = data.get("budget")

    interests = data.get("interests")

    if interests is None:
        interests = data.get("interest", [])

    # Destination validation
    if not destination:
        return jsonify({
            "error": "Destination is required"
        }), 400

    # Days validation
    if days is None or str(days).strip() == "":
        return jsonify({
            "error": "Number of days is required"
        }), 400

    try:
        days = int(days)
    except (ValueError, TypeError):
        return jsonify({
            "error": "Number of days must be a whole number"
        }), 400

    if days < 1:
        return jsonify({
            "error": "Number of days must be at least 1"
        }), 400

    if days > 30:
        return jsonify({
            "error": "Maximum trip duration is 30 days"
        }), 400

    # Budget validation
    if budget is None or str(budget).strip() == "":
        return jsonify({
            "error": "Budget is required"
        }), 400

    try:
        budget = float(budget)
    except (ValueError, TypeError):
        return jsonify({
            "error": "Budget must be a number"
        }), 400

    if budget <= 0:
        return jsonify({
            "error": "Budget must be greater than 0"
        }), 400

    # Interests
    if not isinstance(interests, list):
        interests = [interests]

    interests = [
        str(interest).strip()
        for interest in interests
        if str(interest).strip()
    ]

    if not interests:
        return jsonify({
            "error": "At least one interest is required"
        }), 400

    interest_text = ", ".join(interests)

    # AI prompt
    prompt = f"""
```

You are an expert travel planner.

Create a practical and realistic travel itinerary.

Destination: {destination}
Number of days: {days}
Total budget: ₹{budget:.0f}
Interests: {interest_text}

Generate EXACTLY {days} days.

Start with Day 1.
End with Day {days}.
Do not create Day {days + 1}.

For every day provide:

Morning:

* Approximate time
* Place
* Activity

Afternoon:

* Approximate time
* Place
* Activity

Evening:

* Approximate time
* Place
* Activity

Food suggestions:

* Suitable local food

Estimated cost for the day:

* Approximate amount

Requirements:

1. Focus on the user's interests.
2. Keep the trip within the total budget.
3. Suggest realistic places.
4. Include transportation suggestions.
5. Avoid unrealistic travel distances.
6. Do not unnecessarily repeat attractions.
7. Keep the schedule practical.
8. Mention entry fees where appropriate.
9. Use clear and easy-to-read language.

After the final day provide:

TOTAL ESTIMATED BUDGET

* Accommodation
* Food
* Transportation
* Activities
* Other expenses
* Approximate total

Then provide:

TRAVEL TIPS

* Useful travel tips for the destination.

FINAL RULE:

Return exactly {days} requested travel days.
Do not create Day {days + 1}.
"""

```
    print("===================================", flush=True)
    print("Sending request to Gemini...", flush=True)
    print("Destination:", destination, flush=True)
    print("Days:", days, flush=True)
    print("Budget:", budget, flush=True)
    print("Interests:", interests, flush=True)
    print("===================================", flush=True)

    # Gemini request
    print("Creating Gemini chat...", flush=True)

    chat = client.chats.create(
        model="gemini-3.8-flash"
    )

    print("Gemini chat created.", flush=True)
    print("Sending prompt to Gemini...", flush=True)

    response = chat.send_message(prompt)

    print("Gemini response received.", flush=True)

    itinerary = response.text

    if not itinerary:
        print("ERROR: Gemini returned no text", flush=True)

        return jsonify({
            "error": "AI did not return an itinerary"
        }), 500

    print("Gemini itinerary generated successfully.", flush=True)

    return jsonify({
        "success": True,
        "destination": destination,
        "days": days,
        "budget": budget,
        "interests": interests,
        "itinerary": itinerary
    })

except Exception as e:

    print("===================================", flush=True)
    print("!!! GEMINI/BACKEND ERROR !!!", flush=True)
    print("ERROR TYPE:", type(e).__name__, flush=True)
    print("ERROR MESSAGE:", str(e), flush=True)
    print("FULL TRACEBACK:", flush=True)
    traceback.print_exc()
    print("===================================", flush=True)

    return jsonify({
        "error": "Unable to generate itinerary. Please try again.",
        "details": str(e)
    }), 500
```

# Start server

if **name** == "**main**":

```
port = int(os.environ.get("PORT", 5000))

app.run(
    host="0.0.0.0",
    port=port
)
```


           

    
            
