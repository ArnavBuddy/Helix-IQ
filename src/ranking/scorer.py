from typing import Dict

class LeadScorer:
    """
    The Probability Engine: Assigns scores to leads based on weighted signals.
    """
    
    WEIGHTS = {
        "role_fit": 30,
        "company_intent": 20,
        "technographic": 15,
        "location": 10,
        "scientific_intent": 40
    }
    
    HUBS = ["Boston", "Cambridge", "San Francisco", "Bay Area", "Basel", "London", "Oxford"]
    
    HIGH_INTENT_ROLES = ["Toxicology", "Safety", "Hepatic", "3D", "Liver", "Preclinical"]
    MEDIUM_INTENT_ROLES = ["Scientist", "Investigator"]
    
    def score_profile(self, profile: Dict[str, str]) -> Dict[str, str]:
        """
        Calculate the Propensity to Buy score (0-100).
        """
        score = 0
        reasons = []
        
        title = profile.get("title", "")
        company = profile.get("company", "")
        location = profile.get("location", "")
        source = profile.get("source", "")
        
        # 1. Role Fit (+30)
        # Check for high intent keywords
        if any(keyword.lower() in title.lower() for keyword in self.HIGH_INTENT_ROLES):
            score += self.WEIGHTS["role_fit"]
            reasons.append(f"Role Fit: '{title}' matches key terms (+30)")
        elif any(keyword.lower() in title.lower() for keyword in self.MEDIUM_INTENT_ROLES):
            score += 15 # Partial credit
            reasons.append(f"Role Fit: '{title}' is relevant (+15)")
            
        # 2. Scientific Intent (+40)
        # If source is PubMed or they have recent papers (mocked via source for now)
        if source == "PubMed":
            score += self.WEIGHTS["scientific_intent"]
            reasons.append("Scientific Intent: Recent Publication (+40)")
        # For LinkedIn profiles, we might simulate checking a database
        elif profile.get("has_recent_paper", False):
             score += self.WEIGHTS["scientific_intent"]
             reasons.append("Scientific Intent: Recent Publication (+40)")

        # 3. Company Intent (+20)
        # Mocking funding data
        funded_companies = ["StartUp Bio", "Moderna", "BioTech Inc"]
        if company in funded_companies:
            score += self.WEIGHTS["company_intent"]
            reasons.append(f"Company Intent: {company} recently funded (+20)")
            
        # 4. Location (+10)
        if any(hub.lower() in location.lower() for hub in self.HUBS):
            score += self.WEIGHTS["location"]
            reasons.append(f"Location: Located in hub '{location}' (+10)")
        elif any(hub.lower() in profile.get("company_hq", "").lower() for hub in self.HUBS):
            score += 5 # Partial for HQ being in hub
            reasons.append(f"Location: HQ in hub (+5)")

        # 5. Technographic (+15)
        # Mocking tech stack
        tech_companies = ["Roche", "Novartis", "Genentech"]
        if company in tech_companies:
             score += self.WEIGHTS["technographic"]
             reasons.append("Technographic: Uses similar tech (+15)")

        # Cap at 100
        score = min(score, 100)
        
        profile["score"] = score
        profile["score_reasons"] = "; ".join(reasons)
        
        return profile
