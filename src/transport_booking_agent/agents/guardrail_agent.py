from typing import Dict, Any

class GuardrailAgent:
    def check_guardrails(self, message: str, user_profile: Dict[str, Any]) -> bool:
        """
        Checks the user message and profile against a set of guardrails.
        
        For now, this is a dummy implementation.
        """
        print(f"Checking guardrails for message: '{message}'")
        
        # Dummy guardrail: check for profanity
        if "badword" in message.lower():
            print("Guardrail failed: Profanity detected.")
            return False
            
        # Dummy guardrail: check if user is on a blocklist
        if user_profile.get("is_blocked", False):
            print("Guardrail failed: User is blocked.")
            return False
            
        print("Guardrails passed.")
        return True