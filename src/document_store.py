from typing import Dict, List, Tuple
import re
from collections import defaultdict

class DocumentStore:
    def __init__(self):
        self.documents: Dict[str, List[str]] = defaultdict(list)
        self.index: Dict[str, List[Tuple[str, int]]] = defaultdict(list)
        
    def add_document(self, cdp: str, content: str):
        """Add a document to the store for a specific CDP."""
        # Split content into sentences
        sentences = [s.strip() for s in re.split(r'[.!?]+', content) if s.strip()]
        self.documents[cdp].extend(sentences)
        
        # Index each word
        for idx, sentence in enumerate(sentences):
            words = set(self._tokenize(sentence.lower()))
            for word in words:
                self.index[word].append((cdp, idx))
                
    def search(self, query: str, cdp: str = None) -> List[str]:
        """Search for relevant sentences matching the query."""
        query_words = set(self._tokenize(query.lower()))
        
        # Count matches for each sentence
        scores = defaultdict(int)
        for word in query_words:
            if word in self.index:
                for doc_cdp, sent_idx in self.index[word]:
                    if cdp is None or cdp == doc_cdp:
                        scores[(doc_cdp, sent_idx)] += 1
                        
        # Sort by score
        results = []
        for (doc_cdp, sent_idx), score in sorted(scores.items(), 
                                                key=lambda x: x[1], 
                                                reverse=True)[:3]:
            if score > 1:  # At least 2 matching words
                results.append(self.documents[doc_cdp][sent_idx])
                
        return results
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple word tokenization."""
        return re.findall(r'\w+', text.lower())
