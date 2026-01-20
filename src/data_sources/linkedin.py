import random
from typing import List, Dict, Any
from faker import Faker
from .base import DataSource
from src.data_sources.mock_data import CITY_COORDINATES, COMPANY_HQS, LINKEDIN_TITLES

fake = Faker()

class LinkedInSource(DataSource):
    """Mock LinkedIn Data Source generating synthetic profiles."""
    
    def fetch_data(self, query: str = None, limit: int = 20, **kwargs) -> List[Dict[str, Any]]:
        """
        Generate synthetic LinkedIn profiles.
        """
        results = []
        titles = LINKEDIN_TITLES
        
        companies = list(COMPANY_HQS.keys())
        
        locations = list(CITY_COORDINATES.keys())

        for _ in range(limit):
            profile = {
                "id": fake.uuid4(),
                "name": fake.name(),
                "title": random.choice(titles),
                "company": random.choice(companies),
                "location": random.choice(locations),
                "linkedin_url": f"https://linkedin.com/in/{fake.user_name()}",
                "summary": fake.text(max_nb_chars=100),
                "source": "LinkedIn"
            }
            results.append(profile)
            
        return results
