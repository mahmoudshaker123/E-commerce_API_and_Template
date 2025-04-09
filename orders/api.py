from rest_framework.decorators import  api_view , permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializer
from rest_framework import status

@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def order_api(request):
    data = request.data
    serializer = OrderSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Order created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
