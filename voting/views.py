from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Candidate, Voter
from .serializers import CandidateSerializer

def get_client_ip(request):
    # If behind a proxy, you might use HTTP_X_FORWARDED_FOR
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@api_view(['GET'])
def candidate_list(request):
    candidates = Candidate.objects.all().order_by('id')
    serializer = CandidateSerializer(candidates, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def cast_vote(request):
    candidate_id = request.data.get('candidate_id')
    if candidate_id is None:
        return Response({'error': 'Candidate ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        candidate = Candidate.objects.get(id=candidate_id)
    except Candidate.DoesNotExist:
        return Response({'error': 'Candidate not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    client_ip = get_client_ip(request)
    if Voter.objects.filter(ip_address=client_ip).exists():
        return Response({'error': 'You have already voted.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Register vote
    candidate.vote_count += 1
    candidate.save()
    Voter.objects.create(ip_address=client_ip)
    
    return Response({'message': 'Vote cast successfully.'}, status=status.HTTP_200_OK)
