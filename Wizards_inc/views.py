from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.db import Error, OperationalError
from django.db.transaction import atomic
from psycopg2 import errorcodes
from functools import wraps
import json
import sys
import time

from .models import *


def retry_on_exception(view, num_retries=3, on_failure=HttpResponse(status=500), delay_=0.5, backoff_=1.5):
    @wraps(view)
    def retry(*args, **kwargs):
        delay = delay_
        for i in range(num_retries):
            try:
                return view(*args, **kwargs)
            except OperationalError as ex:
                if i == num_retries - 1:
                    return on_failure
                elif getattr(ex.__cause__, 'pgcode', '') == errorcodes.SERIALIZATION_FAILURE:
                    time.sleep(delay)
                    delay *= backoff_
                else:
                    return on_failure
            except Error as ex:
                return on_failure
    return retry


class PingView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("python/django", status=200)


@method_decorator(csrf_exempt, name='dispatch')
class MagiciansView(View):
    def get(self, request, id=None, *args, **kwargs):
        if id is None:
            magician= list(MAGICIANS.objects.values())
        else:
            magician = list(MAGICIANS.objects.filter(id=id).values())
        return JsonResponse(magician, safe=False)

    @retry_on_exception
    @atomic
    def post(self, request, *args, **kwargs):
        form_data = json.loads(request.body.decode())
        name = form_data['name']
        m = MAGICIANS(name=name)
        m.save()
        return HttpResponse(status=200)

    @retry_on_exception
    @atomic
    def delete(self, request, id=None, *args, **kwargs):
        if id is None:
            return HttpResponse(status=404)
        MAGICIANS.objects.filter(id=id).delete()
        return HttpResponse(status=200)



@method_decorator(csrf_exempt, name='dispatch')
class Magician_hire_costView(View):
    def get(self, request, id=None, *args, **kwargs):
        if id is None:
            hire_cost = list(Magician_hire_cost.objects.values())
        else:
            hire_cost = list(Magician_hire_cost.objects.filter(id=id).values())
        return JsonResponse(hire_cost, safe=False)

    @retry_on_exception
    @atomic
    def post(self, request, *args, **kwargs):
        form_data = json.loads(request.body.decode())
        name, price = form_data['name'], form_data['price']
        h = Magician_hire_costView(name=name, price=price)
        h.save()
        return HttpResponse(status=200)



@method_decorator(csrf_exempt, name='dispatch')
class Total_priceView(View):
    def get(self, request, id=None, *args, **kwargs):
        if id is None:
            price = list(Total_price.objects.values())
        else:
            price = list(Total_price.objects.filter(id=id).values())
        return JsonResponse(price, safe=False)

    @retry_on_exception
    @atomic
    def post(self, request, *args, **kwargs):
        form_data = json.loads(request.body.decode())
        m = Magicians.objects.get(id=form_data['customer']['id'])
        o = Orders(subtotal=form_data['subtotal'], customer=c)
        o.save()
        for m in form_data['magician']:
            m = MAGICIANS.objects.get(id=m['id'])
            o.magician.add(m)
        o.save()
        return HttpResponse(status=200)