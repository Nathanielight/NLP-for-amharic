from ethiopian_languages import EthiopianLanguageProcessor
import json
import os

def main():
    # Initialize the processor
    processor = EthiopianLanguageProcessor()
    
    # Create a directory for test files if it doesn't exist
    test_dir = "test_files"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    
    # Create a sample HTML file
    html_content = """
    <html>
        <head>
            <title>Amharic Test Document</title>
        </head>
        <body>
            <h1>የአማርኛ ምርመራ ሰነድ</h1>
            <p>ይህ የምርመራ ሰነድ ነው። በዚህ ሰነድ ውስጥ የተለያዩ የአማርኛ ቃላት አሉ።</p>
            <p>አንዳንድ ቃላት ብዙ ጊዜ ይደገማሉ። ለምሳሌ፡ ቃል፣ ሰነድ፣ እና ምርመራ።</p>
        </body>
    </html>
    """
    
    html_file = os.path.join(test_dir, "test.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # Create a sample XML file
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<document>
    <title>የአማርኛ ምርመራ ሰነድ</title>
    <content>
        <paragraph>ይህ የምርመራ ሰነድ ነው። በዚህ ሰነድ ውስጥ የተለያዩ የአማርኛ ቃላት አሉ።</paragraph>
        <paragraph>አንዳንድ ቃላት ብዙ ጊዜ ይደገማሉ። ለምሳሌ፡ ቃል፣ ሰነድ፣ እና ምርመራ።</paragraph>
    </content>
</document>"""
    
    xml_file = os.path.join(test_dir, "test.xml")
    with open(xml_file, "w", encoding="utf-8") as f:
        f.write(xml_content)
    
    # Process individual files
    print("\nProcessing HTML file:")
    html_analysis = processor.analyze_file(html_file)
    print(f"Detected language: {html_analysis['detected_language']}")
    print(f"Total words: {html_analysis['statistics']['total_words']}")
    print(f"Unique words: {html_analysis['statistics']['unique_words']}")
    print(f"Zipf's law correlation: {html_analysis['zipf_correlation']:.3f}")
    
    print("\nProcessing XML file:")
    xml_analysis = processor.analyze_file(xml_file)
    print(f"Detected language: {xml_analysis['detected_language']}")
    print(f"Total words: {xml_analysis['statistics']['total_words']}")
    print(f"Unique words: {xml_analysis['statistics']['unique_words']}")
    print(f"Zipf's law correlation: {xml_analysis['zipf_correlation']:.3f}")
    
    # Process entire directory
    print("\nProcessing entire directory:")
    directory_analysis = processor.analyze_directory(test_dir)
    
    # Save results
    results_file = "analysis_results.json"
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(directory_analysis, f, ensure_ascii=False, indent=2)
    print(f"\nAnalysis results saved to {results_file}")

if __name__ == "__main__":
    main() 