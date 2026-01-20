# Shared constants for mock data generation

CITY_COORDINATES = {
    "New York, NY": [40.7128, -74.0060],
    "Boston, MA": [42.3601, -71.0589],
    "Cambridge, MA": [42.3736, -71.1097],
    "San Francisco, CA": [37.7749, -122.4194],
    "South San Francisco, CA": [37.6547, -122.4077],
    "San Diego, CA": [32.7157, -117.1611],
    "Basel, Switzerland": [47.5596, 7.5886],
    "London, UK": [51.5074, -0.1278],
    "Durham, NC": [35.9940, -78.8986],
    "Remote, TX": [31.9686, -99.9018], # Central TX approx
}

# Pharma/Biotech Companies
COMPANY_HQS = {
    "Pfizer": "New York, NY",
    "Novartis": "Basel, Switzerland",
    "Roche": "Basel, Switzerland", 
    "StartUp Bio": "Cambridge, MA",
    "Genentech": "South San Francisco, CA", 
    "Vertex": "Boston, MA", 
    "Moderna": "Cambridge, MA", 
    "BioTech Inc": "San Diego, CA",
    "University of Boston": "Boston, MA"
}

# Academic Institutes for PubMed
ACADEMIC_INSTITUTES = {
    "Harvard Medical School": "Boston, MA",
    "MIT": "Cambridge, MA",
    "UCSF": "San Francisco, CA",
    "Stanford University": "San Francisco, CA", # Generic mapping
    "Broad Institute": "Cambridge, MA",
    "Dana-Farber Cancer Institute": "Boston, MA",
    "UCSD": "San Diego, CA",
    "Francis Crick Institute": "London, UK"
}

LINKEDIN_TITLES = [
    "Director of Toxicology", 
    "Head of Preclinical Safety", 
    "VP Drug Safety", 
    "Senior Scientist, Liver Toxicity",
    "Principal Investigator",
    "Research Scientist"
]

PUBMED_TITLES = [
    "Professor",
    "Postdoctoral Fellow",
    "PhD Candidate",
    "Research Associate",
    "Principal Investigator"
]
