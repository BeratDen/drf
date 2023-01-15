from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Product
from .validators import validate_title_no_hello, unique_product_title
from api.serializers import UserPublicSerializer


class ProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk',
        read_only=True
    )
    title = serializers.CharField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source='user', read_only=True)
    # my_user_data = serializers.SerializerMethodField(read_only=True)
    # related_products = ProductInlineSerializer(
    #     source='user.product_set.all()', read_only=True, many=True).data
    # print(related_products)
    my_discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk',
    )
    # email = serializers.EmailField(source='user.email', read_only=True)

    title = serializers.CharField(
        validators=[
            validate_title_no_hello, unique_product_title
        ])

    # email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Product
        fields = [
            'owner',  # user_id
            'url',
            'edit_url',
            # 'email',
            'id',
            'title',
            # 'name',
            'content',
            'price',
            'sale_price',
            'my_discount',
            # 'related_products',
            # 'my_user_data'
        ]

    # def get_my_user_data(self, obj):
    #     return {
    #         "username": obj.user.username
    #     }

    # def validate_title(self, value):
    #     request = self.context.get('request')
    #     user = request.user
    #     qs = Product.objects.filter(user=user, title__iexact=value)
    #     if qs.exists():
    #         raise serializers.ValidationError(
    #             f"{value} is already a product name")
    #     return value

    # def create(self, validated_data):
    #     # return Product.objects.create(**validated_data)
    #     # email = validated_data.pop('email')
    #     obj = super().create(validated_data)
    #     # print(email, obj)
    #     return obj

    # def update(self, instance, validated_data):
    #     email = validated_data.pop('email')
    #     return super().update(instance, validated_data)

    def get_edit_url(self, obj):

        request = self.context.get('request')
        if request is None:
            return None  # or page 404
        return reverse("product-edit", kwargs={"pk": obj.id}, request=request)

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
