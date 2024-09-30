from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import authentication,permissions
from rest_framework import generics
 
from api.serializers import BookSerializer,ReviewSerializer
from api.models import Book,Review

#........API View........

class BookListCreateView(APIView):                                
    def get(self,request,*args,**kwargs):                           #list all books

        qs=Book.objects.all()

        serializer_instance=BookSerializer(qs,many=True)               #serialization *qs--->paython native code  *when using a serializer to handle a collection of objects, you would set many=True(qs has more than one objects)
        
        return Response(data=serializer_instance.data)                 #Response :converting to JSON
    
    def post(self,request,*args,**kwargs):                          #create a book
        
        serializer_instance=BookSerializer(data=request.data)          #deserialization  *python native code --> qs

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)

        return Response(data=serializer_instance.errors)
    
class BookRetriveUpdateDeleteView(APIView):  
    def get(self,request,*args,**kwargs):                                        #retrieve a book
        id=kwargs.get('pk') 
        qs=Book.objects.get(id=id) 
        serializer_instance=BookSerializer(qs)                           #serialization
       
        return Response(data=serializer_instance.data)
    
    def put(self,request,*args,**kwargs):                                        #update a book
        id=kwargs.get('pk')
        book_obj=Book.objects.get(id=id)
        serializer_instance=BookSerializer(data=request.data,instance=book_obj)

        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        
        return Response(data=serializer_instance.errors)
    

    def delete(self,request,*args,**kwargs):                                      #delete a book
        id=kwargs.get('pk')
        Book.objects.get(id=id).delete()
        data={'message':'book deleted'}
        return Response(data)
    

#.......ViewSet.......
 
class BookViewSetView(viewsets.ViewSet):        

    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]


    def list(self,request,*args,**kwargs):
        qs=Book.objects.all()
        serializer_instance=BookSerializer(qs,many=True)
        return Response(data=serializer_instance.data)
    
    def create(self,request,*args,**kwrags):
        serializer_instance=BookSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)
        
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        qs=Book.objects.get(id=id)
        serializer_instance=BookSerializer(qs)
        return Response(data=serializer_instance.data)
    
    def update(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        book_obj=Book.objects.get(id=id)
        serializer_instance=BookSerializer(data=request.data,instance=book_obj)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)   
        else:
            return Response(data=serializer_instance.errors)
        
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        Book.objects.get(id=id).delete()
        data={'message':'book deleted'}
        return Response(data)

#..........custom methods in ViewSet............
   
    @action(methods=['GET'],detail=False)
    def genres(self,request,*args,**kwargs):

        genre=Book.objects.all().values_list('genre',flat=True).distinct()

        return Response(genre)
    


    @action(methods=['POST'],detail=True)
    def add_review(self,request,*args,**kwargs):

        book_id=kwargs.get('pk')

        book_obj=Book.objects.get(id=book_id)

        serializer_instance=ReviewSerializer(data=request.data)

        if serializer_instance.is_valid():

            serializer_instance.save(book_object=book_obj)

            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)
        
class ReviewUpdateDestroyViewSet(viewsets.ViewSet):

    def destroy(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        Review.objects.get(id=id).delete()
        data={'message':'review deleted'}

        return Response(data)
    
    def update(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        rev_obj=Review.objects.get(id=id)
        
        serializer_instance=ReviewSerializer(data=request.data,instance=rev_obj)

        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)
        
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        qs=Review.objects.get(id=id)
        serializer_instance=ReviewSerializer(qs)
        return Response(data=serializer_instance.data)
        

class BookListView(generics.ListCreateAPIView):
    serializer_class=BookSerializer
    queryset=Book.objects.all()

class BookGenericView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=BookSerializer
    queryset=Book.objects.all()

class ReviewCreateView(generics.CreateAPIView):
    serializer_class=ReviewSerializer
    queryset=Review.objects.all()

    def perform_create(self, serializer):                         #overriding this fun for adding something when serializer save here add book object
        id=self.kwargs.get('pk')
        book_obj=Book.objects.get(id=id)
        serializer.save(book_object=book_obj)
        