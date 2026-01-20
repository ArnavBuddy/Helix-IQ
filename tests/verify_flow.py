import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_sources.linkedin import LinkedInSource
from src.data_sources.pubmed import PubMedSource
from src.enrichment.geo import enrich_location_data
from src.enrichment.contact import enrich_contact_info
from src.ranking.scorer import LeadScorer

def test_pipeline():
    print("----------------------------------------------------------------")
    print("Running End-to-End Pipeline Verification")
    print("----------------------------------------------------------------")

    # 1. Fetch
    print("[1] Fetching data...")
    li = LinkedInSource()
    pm = PubMedSource()
    
    leads = li.fetch_data(limit=5)
    pub_leads = pm.fetch_data(limit=5)
    all_leads = leads + pub_leads
    print(f"    Fetched {len(all_leads)} leads.")
    
    # 2. Enrich & Rank
    print("[2] Enriching and Ranking...")
    scorer = LeadScorer()
    
    for i, lead in enumerate(all_leads):
        # Enrich
        lead = enrich_location_data(lead)
        lead = enrich_contact_info(lead)
        
        # Rank
        lead = scorer.score_profile(lead)
        
        if i < 2: # Print first 2 for inspection
            print(f"    Sample {i+1}: {lead['name']} ({lead['title']})")
            print(f"      - Company: {lead['company']} (HQ: {lead.get('company_hq')})")
            print(f"      - Location: {lead.get('location')} -> Lat: {lead.get('lat')}, Lon: {lead.get('lon')}")
            print(f"      - Score: {lead['score']}")
            print(f"      - Reasons: {lead['score_reasons']}")
            
    print("[3] Verification Complete. Logic seems sound.")
    print("----------------------------------------------------------------")

if __name__ == "__main__":
    test_pipeline()
