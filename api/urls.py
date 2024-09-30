from django.urls import path
from api import views

#....router with ViewSet......


from rest_framework.routers import DefaultRouter

router=DefaultRouter()                                                           #create instance of DefaultRouter class          

router.register('v1/books',views.BookViewSetView,basename='books')               #calling register() method (this is registering viewset)
                                                                                 ##This will generate the appropriate URL routes for ViewSet.

router.register('v1/reviews',views.ReviewUpdateDestroyViewSet,basename='reviews')




urlpatterns = [
    
    path('book/',views.BookListCreateView.as_view()),
    path('book/<int:pk>/',views.BookRetriveUpdateDeleteView.as_view()),

    path('v2/books/',views.BookListView.as_view()),
    path('v2/books/<int:pk>/',views.BookGenericView.as_view()),

    path('v2/books/<int:pk>/reviews/',views.ReviewCreateView.as_view())
    
]+router.urls

