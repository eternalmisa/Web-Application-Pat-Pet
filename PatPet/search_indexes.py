import datetime
from haystack import indexes
from PatPet.models import *


class PetIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    pet_city = indexes.CharField(model_attr="pet_city")
    '''
    name = indexes.CharField(model_attr="name")
    age = indexes.CharField(model_attr="age")
    gender = indexes.CharField(model_attr="gender")
    breed = indexes.CharField(model_attr="breed")
    color = indexes.CharField(model_attr="color")
    start_date = indexes.DateField(model_attr="start_date")
    num_of_days = indexes.IntegerField(model_attr="num_of_days")
    content_auto = indexes.EdgeNgramField(model_attr='breed')
    '''

    def get_model(self):
        return PetInfo

    def index_queryset(self, using=None):
        return self.get_model().objects

