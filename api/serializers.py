# serializers are used to convert complex data types such as querysets and model instances 
# into native Python data types like dictionaries
#They are also used for deserialization

from rest_framework import serializers
from api.models import Book,Review



class ReviewSerializer(serializers.ModelSerializer):

    book_object=serializers.StringRelatedField()

    class Meta:
        model=Review
        fields='__all__'
        read_only_fields=['id','book_object']                          # read_only_fields: To prevent certain fields from being modified by the client.(applied to multiple fields at once.)


class BookSerializer(serializers.ModelSerializer):

    # reviews=ReviewSerializer(read_only=True,many=True)

    reviews=serializers.SerializerMethodField(read_only=True)           #read_only=True:  individual field declarations in the serializer.(same as read_only_fields)
    
    # review_count=serializers.IntegerField(read_only=True) 

    review_count=serializers.SerializerMethodField(read_only=True)

    # avg_rating=serializers.IntegerField(read_only=True)

    avg_rating=serializers.SerializerMethodField(read_only=True)

    class Meta:

        model=Book

        # fields='__all__'                               #all fields in model

        fields=['id','title','author','language','price','genre','reviews','review_count','avg_rating']


    def get_review_count(self,obj):

        return Review.objects.filter(book_object=obj).count()
    
    def get_avg_rating(self,obj):

        reviews=Review.objects.filter(book_object=obj)
        avg=0
        if reviews:
            avg=sum([r.rating for r in reviews])/reviews.count()

        return avg
    
    def get_reviews(self,obj):

        qs=Review.objects.filter(book_object=obj)

        serializer_instance=ReviewSerializer(qs,many=True)

        return serializer_instance.data