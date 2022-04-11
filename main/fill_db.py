from django.http import HttpResponse

from main.models import Place


import pandas as pd
import numpy as np


places_df = pd.read_csv('places_prod.csv')


def fill_places():
    # python manage.py migrate main zero
    # python3 manage.py migrate
    places_df['Сайт'] = places_df['Сайт'].fillna('')
    places_df['instagram'] = places_df['instagram'].fillna('')
    places_df['vkontakte'] = places_df['vkontakte'].fillna('')
    places_df['Телефон'] = places_df['Телефон'].fillna('')
    places_df['Мобильный телефон'] = places_df['Мобильный телефон'].fillna('')

    for i, row in places_df.iterrows():
        if row['Телефон'] and row['Мобильный телефон']:
            phone_numbers = str(row['Телефон']) + ', ' + str(row['Мобильный телефон'])
        else:
            phone_numbers = str(row['Телефон']) + str(row['Мобильный телефон'])

        # if str(row['rating']) != 'nan':
        #     rating = float(str(row['rating']).replace(',', '.'))
        # else:
        #     rating = 0

        place = Place(
            name=str(row['Название']),
            search_name=str(row['Название']).lower(),

            ymap_id=int(row['ID']),
            address=str(row['Адрес']),

            rating=row['rating'],
            reviews_number=int(row['reviews_number']),
            sum_rating=int(row['sum_rating']),

            chain_id=int(row['branch']),

            category=str(row['Рубрика']),
            subcategory=str(row['Подрубрика']),

            site=str(row['Сайт']),
            phone_numbers=phone_numbers,
            vk=str(row['vkontakte']),

        )
        place.save()
    return HttpResponse((Place.objects.all().count(), ' ', Place.objects.all()[0].id))
