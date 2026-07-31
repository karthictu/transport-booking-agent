from typing import Dict, Any

class UserProfileAgent:
    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        # Dummy implementation for now.
        # This will be replaced with actual user profile management later.
        print(f"Retrieving profile for user: {user_id}")
        return {
            "user_id": user_id,
            "preferences": ["cheapest", "window seat"],
            "past_trips": [],
            "personal_info": {"name": "John Doe", "email": "john.doe@example.com"}
        }
