from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai
import os


# Load .env file
load_dotenv()


# Create Flask application
app = Flask(__name__)


# Allow frontend to communicate with backend
CORS(app)


# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")


# Check API key
if not api_key:
    print("ERROR: GEMINI_API_KEY not found in .env file")
    raise ValueError("GEMINI_API_KEY is missing")


# Create Gemini client
client = genai.Client(api_key=api_key)


# ---------------- HOME ROUTE ----------------

@app.route("/")
def home():
    return "AI Tourist Tracker Backend is Running"


# ---------------- TRAVEL PLAN ROUTE ----------------

@app.route("/plan", methods=["POST"])
def plan():

    try:

        # Get JSON data
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No data received"
            }), 400


        # Get user inputs
        destination = str(
            data.get("destination", "")
        ).strip()

        days = data.get("days")

        budget = data.get("budget")

        interests = data.get("interests", [])


        # ---------------- VALIDATION ----------------

        if not destination:
            return jsonify({
                "error": "Destination is required"
            }), 400


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
                "error": "For now, maximum trip duration is 30 days"
            }), 400


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


        if not isinstance(interests, list):
            interests = [str(interests)]


        interests = [
            str(interest).strip()
            for interest in interests
            if str(interest).strip()
        ]


        if not interests:
            return jsonify({
                "error": "At least one interest is required"
            }), 400


        # Convert interests into readable text
        interest_text = ", ".join(interests)


        # ---------------- AI PROMPT ----------------

        prompt = f"""
You are an expert travel planner.

Create a practical and realistic travel itinerary.

USER INFORMATION

Destination: {destination}
Number of days: {days}
Total budget: ₹{budget:.0f}
Interests: {interest_text}


IMPORTANT DAY RULE:

The user requested EXACTLY {days} days.

Generate exactly {days} days.

Start with Day 1.

End with Day {days}.

DO NOT generate Day {days + 1}.

DO NOT add extra travel days.

If the user requests 1 day, generate only Day 1.

If the user requests 2 days, generate only Day 1 and Day 2.


FOR EVERY DAY USE THIS STRUCTURE:

DAY X

Morning:
- Approximate time
- Place
- Activity

Afternoon:
- Approximate time
- Place
- Activity

Evening:
- Approximate time
- Place
- Activity

Food suggestions:
- Suitable local food suggestions

Estimated cost for the day:
- Approximate amount


TRIP REQUIREMENTS:

1. Focus on the user's interests.
2. Keep the trip within the total budget of ₹{budget:.0f}.
3. Suggest realistic places.
4. Include reasonable transportation suggestions.
5. Avoid unrealistic travel distances between activities.
6. Do not repeat the same attraction unnecessarily.
7. Make the schedule practical rather than overcrowded.
8. Mention when an activity or attraction may require an entry fee.
9. Keep the writing clear and easy to read.


AFTER THE FINAL DAY, PROVIDE:

TOTAL ESTIMATED BUDGET

- Accommodation
- Food
- Transportation
- Activities
- Other expenses
- Approximate total


Then provide:

TRAVEL TIPS

- Useful travel tips for the destination


FINAL RULE:

Return exactly {days} requested travel days.

Do not create Day {days + 1}.
"""


        # ---------------- GEMINI REQUEST ----------------

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )


        # Get generated text
        itinerary = response.text


        if not itinerary:
            return jsonify({
                "error": "AI did not return an itinerary"
            }), 500


        # ---------------- SEND TO FRONTEND ----------------

        return jsonify({

            "success": True,

            "destination": destination,

            "days": days,

            "budget": budget,

            "interests": interests,

            "itinerary": itinerary

        })


    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "error": "Unable to generate itinerary. Please try again."
        }), 500


# ---------------- START SERVER ----------------

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )