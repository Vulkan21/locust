"""Data generation utilities for load testing"""
import random
import string
from typing import List, Dict, Any


class DataGenerator:
    """Generate realistic test data for glossary terms"""
    
    TERM_CATEGORIES = {
        'tech': ['API', 'Database', 'Framework', 'Algorithm', 'Protocol'],
        'business': ['Revenue', 'Strategy', 'Stakeholder', 'ROI', 'KPI'],
        'science': ['Hypothesis', 'Experiment', 'Variable', 'Control', 'Analysis'],
    }
    
    DESCRIPTION_TEMPLATES = [
        "A comprehensive definition of {term} in the context of {context}.",
        "{term} is a fundamental concept that describes {context}.",
        "Understanding {term} is crucial for mastering {context}.",
        "In {context}, {term} refers to a specific methodology or approach.",
        "{term} represents an important aspect of {context} systems.",
    ]
    
    SOURCES = [
        "Wikipedia",
        "Academic Paper",
        "Industry Standard",
        "Internal Documentation",
        "Expert Interview",
        "Technical Specification",
        "Best Practices Guide",
    ]
    
    RELATION_TYPES = [
        "related_to",
        "subclass_of",
        "uses",
        "part_of",
        "depends_on",
        "alternative_to",
    ]
    
    @staticmethod
    def generate_term_name(prefix: str = "LoadTest", include_random: bool = True) -> str:
        """Generate a unique term name"""
        if include_random:
            random_id = random.randint(10000, 99999)
            return f"{prefix}_Term_{random_id}"
        else:
            category = random.choice(list(DataGenerator.TERM_CATEGORIES.keys()))
            base_term = random.choice(DataGenerator.TERM_CATEGORIES[category])
            suffix = ''.join(random.choices(string.ascii_uppercase, k=3))
            return f"{base_term}_{suffix}"
    
    @staticmethod
    def generate_description(term: str, context: str = None) -> str:
        """Generate a realistic description for a term"""
        if context is None:
            context = random.choice([
                "software development",
                "data science",
                "business management",
                "system architecture",
                "quality assurance",
            ])
        
        template = random.choice(DataGenerator.DESCRIPTION_TEMPLATES)
        description = template.format(term=term, context=context)
        
        if random.random() > 0.5:
            details = [
                f" It involves multiple components and requires careful consideration.",
                f" This concept has been widely adopted in modern practices.",
                f" Key characteristics include precision, efficiency, and scalability.",
                f" Historical context dates back to early industry developments.",
            ]
            description += random.choice(details)
        
        return description
    
    @staticmethod
    def generate_sources(count: int = None) -> List[str]:
        """Generate a list of source references"""
        if count is None:
            count = random.randint(1, 3)
        return random.sample(DataGenerator.SOURCES, min(count, len(DataGenerator.SOURCES)))
    
    @staticmethod
    def generate_term_payload(term: str = None, prefix: str = "LoadTest") -> Dict[str, Any]:
        """Generate a complete term payload for API requests"""
        if term is None:
            term_name = DataGenerator.generate_term_name(prefix)
        else:
            term_name = term
        
        term_id = term_name.lower().replace(" ", "_").replace("(", "").replace(")", "")
        
        return {
            "id": term_id,
            "term": term_name,
            "definition": DataGenerator.generate_description(term_name),
            "category": random.choice(["API", "Architecture", "Performance", "Tools"]),
            "source": ", ".join(DataGenerator.generate_sources()),
            "related_terms": []
        }
    
    @staticmethod
    def generate_search_query() -> str:
        """Generate realistic search queries"""
        queries = [
            "test",
            "load",
            "API",
            "data",
            "system",
            "process",
            "management",
            "development",
            random.choice(string.ascii_lowercase) * 2,  
        ]
        return random.choice(queries)
    
    @staticmethod
    def generate_relation_type() -> str:
        """Get a random relation type"""
        return random.choice(DataGenerator.RELATION_TYPES)
    
    @staticmethod
    def generate_search_params() -> Dict[str, Any]:
        """Generate realistic search parameters"""
        return {
            "q": DataGenerator.generate_search_query(),
            "limit": random.choice([5, 10, 20, 50]),
            "offset": random.choice([0, 0, 0, 10, 20]),  
        }

