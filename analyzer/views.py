from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import DocumentForm
from .models import AnalyzedDocument
from ethiopian_languages import EthiopianLanguageProcessor
import os

def home(request):
    documents = AnalyzedDocument.objects.all().order_by('-uploaded_at')
    return render(request, 'analyzer/home.html', {'documents': documents})

def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            
            # Process the uploaded file
            processor = EthiopianLanguageProcessor()
            try:
                analysis = processor.analyze_file(document.document.path)
                document.analysis_results = analysis
                document.save()
                messages.success(request, 'Document uploaded and analyzed successfully!')
            except Exception as e:
                messages.error(request, f'Error analyzing document: {str(e)}')
            
            return redirect('document_detail', pk=document.pk)
    else:
        form = DocumentForm()
    
    return render(request, 'analyzer/upload.html', {'form': form})

def document_detail(request, pk):
    document = get_object_or_404(AnalyzedDocument, pk=pk)
    return render(request, 'analyzer/document_detail.html', {'document': document})

def visualize_analysis(request, document_id):
    """
    View to visualize the tokenization, normalization, stemming, and index words.
    """
    # Retrieve the document from the database
    document = AnalyzedDocument.objects.get(id=document_id)
    
    # For demonstration, we'll use dummy data. In a real scenario, you would process the document's content.
    tokens = ["word1", "word2", "word3", "word4", "word5"]
    normalized_tokens = ["normalized1", "normalized2", "normalized3", "normalized4", "normalized5"]
    stemmed_tokens = ["stemmed1", "stemmed2", "stemmed3", "stemmed4", "stemmed5"]
    index_words = ["index1", "index2", "index3"]
    
    context = {
        'document': document,
        'tokens': tokens,
        'normalized_tokens': normalized_tokens,
        'stemmed_tokens': stemmed_tokens,
        'index_words': index_words
    }
    
    return render(request, 'analyzer/visualize_analysis.html', context)
