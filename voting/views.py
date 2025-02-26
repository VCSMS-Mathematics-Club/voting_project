from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Candidate, Voter
from .serializers import CandidateSerializer

def get_client_ip(request):
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
    ip_address = request.data.get('ip_address') or get_client_ip(request)  # Use provided or real IP

    if not candidate_id:
        return Response({'error': 'Candidate ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    candidate = get_object_or_404(Candidate, id=candidate_id)

    if Voter.objects.filter(ip_address=ip_address).exists():
        return Response({'error': 'You have already voted.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Register the vote
    candidate.vote_count += 1
    candidate.save()
    Voter.objects.create(ip_address=ip_address)

    return Response({'message': 'Vote cast successfully.'}, status=status.HTTP_200_OK)
