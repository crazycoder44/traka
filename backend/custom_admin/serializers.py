from rest_framework import serializers

from .models import Products
from .models import Branches
from .models import Users

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = [
            'id',
            'productname',
            'desc',
            'price',
            'status',
        ]

    def create(self, validated_data):
        # Use the add_product method, which saves to 'default' by design
        return Products.add_product(validated_data)


class BranchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branches
        fields = [
            'id',
            'branchname',
            'address',
            'mobile',
            'date',
        ]

    def create(self, validated_data):
        result = Branches.add_branch(validated_data)
        if isinstance(result, dict) and "message" in result:
            raise serializers.ValidationError(result["message"])
        return result
    
    def update(self, instance, validated_data):
        # Call the update_branch method, passing instance.id as branch_id and validated_data for updates
        result = Branches.update_branch(instance.id, validated_data)

        # If the result is a dictionary with a message, raise a ValidationError
        if isinstance(result, dict) and "message" in result:
            raise serializers.ValidationError(result["message"])

        # Return the updated instance
        return result


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'firstname',
            'lastname',
            'gender',
            'email',
            'mobile',
            'address',
            'role',
            'datejoined',
            'branch',
            'password',
        ]
        extra_kwargs = {
            'password': {'write_only': True},  # Make password write-only
        }

    def create(self, validated_data):
        # Use the add_user method from the Users model to create a new user
        result = Users.add_user(validated_data)
        
        # If result is a dictionary with a message, raise a ValidationError
        if isinstance(result, dict) and "message" in result:
            raise serializers.ValidationError(result["message"])

        return result