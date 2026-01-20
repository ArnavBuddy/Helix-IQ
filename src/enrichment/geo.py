from typing import Dict
from src.data_sources.mock_data import CITY_COORDINATES, COMPANY_HQS

def enrich_location_data(profile: Dict[str, str]) -> Dict[str, str]:
    """
    Enrich profile with location analysis (Remote vs HQ).
    For mock purposes, we define some known HQs.
    """
    
    # Mock Company HQs are imported from mock_data
    
    person_loc = profile.get("location", "")
    company = profile.get("company", "")
    hq_loc = COMPANY_HQS.get(company, "Unknown HQ")
    
    profile["company_hq"] = hq_loc
    
    # Simple string check for "Remote" or mismatch
    is_remote = False
    
    if "Remote" in person_loc:
        is_remote = True
    elif hq_loc != "Unknown HQ" and person_loc.split(',')[0] not in hq_loc:
        is_remote = True
        
    profile["is_remote"] = is_remote
    profile["location_details"] = f"{person_loc} (HQ: {hq_loc})" if is_remote else person_loc
    
    # Inject Coordinates for Map
    coords = CITY_COORDINATES.get(person_loc, [0, 0])
    # Add small random jitter to separate points visually if they are identical
    import random
    if coords != [0, 0]:
       profile["lat"] = coords[0] + random.uniform(-0.01, 0.01)
       profile["lon"] = coords[1] + random.uniform(-0.01, 0.01)
    else:
       # Default fallback or skip
       profile["lat"] = None
       profile["lon"] = None
       
    return profile
