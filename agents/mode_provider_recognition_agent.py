from typing import Tuple, Optional, Dict, Any

class ModeProviderRecognitionAgent:
    def recognize(self, message: str, user_profile: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
        """
        Recognizes the transport mode and provider from the user message.
        
        For now, this is a dummy implementation.
        It also attempts to prefill provider from user_profile if not explicitly mentioned.
        """
        print(f"Recognizing mode and provider from message: '{message}'")
        
        message_lower = message.lower()
        
        mode = None
        provider = None
        
        if "flight" in message_lower or "fly" in message_lower:
            mode = "flight"
            if "united" in message_lower:
                provider = "United Airlines"
            elif "delta" in message_lower:
                provider = "Delta"
            # Attempt to prefill from user profile if not found in message
            if not provider and mode and user_profile.get("preferred_providers", {}).get(mode):
                provider = user_profile["preferred_providers"][mode]
        elif "train" in message_lower:
            mode = "train"
            if "amtrak" in message_lower:
                provider = "Amtrak"
            # Attempt to prefill from user profile if not found in message
            if not provider and mode and user_profile.get("preferred_providers", {}).get(mode):
                provider = user_profile["preferred_providers"][mode]
        elif "bus" in message_lower:
            mode = "bus"
            # Attempt to prefill from user profile if not found in message
            if not provider and mode and user_profile.get("preferred_providers", {}).get(mode):
                provider = user_profile["preferred_providers"][mode]
            
        print(f"Recognized mode: {mode}, provider: {provider}")
        return mode, provider
