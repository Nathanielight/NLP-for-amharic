from django.db import models
import json

class AnalyzedDocument(models.Model):
    DOCUMENT_TYPES = [
        ('txt', 'Text File'),
        ('html', 'HTML File'),
        ('xml', 'XML File'),
    ]
    
    title = models.CharField(max_length=200)
    document = models.FileField(upload_to='documents/')
    document_type = models.CharField(max_length=4, choices=DOCUMENT_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    analysis_results = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    @property
    def word_count(self):
        if self.analysis_results:
            return self.analysis_results.get('statistics', {}).get('total_words', 0)
        return 0
    
    @property
    def unique_words(self):
        if self.analysis_results:
            return self.analysis_results.get('statistics', {}).get('unique_words', 0)
        return 0
    
    @property
    def language(self):
        if self.analysis_results:
            return self.analysis_results.get('detected_language', 'unknown')
        return 'unknown'
    
    @property
    def zipf_correlation(self):
        if self.analysis_results:
            return round(self.analysis_results.get('zipf_correlation', 0), 3)
        return 0
