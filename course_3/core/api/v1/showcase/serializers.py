from apps.showcase.models import Breed
from apps.showcase.models import Dog
from rest_framework.serializers import CharField
from rest_framework.serializers import ModelSerializer


class BreedSerializer(ModelSerializer):
    class Meta:
        model = Breed
        fields = (
            "name",
            "size",
            "friendliness",
            "trainability",
            "shedding_amount",
            "exercise_needs",
        )


class ReadBreedSerializer(ModelSerializer):
    size = CharField(source="get_size_display")

    class Meta:
        model = Breed
        fields = (
            "id",
            "name",
            "size",
            "friendliness",
            "trainability",
            "shedding_amount",
            "exercise_needs",
        )


class DogSerializer(ModelSerializer):
    class Meta:
        model = Dog
        fields = (
            "name",
            "age",
            "gender",
            "color",
            "favorite_food",
            "favorite_toy",
            "breed",
        )


class ReadDogSerializer(ModelSerializer):
    breed = CharField(source="breed.name")
    gender = CharField(source="get_gender_display")
    color = CharField(source="get_color_display")

    class Meta:
        model = Dog
        fields = (
            "id",
            "name",
            "age",
            "gender",
            "color",
            "favorite_food",
            "favorite_toy",
            "breed",
        )
