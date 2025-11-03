from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .services import FinancialAdvisor

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_financial_advice(request):
    """
    Get AI financial advice
    
    POST /api/ai/advice/
    Body: { "question": "How can I save more money?" }
    """
    question = request.data.get('question')
    
    if not question:
        return Response(
            {'error': 'Question is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get AI advice
    result = FinancialAdvisor.get_advice(request.user, question)
    
    if result['success']:
        return Response({
            'advice': result['advice']
        })
    else:
        return Response(
            {'error': result['error']},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )