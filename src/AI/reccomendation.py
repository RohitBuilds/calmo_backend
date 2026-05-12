from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from src.utils.setting import settings
import json

client = MistralClient(
    api_key=settings.MISTRAL_API_KEY
)

def generate_recommendations(data, prediction):

    prompt = f"""
You are an AI wellness assistant.

User Data:
- Stress Score: {prediction}
- Sleep Duration: {data.sleepDuration}
- Physical Activity Level: {data.physical_activity_level}
- Quality of Sleep: {data.quality_of_sleep}
- Heart Rate: {data.heart_rate}
- Daily Steps: {data.daily_steps}

IMPORTANT:
Return ONLY valid JSON.

Example:
{{
    "recommendations": [
        "Sleep at least 7 hours",
        "Walk daily",
        "Practice meditation"
    ],
    "motivation": "Small healthy habits improve wellness."
}}
"""

    response = client.chat(
        model="mistral-small-latest",
        messages=[
            ChatMessage(
                role="user",
                content=prompt
            )
        ]
    )

    result = response.choices[0].message.content

    print(result)

    
    cleaned_result = (
    result
    .replace("```json", "")
    .replace("```", "")
    .strip()
    )

    parsed_json = json.loads(cleaned_result)

    return parsed_json
    