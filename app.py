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


# Start server
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )



           

    
            
