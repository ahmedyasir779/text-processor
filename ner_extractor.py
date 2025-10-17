import spacy
from typing import List, Dict, Optional
from collections import Counter


class NERExtractor:
    def __init__(self, model: str = 'en_core_web_sm'):
        """
        Initialize NER extractor
        
        Args:
            model: spaCy model to use
        """
        try:
            self.nlp = spacy.load(model)
        except OSError:
            print(f"Model '{model}' not found. Downloading...")
            import subprocess
            subprocess.run(['python', '-m', 'spacy', 'download', model])
            self.nlp = spacy.load(model)
        
        self.doc = None
        self.entities = []
    
    def extract(self, text: str) -> List[Dict]:
        """
        Extract all entities from text
        
        Args:
            text: Input text
            
        Returns:
            List of dictionaries with entity info
        """
        self.doc = self.nlp(text)
        self.entities = []
        
        for ent in self.doc.ents:
            self.entities.append({
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char
            })
        
        return self.entities
    
    def get_persons(self, text: str = None) -> List[str]:
        """
        Extract person names
        
        Args:
            text: Input text (if None, uses last extracted)
            
        Returns:
            List of person names
        """
        if text:
            self.extract(text)
        
        return [ent['text'] for ent in self.entities 
                if ent['label'] == 'PERSON']
    
    def get_organizations(self, text: str = None) -> List[str]:
        """
        Extract organization names
        
        Args:
            text: Input text (if None, uses last extracted)
            
        Returns:
            List of organization names
        """
        if text:
            self.extract(text)
        
        return [ent['text'] for ent in self.entities 
                if ent['label'] == 'ORG']
    
    def get_locations(self, text: str = None) -> List[str]:
        """
        Extract locations (countries, cities, etc.)
        
        Args:
            text: Input text (if None, uses last extracted)
            
        Returns:
            List of locations
        """
        if text:
            self.extract(text)
        
        return [ent['text'] for ent in self.entities 
                if ent['label'] == 'GPE']
    
    def get_dates(self, text: str = None) -> List[str]:
        """
        Extract dates
        
        Args:
            text: Input text (if None, uses last extracted)
            
        Returns:
            List of dates
        """
        if text:
            self.extract(text)
        
        return [ent['text'] for ent in self.entities 
                if ent['label'] == 'DATE']
    
    def get_money(self, text: str = None) -> List[str]:
        """
        Extract monetary values
        
        Args:
            text: Input text (if None, uses last extracted)
            
        Returns:
            List of money amounts
        """
        if text:
            self.extract(text)
        
        return [ent['text'] for ent in self.entities 
                if ent['label'] == 'MONEY']
    
    def get_by_label(self, label: str, text: str = None) -> List[str]:
        """
        Extract entities by specific label
        
        Args:
            label: Entity type (PERSON, ORG, GPE, etc.)
            text: Input text (if None, uses last extracted)
            
        Returns:
            List of entities matching label
        """
        if text:
            self.extract(text)
        
        return [ent['text'] for ent in self.entities 
                if ent['label'] == label]
    
    def get_entity_counts(self, text: str = None) -> Dict[str, int]:
        """
        Count entities by type
        
        Args:
            text: Input text (if None, uses last extracted)
            
        Returns:
            Dictionary mapping labels to counts
        """
        if text:
            self.extract(text)
        
        labels = [ent['label'] for ent in self.entities]
        return dict(Counter(labels))
    
    def get_summary(self, text: str = None) -> str:
        """
        Get formatted summary of extracted entities
        
        Args:
            text: Input text (if None, uses last extracted)
            
        Returns:
            Formatted summary string
        """
        if text:
            self.extract(text)
        
        summary = []
        summary.append("NAMED ENTITY RECOGNITION SUMMARY")
        summary.append("=" * 60)
        summary.append(f"\nTotal entities found: {len(self.entities)}")
        
        # Group by type
        counts = self.get_entity_counts()
        summary.append("\nEntities by type:")
        for label, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
            summary.append(f"  {label}: {count}")
        
        # Show examples
        summary.append("\nExtracted entities:")
        
        # People
        persons = self.get_persons()
        if persons:
            summary.append(f"\n   People: {', '.join(set(persons[:5]))}")
            if len(persons) > 5:
                summary.append(f"     ... and {len(persons) - 5} more")
        
        # Organizations
        orgs = self.get_organizations()
        if orgs:
            summary.append(f"\n   Organizations: {', '.join(set(orgs[:5]))}")
            if len(orgs) > 5:
                summary.append(f"     ... and {len(orgs) - 5} more")
        
        # Locations
        locations = self.get_locations()
        if locations:
            summary.append(f"\n   Locations: {', '.join(set(locations[:5]))}")
            if len(locations) > 5:
                summary.append(f"     ... and {len(locations) - 5} more")
        
        # Dates
        dates = self.get_dates()
        if dates:
            summary.append(f"\n   Dates: {', '.join(set(dates[:5]))}")
        
        # Money
        money = self.get_money()
        if money:
            summary.append(f"\n   Money: {', '.join(set(money[:3]))}")
        
        return '\n'.join(summary)
    
    def visualize(self, text: str = None, style: str = 'ent'):
        """
        Create HTML visualization of entities
        
        Args:
            text: Input text (if None, uses last extracted)
            style: Visualization style ('ent' or 'dep')
            
        Returns:
            HTML string for visualization
        """
        if text:
            self.doc = self.nlp(text)
        
        from spacy import displacy
        return displacy.render(self.doc, style=style, jupyter=False)


# ============================================
# TESTING CODE
# ============================================

if __name__ == "__main__":
    # Test text with various entities
    test_text = """
    Ahmed Yasir works as a Senior Software Engineer at Google in Riyadh, Saudi Arabia.
    He previously worked at Microsoft in Seattle from 2018 to 2020.
    
    Ahmed graduated from King Saud University in 2017 with a degree in Computer Science.
    He speaks Arabic, English, and is learning Python.
    
    Last Monday, he attended a conference at the Riyadh International Convention Center
    where he met Sarah Johnson from Amazon and Mohammed Ali from Meta.
    
    The event cost $500 per ticket and attracted over 2,000 attendees.
    Next month, Ahmed will visit San Francisco and New York City.
    
    His salary is approximately SAR 300,000 per year.
    Contact: ahmed@example.com | Phone: +966-50-123-4567
    """
    
    print("=" * 60)
    print("NAMED ENTITY RECOGNITION - TEST")
    print("=" * 60)
    
    print("\n ORIGINAL TEXT:")
    print(test_text[:200] + "...")
    
    # Initialize extractor
    extractor = NERExtractor()
    
    # Extract entities
    print("\n\n EXTRACTING ENTITIES...")
    entities = extractor.extract(test_text)
    
    print(f"\nFound {len(entities)} entities\n")
    
    # Show all entities
    print("ALL ENTITIES:")
    for ent in entities:
        print(f"  {ent['text']:30} → {ent['label']}")
    
    # Extract by type
    print("\n\n PEOPLE:")
    persons = extractor.get_persons()
    for person in set(persons):
        print(f"  - {person}")
    
    print("\n ORGANIZATIONS:")
    orgs = extractor.get_organizations()
    for org in set(orgs):
        print(f"  - {org}")
    
    print("\n LOCATIONS:")
    locations = extractor.get_locations()
    for loc in set(locations):
        print(f"  - {loc}")
    
    print("\n DATES:")
    dates = extractor.get_dates()
    for date in set(dates):
        print(f"  - {date}")
    
    print("\n MONEY:")
    money = extractor.get_money()
    for amount in money:
        print(f"  - {amount}")
    
    # Entity counts
    print("\n\n ENTITY COUNTS:")
    counts = extractor.get_entity_counts()
    for label, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {label}: {count}")
    
    # Summary
    print("\n\n" + "=" * 60)
    print("COMPLETE SUMMARY:")
    print("=" * 60)
    print(extractor.get_summary())
    
    # Save visualization
    print("\n\n Creating HTML visualization...")
    html = extractor.visualize()
    with open('output/ner_visualization.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(" Saved to output/ner_visualization.html")
    print("  Open this file in a browser to see highlighted entities!")
    
    print("\n" + "=" * 60)
    print(" ALL TESTS COMPLETE!")
    print("=" * 60)