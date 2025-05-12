from .views import visualize_analysis

urlpatterns = [
    # ... existing URL patterns ...
    path('visualize/<int:document_id>/', visualize_analysis, name='visualize_analysis'),
] 