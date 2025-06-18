from rest_framework import serializers
from .models import Book, BorrowRequest
from core.models import Author, Genre, Condition, Location

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['owner', 'created_at', 'is_available']

class BorrowRequestSerializer(serializers.ModelSerializer):
    requester = serializers.ReadOnlyField(source='requester.email')
    book_title = serializers.ReadOnlyField(source='book.title')

    class Meta:
        model = BorrowRequest
        fields = ['id', 'book', 'book_title', 'requester', 'requested_at', 'status']
        read_only_fields = ['status', 'requested_at', 'requester']