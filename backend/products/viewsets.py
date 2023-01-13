from rest_framework import mixins, viewsets

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):

    """
    get -> list -> Queryset

    get -> retrieve -> Product Instance Detail View

    post -> create -> New Instance

    put -> update

    patch -> Partial Update

    delete -> Destroy

    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'  # defaul


class ProductGeenericViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """
    get -> list -> Queryset

    get -> retrieve -> Product Instance Detail View

    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'  # defaul


product_list_view = ProductGeenericViewSet.as_view({'get': 'list'})

product_list_view = ProductGeenericViewSet.as_view({'get': 'retrieve'})
