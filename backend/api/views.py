import json
from django.forms.models import model_to_dict
from django.http import JsonResponse
from products.models import Product

# Rest Frame Fork For Django
from rest_framework.response import Response
from rest_framework.decorators import api_view
from products.serializers import ProductSerializer
# Django Models


@api_view(["POST"])
def api_home(request, *args, **kwargs):
    """_summary_

    DRF API View

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    data = request.data
    instance = Product.objects.all().order_by("?").first()
    data = {}
    if instance:
        # data = model_to_dict(instance, fields=[
        #                      'id', 'title', 'price', 'sale_price'])
        data = ProductSerializer(instance).data

    return Response(
        data
    )


def api_home2(request, *args, **kwargs):
    """_summary_

    Its was for testing

    Args:
        request (any): json request

    Returns:
        JsonResponse: data
    """
    # request -> HttpRequest -> Django
    # print(dir(request))
    # request.body
    # print(request.GET) # url query params
    body = request.body  # byte string JSON data
    data = {}
    try:
        data = json.loads(body)  # string of JSON data -> Python Dict
    except:
        pass

    print(data)
    data['params'] = dict(request.GET)
    data['headers'] = dict(request.headers)  # request.META -> old request
    data['content_type'] = request.content_type
    return JsonResponse(
        data
    )
