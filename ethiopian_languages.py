import re
from typing import Dict, List, Tuple, Union
import langdetect
from langdetect import DetectorFactory
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import os

class EthiopianLanguageProcessor:
    def __init__(self):
        # Initialize Amharic-specific settings
        self.language_settings = {
            'am': {'name': 'Amharic', 'script': 'Ethiopic'}
        }
        
        # Amharic stop words
        self.stop_words = {
            'am': [
                'ነው', 'የ', 'እና', 'በ', 'ለ', 'እየ', 'ማድረግ', 'እንዲሁ', 'እንደ', 'ተብሎ',
                'እንቀሳቀስ', 'እንጂ', 'ወይም', 'እስከ', 'ስለ', 'እንኳን', 'ይህ', 'ነበር', 'እዚህ',
                'ይሆናል', 'ይደርሳል', 'የነው', 'ነበር', 'ያለ', 'እናቸው', 'ነበሩ', 'ብቻ', 'እርሱ'
            ]
        }
        
        # Amharic normalization rules
        self.normalization_rules = [
            (r'[ሃኀኃሐሓኻ]', 'ሀ'), (r'[ሑኁዅ]', 'ሁ'), (r'[ኂሒኺ]', 'ሂ'), (r'[ኌሔዄ]', 'ሄ'),
            (r'[ሕኅ]', 'ህ'), (r'[ኆሖኾ]', 'ሆ'), (r'[ሠ]', 'ሰ'), (r'[ዓኣዐ]', 'አ'), (r'[ዑ]', 'ኡ'),
            (r'[ዒ]', 'ኢ'), (r'[ዔ]', 'ኤ'), (r'[ዕ]', 'እ'), (r'[ዖ]', 'ኦ'), (r'[ጸ]', 'ፀ'),
            (r'[ጹ]', 'ፁ'), (r'[ጺ]', 'ፂ'), (r'[ጻ]', 'ፃ'), (r'[ጼ]', 'ፄ'), (r'[ጽ]', 'ፅ'),
            (r'[ጾ]', 'ፆ'), (r'(ሉ[ዋአ])', 'ሏ'), (r'(ሙ[ዋአ])', 'ሟ'), (r'(ቱ[ዋአ])', 'ቷ'),
            (r'(ሩ[ዋአ])', 'ሯ'), (r'(ሱ[ዋአ])', 'ሷ'), (r'(ሹ[ዋአ])', 'ሿ'), (r'(ቁ[ዋአ])', 'ቋ'),
            (r'(ቡ[ዋአ])', 'ቧ'), (r'(ቹ[ዋአ])', 'ቿ'), (r'(ሁ[ዋአ])', 'ኋ'), (r'(ኑ[ዋአ])', 'ኗ'),
            (r'(ኙ[ዋአ])', 'ኟ'), (r'(ኩ[ዋአ])', 'ኳ'), (r'(ዙ[ዋአ])', 'ዟ'), (r'(ጉ[ዋአ])', 'ጓ'),
            (r'(ደ[ዋአ])', 'ዷ'), (r'(ጡ[ዋአ])', 'ጧ'), (r'(ጩ[ዋአ])', 'ጯ'), (r'(ጹ[ዋአ])', 'ጿ'),
            (r'(ፉ[ዋአ])', 'ፏ'), (r'[ቊ]', 'ቁ'), (r'[ኵ]', 'ኩ')
        ]
        
        # Enhanced Amharic punctuation patterns
        self.punctuation_patterns = {
            'sentence_end': re.compile(r'[።፡፤፥፦፧፨]+'),  # Sentence ending marks
            'word_separator': re.compile(r'[፣፤]+'),  # Word separators
            'quotes': re.compile(r'[''"«»]+'),  # Quotes
            'parentheses': re.compile(r'[()\[\]{}]+'),  # Parentheses
            'special_chars': re.compile(r'[!@#$%^&*_+=|\\<>/?~`]+'),  # Special characters
            'numbers': re.compile(r'[0-9]+'),  # Numbers
            'spaces': re.compile(r'\s+')  # Multiple spaces
        }
        
        # Amharic prefixes to remove during stemming
        self.prefixes = [
            'የ', 'በ', 'ለ', 'እና', 'እንደ', 'እስከ', 'ስለ', 'እንኳን'
        ]
        
        # Amharic suffixes to remove during stemming
        self.suffixes = [
            'ን', 'ኝ', 'ው', 'ዎች', 'ዎቹ', 'ዎቻቸው', 'ዎቻችሁ', 'ዎቻችን',
            'ውን', 'ውም', 'ውምን', 'ውንም', 'ውምንም',
            'ዎችን', 'ዎቹን', 'ዎቻቸውን', 'ዎቻችሁን', 'ዎቻችንን',
            'ዎችም', 'ዎቹም', 'ዎቻቸውም', 'ዎቻችሁም', 'ዎቻችንም'
        ]
    
    def process_file(self, file_path: str) -> str:
        """Process a file (HTML, XML, or text) and return its content"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        file_extension = os.path.splitext(file_path)[1].lower()
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if file_extension == '.html':
            return self._process_html(content)
        elif file_extension == '.xml':
            return self._process_xml(content)
        else:
            return content
    
    def _process_html(self, html_content: str) -> str:
        """Extract text content from HTML"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Get text content
        text = soup.get_text(separator=' ', strip=True)
        return text
    
    def _process_xml(self, xml_content: str) -> str:
        """Extract text content from XML"""
        try:
            root = ET.fromstring(xml_content)
            # Extract text from all elements
            text = ' '.join(root.itertext())
            return text
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML content: {str(e)}")
    
    def process_directory(self, directory_path: str, file_extensions: List[str] = None) -> Dict[str, str]:
        """Process all files in a directory and return their contents"""
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Directory not found: {directory_path}")
            
        if file_extensions is None:
            file_extensions = ['.html', '.xml', '.txt']
            
        results = {}
        for root, _, files in os.walk(directory_path):
            for file in files:
                if any(file.endswith(ext) for ext in file_extensions):
                    file_path = os.path.join(root, file)
                    try:
                        content = self.process_file(file_path)
                        results[file_path] = content
                    except Exception as e:
                        print(f"Error processing {file_path}: {str(e)}")
                        
        return results
    
    def analyze_file(self, file_path: str) -> Dict:
        """Analyze a single file and return the results"""
        content = self.process_file(file_path)
        return self.analyze_text(content)
    
    def analyze_directory(self, directory_path: str, file_extensions: List[str] = None) -> Dict[str, Dict]:
        """Analyze all files in a directory and return the results"""
        file_contents = self.process_directory(directory_path, file_extensions)
        results = {}
        
        for file_path, content in file_contents.items():
            try:
                analysis = self.analyze_text(content)
                results[file_path] = analysis
            except Exception as e:
                print(f"Error analyzing {file_path}: {str(e)}")
                
        return results
    
    def analyze_text(self, text: str) -> Dict:
        """Analyze text and return comprehensive results"""
        # Detect language
        detected_lang = self.detect_language(text)
        
        # Process the text
        tokens = self.tokenize(text)
        
        # Analyze statistics
        stats = self.analyze_statistics(tokens)
        
        # Apply Luhn's idea
        words_to_remove, index_terms = self.apply_luhns_idea(stats['freq_rank_data'])
        
        # Remove stop words
        filtered_tokens = self.remove_stop_words(tokens, detected_lang)
        
        # Stem words
        stemmed_tokens = [self.stem_word(token, detected_lang) for token in filtered_tokens]
        
        # Calculate Zipf's law correlation
        zipf_correlation = self._calculate_zipf_correlation(stats['freq_rank_data'])
        
        return {
            'detected_language': detected_lang,
            'original_tokens': tokens,
            'filtered_tokens': filtered_tokens,
            'stemmed_tokens': stemmed_tokens,
            'words_to_remove': words_to_remove,
            'index_terms': index_terms,
            'word_frequencies': dict(stats['word_frequencies']),
            'zipf_correlation': zipf_correlation,
            'statistics': {
                'total_words': len(tokens),
                'unique_words': len(stats['word_frequencies']),
                'average_word_length': sum(len(word) for word in tokens) / len(tokens) if tokens else 0
            }
        }
    
    def _calculate_zipf_correlation(self, freq_rank_data: pd.DataFrame) -> float:
        """Calculate correlation with Zipf's law"""
        max_freq = freq_rank_data['frequency'].max()
        ranks = freq_rank_data['rank']
        zipf_freq = max_freq / ranks
        correlation = np.corrcoef(np.log(freq_rank_data['frequency']), np.log(zipf_freq))[0,1]
        return correlation
    
    def detect_language(self, text: str) -> str:
        """Detect if the text is Amharic"""
        # For Amharic, we can check if the text contains Ethiopic characters
        if re.search(r'[\u1200-\u137F]', text):
            return 'am'
        return 'unknown'
    
    def normalize_text(self, text: str) -> str:
        """Normalize Amharic text using the provided rules"""
        normalized_text = text
        for pattern, replacement in self.normalization_rules:
            normalized_text = re.sub(pattern, replacement, normalized_text)
        return normalized_text
    
    def remove_markup(self, text: str) -> str:
        """Remove HTML and other markup from text"""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove special characters but keep Amharic characters
        text = re.sub(r'[^\w\s\u1200-\u137F]', ' ', text)
        return text
    
    def preprocess_text(self, text: str) -> str:
        """Additional preprocessing steps for Amharic text"""
        # Convert to lowercase (for Latin characters)
        text = text.lower()
        
        # Remove numbers
        text = self.punctuation_patterns['numbers'].sub(' ', text)
        
        # Remove special characters
        text = self.punctuation_patterns['special_chars'].sub(' ', text)
        
        # Normalize spaces
        text = self.punctuation_patterns['spaces'].sub(' ', text)
        
        return text.strip()
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into words with proper Amharic punctuation handling"""
        # Remove markup first
        text = self.remove_markup(text)
        
        # Normalize the text
        text = self.normalize_text(text)
        
        # Additional preprocessing
        text = self.preprocess_text(text)
        
        # Handle different types of punctuation
        # Replace sentence endings with spaces
        text = self.punctuation_patterns['sentence_end'].sub(' ', text)
        # Replace word separators with spaces
        text = self.punctuation_patterns['word_separator'].sub(' ', text)
        # Remove quotes
        text = self.punctuation_patterns['quotes'].sub('', text)
        # Remove parentheses
        text = self.punctuation_patterns['parentheses'].sub('', text)
        
        # Split on whitespace and filter empty tokens
        tokens = [token.strip() for token in text.split() if token.strip()]
        
        return tokens
    
    def analyze_statistics(self, tokens: List[str]) -> Dict:
        """Analyze statistical properties of the text"""
        # Calculate word frequencies
        word_freq = Counter(tokens)
        
        # Create frequency vs rank data
        freq_rank = pd.DataFrame({
            'word': list(word_freq.keys()),
            'frequency': list(word_freq.values())
        })
        freq_rank = freq_rank.sort_values('frequency', ascending=False)
        freq_rank['rank'] = range(1, len(freq_rank) + 1)
        freq_rank['rank_freq_product'] = freq_rank['rank'] * freq_rank['frequency']
        
        return {
            'word_frequencies': word_freq,
            'freq_rank_data': freq_rank
        }
    
    def plot_frequency_rank(self, freq_rank_data: pd.DataFrame):
        """Plot frequency vs rank graph"""
        plt.figure(figsize=(10, 6))
        plt.loglog(freq_rank_data['rank'], freq_rank_data['frequency'], 'b-')
        plt.title('Frequency vs Rank (Log-Log Scale)')
        plt.xlabel('Rank')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.show()
    
    def apply_luhns_idea(self, freq_rank_data: pd.DataFrame, 
                        upper_cutoff_percentile: float = 80,
                        lower_cutoff_percentile: float = 20) -> Tuple[List[str], List[str]]:
        """Apply Luhn's idea to determine index terms"""
        # Calculate cut-off points
        upper_cutoff = np.percentile(freq_rank_data['frequency'], upper_cutoff_percentile)
        lower_cutoff = np.percentile(freq_rank_data['frequency'], lower_cutoff_percentile)
        
        # Words to remove (too frequent or too rare)
        words_to_remove = freq_rank_data[
            (freq_rank_data['frequency'] >= upper_cutoff) |
            (freq_rank_data['frequency'] <= lower_cutoff)
        ]['word'].tolist()
        
        # Words to keep for indexing
        index_terms = freq_rank_data[
            (freq_rank_data['frequency'] < upper_cutoff) &
            (freq_rank_data['frequency'] > lower_cutoff)
        ]['word'].tolist()
        
        return words_to_remove, index_terms
    
    def remove_stop_words(self, tokens: List[str], language: str) -> List[str]:
        """Remove stop words from tokens"""
        if language in self.stop_words:
            return [token for token in tokens if token not in self.stop_words[language]]
        return tokens
    
    def stem_word(self, word: str, language: str) -> str:
        """Stem Amharic words"""
        if language != 'am':
            return word
            
        stemmed = word
        
        # Remove prefixes
        for prefix in self.prefixes:
            if stemmed.startswith(prefix):
                stemmed = stemmed[len(prefix):]
                break
        
        # Remove suffixes
        for suffix in self.suffixes:
            if stemmed.endswith(suffix):
                stemmed = stemmed[:-len(suffix)]
                break
        
        return stemmed 