from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BorrowRequestViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'borrow-requests', BorrowRequestViewSet, basename='borrowrequest')

urlpatterns = router.urls
