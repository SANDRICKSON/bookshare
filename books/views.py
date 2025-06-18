from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book, BorrowRequest
from .serializers import BookSerializer, BorrowRequestSerializer
from rest_framework.decorators import action

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', 'genre', 'condition', 'location']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class BorrowRequestViewSet(viewsets.ModelViewSet):
    serializer_class = BorrowRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # მფლობელს ნახოს მის წიგნებზე შემოსული მოთხოვნები, მომხმარებელს - თავისი მოთხოვნები
        if self.request.method in ['GET']:
            return BorrowRequest.objects.filter(requester=user)
        return BorrowRequest.objects.none()

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def respond(self, request, pk=None):
        borrow_request = self.get_object()
        book = borrow_request.book
        user = request.user

        # მხოლოდ მფლობელს აქვს უფლება პასუხის გაცემაზე
        if book.owner != user:
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        action = request.data.get('action')
        if action not in ['accept', 'reject']:
            return Response({"detail": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

        if borrow_request.status != 'pending':
            return Response({"detail": "Request already processed"}, status=status.HTTP_400_BAD_REQUEST)

        if action == 'accept':
            borrow_request.status = 'accepted'
            book.is_available = False
            book.save()
        else:
            borrow_request.status = 'rejected'

        borrow_request.save()
        return Response({"status": borrow_request.status})