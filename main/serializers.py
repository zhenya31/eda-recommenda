from django.core.serializers import serialize

from main.models import Place


def serialize_places(objects):
    fields = (
        'id',
        'name',
        'address',
        'reviews_number',
        'rating',
        'category',
        'subcategory',
        'site',
        'phone_numbers',
        'vk',
        'chain_id',
#       'ymap_id',
    )

    return serialize('python', objects, fields=fields)
