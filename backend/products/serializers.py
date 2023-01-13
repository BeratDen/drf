from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    my_discount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'content',
            'price',
            'sale_price',
            'my_discount',
        ]

    def get_my_discount(self, obj):
        """_summary_

        Args:
            obj (_type_): _description_

        Returns:
            _type_: _description_
        """

        # obj.user -> user.username
        # obj.category -> category.any
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, Product):
            return None
        return obj.get_discount()


# class SecondaryProductSerializer(serializers.ModelSerializer):

#     my_discount = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = Product
#         fields = [
#             'title',
#             'content',
#             'price',
#             'sale_price',
#             'my_discount',
#         ]

#     def get_my_discount(self, obj):
#         """_summary_

#         Args:
#             obj (_type_): _description_

#         Returns:
#             _type_: _description_
#         """

#         print(obj.id)
#         # obj.user -> user.username
#         # obj.category -> category.any
#         return obj.get_discount()
