from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from django.http import Http404
from django.shortcuts import get_object_or_404
from api.mixins import StaffEditorPermissionMixin
from .models import Product
from .serializers import ProductSerializer


class ProductListCreateAPIView(
    StaffEditorPermissionMixin,
    generics.ListCreateAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)

        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title

        serializer.save(content=content)
        # send a Django signal


product_create_view = ProductListCreateAPIView.as_view()


class ProductDetailAPIView(
    StaffEditorPermissionMixin,
    generics.RetrieveAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'pk' -> # Product.objects.get(pk='abc')


product_detail_view = ProductDetailAPIView.as_view()


class ProductUpdateAPIView(
    StaffEditorPermissionMixin,
    generics.UpdateAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title
            ##
    # TODO: try defined function down blow
    # def perform_update(self, serializer):
    #     return super().perform_update(serializer)


product_update_view = ProductUpdateAPIView.as_view()


class ProductDestroyAPIView(
    StaffEditorPermissionMixin,
    generics.DestroyAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        # instance
        return super().perform_destroy(instance)


product_destroy_view = ProductDestroyAPIView.as_view()


# class ProductListAPIView(generics.RetrieveAPIView):
#     """
#     Not Needed to use
#     """
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     # lookup_field = 'pk' -> # Product.objects.get(pk='abc')


# product_list_view = ProductListAPIView.as_view()


class ProductMixinView(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):  # HTTP -> get
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):  # HTTP -> post
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content')
        if content is None:
            content = "this is a single view doing cool stuff"
        serializer.save(content=content)

    def put(self, request, *args, **kwargs):  # HTTP -> put
        pk = kwargs.get('pk')
        if pk is not None:
            return self.update(request, *args, **kwargs)
        return f"invalid pk {pk}"

    def delete(self, request, *args, **kwargs):  # HTTP -> delete
        pk = kwargs.get('pk')
        if pk is not None:
            return self.destroy(request, *args, **kwargs)
        return f"invalid pk {pk}"


product_mixin_view = ProductMixinView.as_view()


@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    """ Product chaned API request method

    Args:
        request (request,request_url,pk): _description_

    Returns:
        product : its return product to request method type to post or get 
        if its get and has pk its return detail page its has not pk then return all product
        and if its get method its create a product item
    """

    method = request.method  # PUT -> Update # Destroy -> delete

    if method == 'GET':

        if pk is not None:
            print(pk)
            # detail view
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data)

        # list view
        qs = Product.objects.all()  # qs -> queryset
        data = ProductSerializer(qs, many=True).data
        return Response(data)

    if method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # instance = serializer.save() # -> instance = form.save()
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None

            if content is None:
                content = title
                serializer.save(content=content)

            return Response(serializer.data)

        return Response({"invalid data": "not good data"}, status=400)
        # crete an item
