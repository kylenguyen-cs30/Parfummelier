from flask import Blueprint, request, jsonify, abort
from typing import List, Dict
from .accord_note_table import get_accord_note_data_json, get_accords_from_notebank

quiz_blueprint = Blueprint("quiz", __name__)

@quiz_blueprint.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Quiz Service launched"}), 200

# In-memory dictionary for user notebanks
user_notebanks: Dict[int, List[str]] = {}

# Mapping of answers to corresponding notes
ANSWER_TO_NOTES = {
    "Reading a book in a cozy nook": ["Bergamot", "Palestinian Sweet Lime", "Plum"],
    "Watching your favorite series with a snack": ["Popcorn", "Petitgrain", "Pomegranate"],
    "Meditating or practicing yoga": ["Frankincense", "Myrrh", "Lavender"],
    "Cooking up a new recipe": ["Bigarade", "Oregano", "Strawberry"],
    "Upbeat pop that makes you dance": ["Peach", "Pomelo", "Watermelon"],
    "Classic rock with guitar riffs": ["Bitter Orange", "Sudachi citrus", "Yuzu"],
    "Soothing classical music": ["Blood Orange", "Tangelo", "Iris"],
    "Jazzy tunes with a laid-back vibe": ["Buddha's Hand", "Yuzu", "Amber"],
    "A freshly brewed cup of coffee": ["Calamansi", "Hazelnut", "Caramel"],
    "A calming cup of herbal tea": ["Green Tea", "Acai Berry", "Jasmine"],
    "A glass of rich red wine": ["Grapes", "Oak", "Blackberry"],
    "A refreshing mojito cocktail": ["Lime", "Acerola", "Rum"],
    "Sunrise, when the world feels fresh and quiet": ["Candied Lemon", "Apple", "Peppermint"],
    "Mid-afternoon, when the sun is warm but not too hot": ["Chen Pi", "Apricot", "Sandalwood"],
    "Early evening, just before the stars come out": ["Chinotto", "Blackberry", "Cedar"],
    "Late at night, when everything feels calm": ["Indian Oud", "Blueberry", "Patchouli"],
    "A classic Italian pasta dish": ["Citron", "Cantaloupe", "Olive"],
    "Spicy and flavorful Mexican food": ["Cilantro", "Green Pepper", "Cinnamon"],
    "French pastries and delicate desserts": ["Citrus Water", "Thyme", "Lavender"],
    "Fresh and simple Japanese cuisine": ["Ginger", "Rice", "Yuzu"],
    "Hiking in the mountains or by the beach": ["Pine", "Oakmoss", "Sandalwood"],
    "Going to a live concert or music festival": ["Clementine", "Amberwood", "Rum"],
    "Treating yourself to a spa day": ["Finger Lime", "Chamomile", "Sandalwood"],
    "Exploring new cafes or hidden spots in the city": ["Grapefruit", "Cherry", "Coffee"],
    "A loyal and playful dog": ["Green Tangerine", "Woody", "Amber"],
    "An independent and mysterious cat": ["Hassaku", "Coconut", "Jasmine"],
    "A colorful bird that sings all day": ["Citrus", "Dragon Fruit", "Peppermint"],
    "A calm fish that swims gracefully": ["Aquatic", "Seaweed", "Salt"],
    "Relaxing on a secluded tropical island": ["Bergamot", "Agave", "Coconut"],
    "Skiing in the snowy mountains": ["Kaffir Lime", "Fig", "Clove leaf"],
    "Exploring a bustling city like New York": ["Kumquat", "Grapes", "Rose"],
    "Strolling through romantic Paris streets": ["Lemon", "Kiwi", "Amber"],
    "Spring, when everything blooms": ["Cherry Blossom", "Grass", "Lemon"],
    "Summer, with endless sunny days": ["Watermelon", "Orange Blossom", "Coconut"],
    "Fall, with cozy vibes and colorful leaves": ["Lime", "Maple", "Sandalwood"],
    "Winter, when it’s all about warmth and hot cocoa": ["Mandarin Orange", "Mango", "Gingerbread"],
    "Action-packed superhero adventure": ["Black Pepper", "Papaya", "Tobacco"],
    "A lighthearted romantic comedy": ["Strawberry", "Peach", "Cotton Candy"],
    "A mystery that keeps you on the edge of your seat": ["Neroli", "Pear", "Vetiver"],
    "A fantasy with magical creatures and faraway lands": ["Orange", "Pineapple", "Musk"],
}

# NOTE: Submit quiz responses

@quiz_blueprint.route("/submit-quiz/", methods=["POST"])
def submit_quiz():
    data = request.json
    answers = data.get("answers", [])

    if len(answers) != 10:
        abort(400, description="Quiz must have exactly 10 answers.")

    # Build the notebank based on answers
    notebank = []
    for answer in answers:
        if answer not in ANSWER_TO_NOTES:
            abort(400, description=f"Invalid answer: {answer}")
        notebank.extend(ANSWER_TO_NOTES[answer])

    # Store the notebank in localhost
    user_notebanks["localhost:5005"] = notebank

    return jsonify({"message": "Notebank created successfully", "notebank": notebank})

@quiz_blueprint.route("/accord-note-data/", methods=["POST"])
def get_accord_note_data():
    notebank = request.json.get("notebank", [])
    accords = get_accords_from_notebank(notebank)
    return jsonify(accords)

@quiz_blueprint.route("/update-notebank/", methods=["PUT"])
def update_notebank():
    # Parse the JSON data from the request
    data = request.json
    answers = data.get("answers", [])

    # Ensure that there are exactly 10 answers
    if len(answers) != 10:
        abort(400, description="Quiz must have exactly 10 answers.")

    # Initialize a new notebank for the updated answers
    updated_notebank = []

    # Validate each answer and build the updated notebank
    for answer in answers:
        if answer not in ANSWER_TO_NOTES:
            abort(400, description=f"Invalid answer: {answer}")
        updated_notebank.extend(ANSWER_TO_NOTES[answer])

    # Update the user's notebank in memory
    user_notebanks["localhost:5005"] = updated_notebank

    # Return a success message with the updated notebank
    return jsonify({"message": "Notebank updated successfully", "updated_notebank": updated_notebank})
