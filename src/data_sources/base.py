from abc import ABC, abstractmethod
import pandas as pd
from typing import List, Dict, Any

class DataSource(ABC):
    """Abstract base class for all data sources."""
    
    @abstractmethod
    def fetch_data(self, query: str = None, **kwargs) -> List[Dict[str, Any]]:
        """
        Fetch data from the source.
        
        Args:
            query: Search term or keyword.
            kwargs: Additional arguments.
            
        Returns:
            List of dictionaries containing the data.
        """
        pass

    def normalize(self, data: List[Dict[str, Any]]) -> pd.DataFrame:
        """Convert list of dicts to DataFrame."""
        return pd.DataFrame(data)
