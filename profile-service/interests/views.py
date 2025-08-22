from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Interest
from .serializers import InterestSerializer, InterestListSerializer


class InterestViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Interest model - Read-only operations"""
    
    queryset = Interest.objects.filter(is_active=True)
    serializer_class = InterestListSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to view interests
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return InterestSerializer
        return InterestListSerializer
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get all available interest categories"""
        categories = dict(Interest.INTEREST_CATEGORIES)
        return Response({
            'categories': categories,
            'count': len(categories)
        })
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search interests by name or category"""
        query = request.query_params.get('q', '')
        category = request.query_params.get('category', '')
        
        queryset = self.queryset
        
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query)
            )
        
        if category:
            queryset = queryset.filter(category=category)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'results': serializer.data,
            'count': queryset.count(),
            'query': query,
            'category': category
        })
