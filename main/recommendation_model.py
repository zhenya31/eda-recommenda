from django.db.models import Case, When

from main.models import Place

import pandas as pd
import numpy as np

from main.serializers import serialize_places

import csv

model = np.zeros((16864, 16864), dtype=np.short)

with open("model.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")
    for i, line in enumerate(reader):
        if i > 0:
            model[i-1] = np.array(line, dtype=np.short)
print(model.shape)

def get_recommendations(favourites):
    # model = np.array(pd.read_csv('model.csv', index_col=False, sep=','))  ## НАДО ВЫНЕСТИ ИЗ МЕТОДА
    # print(model.shape)

    scores = model[favourites[0] - 1]
    for i in range(1, len(favourites)):
        scores += model[favourites[i] - 1]

    n = 20

    chains = set(Place.objects.filter(pk__in=favourites).values_list('chain_id', flat=True))
    chains.remove(0)  # убираем из списка значение chain_id = 0
    branches = Place.objects.filter(chain_id__in=chains).values_list('id', flat=True)

    scores[np.array(favourites) - 1] = 0  # зануляем похожесь для входных ресторанов

    if branches:
        scores[np.array(branches) - 1] = 0  # зануляем похожесь для всех филиалов любимых товаров

    recommended = np.argpartition(scores, -n)[-n:]
    recommended = sorted(recommended, key=lambda x: -scores[x])

    recommended_final = []
    for rec in recommended:
        if scores[rec] < 100 and len(recommended_final) >= 3:
            break
        if scores[rec] <= 0:
            break
        if len(recommended_final) >= len(favourites) + 10:
            break
        if len(recommended_final) >= 20:
            break

        recommended_final.append(rec + 1)

    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(recommended_final)])
    recommended_places = Place.objects.filter(pk__in=recommended_final).order_by(preserved)
    recommended_places = serialize_places(recommended_places)

    for i in range(len(recommended_final)):
        recommended_places[i]['score'] = int(scores[recommended_final[i] - 1])

    return recommended_places