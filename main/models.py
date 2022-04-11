from django.db import models


class Place(models.Model):
    name = models.CharField('Название', max_length=255)
    ymap_id = models.IntegerField()
    address = models.CharField('Адрес', max_length=1024)

    search_name = models.CharField('Название для поиска', max_length=255)

    rating = models.FloatField('Рейтинг')
    reviews_number = models.IntegerField()
    sum_rating = models.IntegerField()

    category = models.CharField('Категория', max_length=255)
    subcategory = models.CharField('Подкатегория', max_length=255)

    chain_id = models.IntegerField()

    site = models.CharField('Сайт', max_length=255)
    phone_numbers = models.CharField('Номер телефона', max_length=255)
    vk = models.CharField('VK', max_length=255)
    instagram = models.CharField('Instagram', max_length=255)

    def __str__(self):
        return self.name





