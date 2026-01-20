from typing import Dict

def enrich_contact_info(profile: Dict[str, str]) -> Dict[str, str]:
    """
    Generate mock contact info.
    """
    if "email" not in profile:
        # Mock pattern: firstname.lastname@company.com
        name_parts = profile.get("name", "").lower().split()
        if len(name_parts) >= 2:
            email_local = f"{name_parts[0]}.{name_parts[-1]}"
        else:
            email_local = "info"
            
        company_domain = profile.get("company", "company").replace(" ", "").lower() + ".com"
        profile["email"] = f"{email_local}@{company_domain}"
        
    return profile
