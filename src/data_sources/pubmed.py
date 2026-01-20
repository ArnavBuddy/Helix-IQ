import random
from typing import List, Dict, Any
from faker import Faker
from .base import DataSource
from src.data_sources.mock_data import CITY_COORDINATES, ACADEMIC_INSTITUTES, PUBMED_TITLES

fake = Faker()

class PubMedSource(DataSource):
    """Mock PubMed Data Source generating synthetic papers."""
    
    def fetch_data(self, query: str = None, limit: int = 10, **kwargs) -> List[Dict[str, Any]]:
        """
        Generate synthetic PubMed papers (authors).
        """
        results = []
        keywords = [
            "Drug-Induced Liver Injury", 
            "3D cell culture", 
            "Organ-on-chip", 
            "Hepatic spheroids", 
            "Investigative Toxicology"
        ]
        
        for _ in range(limit):
            keyword = random.choice(keywords)
            author = {
                "id": fake.uuid4(),
                "name": fake.name(),
                "title": random.choice(PUBMED_TITLES), # Academic titles
                "company": random.choice(list(ACADEMIC_INSTITUTES.keys())), # Academic affiliation
                "location": random.choice(list(CITY_COORDINATES.keys())), # Key hubs
                "paper_title": f"Novel approaches in {keyword}: {fake.sentence()}",
                "publication_date": fake.date_between(start_date='-2y', end_date='today').isoformat(),
                "source": "PubMed"
            }
            results.append(author)
            
        return results
