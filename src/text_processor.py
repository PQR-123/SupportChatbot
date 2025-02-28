import re
from typing import Tuple, Optional

class TextProcessor:
    CDP_KEYWORDS = {
        'segment', 'mparticle', 'lytics', 'zeotap',
        'cdp', 'customer data platform'
    }
    
    HOW_TO_PATTERNS = [
        r'how (do|can|to|should) (i|we|you)',
        r'what( is|\'s)? (the )?(best )?(way|method) to',
        r'guide (me|us) (through|on)',
    ]
    
    def __init__(self):
        self.patterns = [re.compile(pattern, re.IGNORECASE) 
                        for pattern in self.HOW_TO_PATTERNS]
    
    def validate_question(self, text: str) -> Tuple[bool, str]:
        """Validate if the question is CDP-related and how-to format."""
        # Check if empty or too short
        if not text or len(text.strip()) < 10:
            return False, "Please ask a complete question."
            
        # Check if it's a how-to question
        is_how_to = any(pattern.search(text) for pattern in self.patterns)
        if not is_how_to:
            return False, "Please ask a 'how-to' question."
            
        # Check if CDP-related
        words = set(re.findall(r'\w+', text.lower()))
        if not words.intersection(self.CDP_KEYWORDS):
            return False, "Please ask a question related to CDP platforms."
            
        return True, ""
        
    def extract_cdp(self, text: str) -> Optional[str]:
        """Extract mentioned CDP platform from text."""
        text_lower = text.lower()
        
        if 'segment' in text_lower:
            return 'segment'
        elif 'mparticle' in text_lower:
            return 'mparticle'
        elif 'lytics' in text_lower:
            return 'lytics'
        elif 'zeotap' in text_lower:
            return 'zeotap'
            
        return None
