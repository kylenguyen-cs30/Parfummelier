from flask import Blueprint, request, jsonify, abort
from typing import List, Dict
import requests
import os

PRODUCT_API_URL_QUIZ_SERVICES = os.getenv(
    "PRODUCT_API_URL", "http://product-service:5000"
)

quiz_blueprint = Blueprint("quiz", __name__)


@quiz_blueprint.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Quiz Service launched"}), 200


# In-memory dictionary for user accordbanks
user_accordbanks: Dict[int, List[str]] = {}

# Mapping of answers to corresponding accords
ANSWER_TO_ACCORDS = {
    "Reading a book in a cozy nook": ["Powdery", "Amber", "Woody"],
    "Watching your favorite series with a snack": ["Sweet", "Aromatic", "Nutty"],
    "Meditating or practicing yoga": ["Earthy", "Balsamic", "Lavender"],
    "Cooking up a new recipe": ["Herbal", "Spicy", "Bitter"],
    "Upbeat pop that makes you dance": ["Fruity", "Tropical", "Citrus"],
    "Classic rock with guitar riffs": ["Leather", "Warm Spicy", "Tobacco"],
    "Soothing classical music": ["Iris", "White Floral", "Floral"],
    "Jazzy tunes with a laid-back vibe": ["Soft Spicy", "Patchouli", "Mossy"],
    "A freshly brewed cup of coffee": ["Coffee", "Caramel", "Chocolate"],
    "A calming cup of herbal tea": ["Green", "Soapy", "Fresh"],
    "A glass of rich red wine": ["Mossy", "Oud", "Honey"],
    "A refreshing mojito cocktail": ["Rum", "Salty", "Mint"],
    "Sunrise, when the world feels fresh and quiet": [
        "Ozonic",
        "Fresh Spicy",
        "Aldehydic",
    ],
    "Mid-afternoon, when the sun is warm but not too hot": [
        "Lactonic",
        "Citrus",
        "Marine",
    ],
    "Early evening, just before the stars come out": ["Rose", "Powdery", "Camphor"],
    "Late at night, when everything feels calm": ["Musky", "Mineral", "Beeswax"],
    "A classic Italian pasta dish": ["Animalic", "Savory", "Earthy"],
    "Spicy and flavorful Mexican food": ["Cinnamon", "Smoky", "Peppery"],
    "French pastries and delicate desserts": ["Vanilla", "Almond", "Cacao"],
    "Fresh and simple Japanese cuisine": ["Aquatic", "Green", "Rice"],
    "Hiking in the mountains or by the beach": ["Conifer", "Amber", "Sand"],
    "Going to a live concert or music festival": ["Metallic", "Rum", "Leather"],
    "Treating yourself to a spa day": ["Floral", "Soapy", "Tuberose"],
    "Exploring new cafes or hidden spots in the city": ["Coffee", "Nutty", "Woodsy"],
    "A loyal and playful dog": ["Musky", "Honey", "Soft Spicy"],
    "An independent and mysterious cat": ["Animalic", "Patchouli", "Violet"],
    "A colorful bird that sings all day": ["Fruity", "Citrus", "Yellow Floral"],
    "A calm fish that swims gracefully": ["Aquatic", "Salty", "Marine"],
    "Relaxing on a secluded tropical island": ["Coconut", "Tropical", "Fresh"],
    "Skiing in the snowy mountains": ["Icy", "Woody", "Powdery"],
    "Exploring a bustling city like New York": ["Industrial Glue", "Amber", "Concrete"],
    "Strolling through romantic Paris streets": ["Rose", "Powdery", "Floral"],
    "Spring, when everything blooms": ["Floral", "Green", "Fresh"],
    "Summer, with endless sunny days": ["Citrus", "Tropical", "White Floral"],
    "Fall, with cozy vibes and colorful leaves": ["Warm Spicy", "Herbal", "Earthy"],
    "Winter, when it’s all about warmth and hot cocoa": [
        "Vanilla",
        "Cinnamon",
        "Nutty",
    ],
    "Action-packed superhero adventure": ["Black Pepper", "Leather", "Smoky"],
    "A lighthearted romantic comedy": ["Sweet", "Fruity", "Soft Spicy"],
    "A mystery that keeps you on the edge of your seat": ["Earthy", "Woody", "Dark"],
    "A fantasy with magical creatures and faraway lands": ["Musk", "Green", "Amber"],
}


# Submit quiz responses
@quiz_blueprint.route("/submit-quiz/", methods=["POST"])
def submit_quiz():
    data = request.json
    answers = data.get("answers", [])

    if len(answers) != 10:
        abort(400, description="Quiz must have exactly 10 answers.")

    # Using a set to store unique accords
    accordbank_set = set()
    for answer in answers:
        if answer not in ANSWER_TO_ACCORDS:
            abort(400, description=f"Invalid answer: {answer}")
        accordbank_set.update(ANSWER_TO_ACCORDS[answer])  # Adds only unique accords

    # Convert set back to list for storage
    accordbank = list(accordbank_set)

    # Store the accordbank in memory
    user_accordbanks["localhost:5005"] = accordbank

    return jsonify(
        {"message": "Accordbank created successfully", "accordbank": accordbank}
    )


@quiz_blueprint.route("/accord-data/", methods=["POST"])
def get_accord_data():
    accordbank = request.json.get("accordbank", [])
    accords = list(set(accordbank))
    return jsonify(accords)


@quiz_blueprint.route("/update-accordbank/", methods=["PUT"])
def update_accordbank():
    data = request.json
    answers = data.get("answers", [])

    if len(answers) != 10:
        abort(400, description="Quiz must have exactly 10 answers.")

    # Using a set to store unique accords for the updated accordbank
    updated_accordbank_set = set()
    for answer in answers:
        if answer not in ANSWER_TO_ACCORDS:
            abort(400, description=f"Invalid answer: {answer}")
        updated_accordbank_set.update(ANSWER_TO_ACCORDS[answer])

    # Convert set back to list for storage
    updated_accordbank = list(updated_accordbank_set)

    # Update the user's accordbank in memory
    user_accordbanks["localhost:5005"] = updated_accordbank

    return jsonify(
        {
            "message": "Accordbank updated successfully",
            "updated_accordbank": updated_accordbank,
        }
    )


# getting accord from the user
def get_recommendations_for_user(accordbank):
    url = f"{PRODUCT_API_URL_QUIZ_SERVICES}/recommendations"
    response = requests.post(url, json={"accordbank": accordbank})

    if response.status_code == 200:
        return response.json()  # Ensure this is returning the full response
    else:
        raise Exception(f"Failed to fetch recommendations: {response.text}")


@quiz_blueprint.route("/get-recommendations/", methods=["POST"])
def get_recommendations():
    data = request.json
    accordbank = data.get("accordbank", [])

    if not accordbank:
        abort(400, description="Accord bank data is required.")

    try:
        # Call product-service to get recommendations based on the accordbank
        recommendations = get_recommendations_for_user(accordbank)
        return jsonify({"recommendations": recommendations})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@quiz_blueprint.errorhandler(400)
def bad_request(error):
    response = jsonify({"description": error.description})
    response.status_code = 400
    return response
