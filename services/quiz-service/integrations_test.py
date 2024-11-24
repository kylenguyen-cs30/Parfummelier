import pytest
import requests

# Base URLs for quiz-service and product-service
QUIZ_SERVICE_URL = "http://localhost:5005/quiz"
PRODUCT_SERVICE_URL = "http://localhost:5003"

# Sample quiz answers
SAMPLE_ANSWERS = [
    "Reading a book in a cozy nook",
    "Watching your favorite series with a snack",
    "Meditating or practicing yoga",
    "Cooking up a new recipe",
    "Upbeat pop that makes you dance",
    "Classic rock with guitar riffs",
    "Soothing classical music",
    "Jazzy tunes with a laid-back vibe",
    "A freshly brewed cup of coffee",
    "A calming cup of herbal tea",
]


def test_quiz_to_product_integration():
    """
    Test the integration between quiz-service and product-service.
    """

    # Step 1: Submit quiz answers to quiz-service
    response = requests.post(
        f"{QUIZ_SERVICE_URL}/submit-quiz/",
        json={"answers": SAMPLE_ANSWERS}
    )
    assert response.status_code == 200, f"Quiz submission failed: {response.text}"
    accordbank = response.json().get("accordbank", [])
    assert len(accordbank) > 0, "Generated accordbank is empty"

    print(f"Generated accordbank: {accordbank}")

    # Step 2: Fetch recommendations from quiz-service
    recommendations_response = requests.post(
        f"{QUIZ_SERVICE_URL}/get-recommendations/",
        json={"accordbank": accordbank}
    )
    assert recommendations_response.status_code == 200, f"Failed to get recommendations: {recommendations_response.text}"

    # Adjust: Correctly extract the recommendations list
    recommendations_dict = recommendations_response.json().get("recommendations", {})
    recommendations = recommendations_dict.get("recommendations", [])
    assert isinstance(recommendations, list), f"`recommendations` should be a list but got {type(recommendations)}"
    assert len(recommendations) > 0, "No recommendations found"

    print(f"Recommendations: {recommendations}")

    # Step 3: Validate the recommendation structure
    for recommendation in recommendations:
        assert isinstance(recommendation, dict), "Each recommendation should be a dictionary"
        assert "id" in recommendation, "Recommendation missing 'id'"
        assert "name" in recommendation, "Recommendation missing 'name'"
        assert "brand" in recommendation, "Recommendation missing 'brand'"
        assert "accords" in recommendation, "Recommendation missing 'accords'"
        assert "imageURL" in recommendation, "Recommendation missing 'imageURL'"
