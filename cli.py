"""
Text Processing Pipeline - Command Line Interface
Combines all Week 2 modules into one professional NLP toolkit
"""

import argparse
import sys
from pathlib import Path
from colorama import Fore, Style, init

# Initialize colorama
init()

from text_cleaner import TextCleaner
from text_processor import TextProcessor
from info_extractor import InfoExtractor
from ner_extractor import NERExtractor


def print_success(msg):
    print(f"{Fore.GREEN}✓ {msg}{Style.RESET_ALL}")

def print_error(msg):
    print(f"{Fore.RED}✗ {msg}{Style.RESET_ALL}")

def print_info(msg):
    print(f"{Fore.CYAN}ℹ {msg}{Style.RESET_ALL}")

def print_warning(msg):
    print(f"{Fore.YELLOW}⚠ {msg}{Style.RESET_ALL}")

def print_header(msg):
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{msg}")
    print(f"{'='*60}{Style.RESET_ALL}\n")


def process_text(args):
    """Main text processing pipeline"""
    
    # Read input
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
            print_success(f"Loaded text from {args.file}")
        except FileNotFoundError:
            print_error(f"File not found: {args.file}")
            sys.exit(1)
        except Exception as e:
            print_error(f"Error reading file: {e}")
            sys.exit(1)
    elif args.text:
        text = args.text
    else:
        print_error("Please provide either --file or --text")
        print_info("Usage: python cli.py --file input.txt --all")
        sys.exit(1)
    
    print_info(f"Original text: {len(text)} characters, {len(text.split())} words")
    
    # Store original for comparison
    original_text = text
    
    # Step 1: Clean (if requested)
    if args.clean:
        print_header("STEP 1: CLEANING TEXT")
        cleaner = TextCleaner(text)
        text = (cleaner
                .remove_html_tags()
                .remove_urls()
                .remove_emails()
                .remove_phone_numbers()
                .remove_special_characters()
                .normalize_unicode()
                .normalize_whitespace()
                .get_cleaned_text())
        
        if args.lowercase:
            text = text.lower()
        
        report = cleaner.get_report()
        print_success(f"Cleaned: {report['original_length']} → {report['final_length']} chars")
        print_info(f"Removed {report['chars_removed']} characters")
    
    # Step 2: Process (if requested)
    if args.process:
        print_header("STEP 2: LINGUISTIC PROCESSING")
        processor = TextProcessor(text)
        
        # Tokenize
        tokens = processor.tokenize_words()
        print_info(f"Tokenized: {len(tokens)} tokens")
        
        # Remove stop words
        if args.remove_stopwords:
            filtered_tokens = processor.remove_stopwords(tokens)
            print_info(f"After removing stop words: {len(filtered_tokens)} tokens")
            tokens = filtered_tokens
        
        # Lemmatize
        if args.lemmatize:
            lemmatized = processor.lemmatize_words(tokens)
            print_success(f"Applied lemmatization to {len(lemmatized)} tokens")
            tokens = lemmatized
        
        # Word frequency
        if args.frequency:
            freq = processor.get_word_frequency(tokens)
            print_header("TOP 10 MOST COMMON WORDS")
            for i, (word, count) in enumerate(list(freq.items())[:10], 1):
                print(f"  {i}. {word}: {count}")
        
        # Extract parts of speech
        if args.extract_pos:
            print_header("EXTRACTED WORD TYPES")
            nouns = processor.extract_nouns()
            verbs = processor.extract_verbs()
            adjectives = processor.extract_adjectives()
            
            if nouns:
                print(f"📦 Nouns ({len(nouns)}): {', '.join(list(set(nouns))[:10])}")
            if verbs:
                print(f"⚡ Verbs ({len(verbs)}): {', '.join(list(set(verbs))[:10])}")
            if adjectives:
                print(f"✨ Adjectives ({len(adjectives)}): {', '.join(list(set(adjectives))[:10])}")
        
        # Statistics
        if args.stats:
            print_header("TEXT STATISTICS")
            stats = processor.get_statistics()
            print(f"📊 Total characters: {stats['total_characters']}")
            print(f"📝 Total words: {stats['total_words']}")
            print(f"🔤 Unique words: {stats['unique_words']}")
            print(f"📄 Total sentences: {stats['total_sentences']}")
            print(f"📏 Avg word length: {stats['avg_word_length']}")
            print(f"📐 Avg sentence length: {stats['avg_sentence_length']:.1f} words")
            print(f"🎯 Lexical diversity: {stats['lexical_diversity']:.2%}")
    
    # Step 3: Extract structured info (if requested)
    if args.extract_info:
        print_header("STEP 3: INFORMATION EXTRACTION (Pattern-Based)")
        info_extractor = InfoExtractor(original_text)  # Use original, not cleaned
        
        all_info = info_extractor.extract_all()
        
        found_any = False
        for info_type, items in all_info.items():
            if items:
                found_any = True
                print(f"\n📌 {info_type.upper().replace('_', ' ')} ({len(items)}):")
                for item in items[:5]:
                    print(f"   • {item}")
                if len(items) > 5:
                    print(f"   ... and {len(items) - 5} more")
        
        if not found_any:
            print_warning("No structured information found (emails, phones, URLs, etc.)")
    
    # Step 4: Named Entity Recognition (if requested)
    if args.extract_entities:
        print_header("STEP 4: NAMED ENTITY RECOGNITION (AI-Based)")
        
        try:
            ner = NERExtractor()
            entities = ner.extract(original_text)  # Use original text
            
            if entities:
                print_success(f"Found {len(entities)} named entities")
                
                # Show by category
                persons = ner.get_persons()
                if persons:
                    print(f"\n👤 People ({len(persons)}): {', '.join(list(set(persons))[:5])}")
                
                orgs = ner.get_organizations()
                if orgs:
                    print(f"🏢 Organizations ({len(orgs)}): {', '.join(list(set(orgs))[:5])}")
                
                locations = ner.get_locations()
                if locations:
                    print(f"📍 Locations ({len(locations)}): {', '.join(list(set(locations))[:5])}")
                
                dates = ner.get_dates()
                if dates:
                    print(f"📅 Dates ({len(dates)}): {', '.join(list(set(dates))[:3])}")
                
                money = ner.get_money()
                if money:
                    print(f"💰 Money ({len(money)}): {', '.join(money[:3])}")
                
                # Save visualization if requested
                if args.visualize:
                    output_dir = Path(args.output).parent if args.output else Path('output')
                    output_dir.mkdir(exist_ok=True)
                    
                    html_path = output_dir / 'ner_visualization.html'
                    html = ner.visualize(original_text)
                    
                    with open(html_path, 'w', encoding='utf-8') as f:
                        f.write(html)
                    
                    print_success(f"Saved NER visualization to {html_path}")
                    print_info("Open this file in a browser to see highlighted entities")
            else:
                print_warning("No named entities found")
                
        except Exception as e:
            print_error(f"NER extraction failed: {e}")
            print_info("Make sure spaCy model is installed: python -m spacy download en_core_web_sm")
    
    # Save output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print_success(f"Saved processed text to {output_path}")
    
    print_header("✓ PIPELINE COMPLETE")


def main():
    parser = argparse.ArgumentParser(
        description='Text Processing Pipeline - Professional NLP Toolkit',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Clean text file
  python cli.py --file input.txt --clean --output clean.txt
  
  # Process and analyze
  python cli.py --file input.txt --process --stats --frequency
  
  # Extract structured info (emails, phones, URLs, dates, etc.)
  python cli.py --file input.txt --extract-info
  
  # Named entity recognition (people, organizations, locations)
  python cli.py --file input.txt --extract-entities --visualize
  
  # Full pipeline
  python cli.py --file input.txt --all
  
  # Quick analysis
  python cli.py --text "Apple Inc. is located in Cupertino. Contact: info@apple.com" --all
        """
    )
    
    # Input options
    parser.add_argument('--file', '-f', type=str, help='Input text file')
    parser.add_argument('--text', '-t', type=str, help='Input text string')
    
    # Processing stages
    parser.add_argument('--clean', '-c', action='store_true', 
                       help='Clean text (remove HTML, URLs, special chars, etc.)')
    parser.add_argument('--process', '-p', action='store_true',
                       help='Process text (tokenize, lemmatize, analyze)')
    parser.add_argument('--extract-info', action='store_true',
                       help='Extract structured info (emails, phones, URLs, dates, currency)')
    parser.add_argument('--extract-entities', '-e', action='store_true',
                       help='Extract named entities (people, orgs, locations) using AI')
    
    # Processing options
    parser.add_argument('--lowercase', action='store_true',
                       help='Convert to lowercase')
    parser.add_argument('--remove-stopwords', action='store_true',
                       help='Remove stop words (the, a, is, etc.)')
    parser.add_argument('--lemmatize', action='store_true',
                       help='Apply lemmatization (better→good, running→run)')
    parser.add_argument('--frequency', action='store_true',
                       help='Show word frequency analysis')
    parser.add_argument('--extract-pos', action='store_true',
                       help='Extract nouns, verbs, adjectives')
    parser.add_argument('--stats', action='store_true',
                       help='Show text statistics')
    parser.add_argument('--visualize', action='store_true',
                       help='Create HTML visualization of entities')
    
    # Output
    parser.add_argument('--output', '-o', type=str,
                       help='Output file path for processed text')
    
    # Shortcuts
    parser.add_argument('--all', action='store_true',
                       help='Run complete pipeline (all stages enabled)')
    
    args = parser.parse_args()
    
    # Handle --all shortcut
    if args.all:
        args.clean = True
        args.process = True
        args.extract_info = True
        args.extract_entities = True
        args.frequency = True
        args.stats = True
        args.extract_pos = True
        args.lemmatize = True
        args.remove_stopwords = True
        args.visualize = True
    
    # Show help if no arguments
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    
    try:
        process_text(args)
    except KeyboardInterrupt:
        print_warning("\n\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()