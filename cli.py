import argparse
import sys
from pathlib import Path
from colorama import Fore, Style, init

# Initialize colorama
init()

from text_cleaner import TextCleaner
from text_processor import TextProcessor
# Assuming you have entity_extractor.py
try:
    from info_extractor import InfoExtractor as EntityExtractor
except ImportError:
    EntityExtractor = None


def print_success(msg):
    print(f"{Fore.GREEN}✓ {msg}{Style.RESET_ALL}")

def print_error(msg):
    print(f"{Fore.RED}✗ {msg}{Style.RESET_ALL}")

def print_info(msg):
    print(f"{Fore.CYAN}ℹ {msg}{Style.RESET_ALL}")

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
    elif args.text:
        text = args.text
    else:
        print_error("Please provide either --file or --text")
        sys.exit(1)
    
    print_info(f"Original text length: {len(text)} characters")
    
    # Step 1: Clean (if requested)
    if args.clean:
        print_header("STEP 1: CLEANING TEXT")
        cleaner = TextCleaner(text)
        text = (cleaner
                .remove_html_tags()
                .remove_urls()
                .remove_emails()
                .remove_special_characters()
                .normalize_whitespace()
                .to_lowercase()
                .get_cleaned_text())
        
        report = cleaner.get_report()
        print_success(f"Cleaned: {report['original_length']} → {report['final_length']} chars")
    
    # Step 2: Process (if requested)
    if args.process:
        print_header("STEP 2: PROCESSING TEXT")
        processor = TextProcessor(text)
        
        # Tokenize
        tokens = processor.tokenize_words()
        print_info(f"Tokens: {len(tokens)}")
        
        # Remove stop words
        if args.remove_stopwords:
            tokens = processor.remove_stopwords(tokens)
            print_info(f"After removing stop words: {len(tokens)}")
        
        # Lemmatize
        if args.lemmatize:
            tokens = processor.lemmatize_words(tokens)
            print_success("Applied lemmatization")
        
        # Word frequency
        if args.frequency:
            freq = processor.get_word_frequency(tokens)
            print_header("TOP 10 WORDS")
            for word, count in list(freq.items())[:10]:
                print(f"  {word}: {count}")
        
        # Extract parts of speech
        if args.extract_pos:
            print_header("EXTRACTED WORD TYPES")
            nouns = processor.extract_nouns()
            verbs = processor.extract_verbs()
            adjectives = processor.extract_adjectives()
            
            print(f"Nouns: {nouns[:10]}")
            print(f"Verbs: {verbs[:10]}")
            print(f"Adjectives: {adjectives[:10]}")
        
        # Statistics
        if args.stats:
            print_header("TEXT STATISTICS")
            stats = processor.get_statistics()
            for key, value in stats.items():
                print(f"  {key}: {value}")
    
    # Step 3: Extract entities (if requested and available)
    if args.entities and EntityExtractor:
        print_header("STEP 3: EXTRACTING ENTITIES")
        extractor = EntityExtractor(text)
        
        emails = extractor.extract_emails()
        phones = extractor.extract_phones()
        urls = extractor.extract_urls()
        
        if emails:
            print(f"Emails: {emails}")
        if phones:
            print(f"Phones: {phones}")
        if urls:
            print(f"URLs: {urls}")
    
    # Save output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print_success(f"Saved output to {args.output}")
    
    print_header("PIPELINE COMPLETE")


def main():
    parser = argparse.ArgumentParser(
        description='Text Processing Pipeline - NLP Toolkit',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Clean text file
  python cli.py --file input.txt --clean --output clean.txt
  
  # Process and analyze
  python cli.py --file input.txt --process --stats --frequency
  
  # Full pipeline
  python cli.py --file input.txt --clean --process --entities --lemmatize
        """
    )
    
    # Input options
    parser.add_argument('--file', '-f', type=str, help='Input text file')
    parser.add_argument('--text', '-t', type=str, help='Input text string')
    
    # Processing options
    parser.add_argument('--clean', '-c', action='store_true', 
                       help='Clean text (remove HTML, URLs, etc.)')
    parser.add_argument('--process', '-p', action='store_true',
                       help='Process text (tokenize, analyze)')
    parser.add_argument('--entities', '-e', action='store_true',
                       help='Extract entities (emails, phones, URLs)')
    
    # Advanced options
    parser.add_argument('--remove-stopwords', action='store_true',
                       help='Remove stop words')
    parser.add_argument('--lemmatize', action='store_true',
                       help='Apply lemmatization')
    parser.add_argument('--frequency', action='store_true',
                       help='Show word frequency')
    parser.add_argument('--extract-pos', action='store_true',
                       help='Extract nouns, verbs, adjectives')
    parser.add_argument('--stats', action='store_true',
                       help='Show text statistics')
    
    # Output
    parser.add_argument('--output', '-o', type=str,
                       help='Output file path')
    
    # Shortcut
    parser.add_argument('--all', action='store_true',
                       help='Run full pipeline (clean + process + entities)')
    
    args = parser.parse_args()
    
    # Handle --all shortcut
    if args.all:
        args.clean = True
        args.process = True
        args.entities = True
        args.frequency = True
        args.stats = True
        args.extract_pos = True
    
    try:
        process_text(args)
    except KeyboardInterrupt:
        print_error("\n\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        print_error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()