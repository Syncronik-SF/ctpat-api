from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from incidence.serializers import  IncidenceSerializer

# Create your views here.

@api_view(['POST'])
def incidence_post(request):
    if request.method == 'POST':
        serializer = IncidenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
    
    
    