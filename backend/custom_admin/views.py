from rest_framework import generics, status
from rest_framework.response import Response

from .models import Products
from .models import Branches
from .models import Users

from .serializers import ProductsSerializer
from .serializers import BranchesSerializer
from .serializers import UsersSerializer


class ProductsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Products.objects.using('default').all()
    serializer_class = ProductsSerializer

products_list_create_view = ProductsListCreateAPIView.as_view()


class ProductsDetailAPIView(generics.RetrieveAPIView):
    queryset = Products.objects.using('default').all()
    serializer_class = ProductsSerializer
    # lookup_field = 'pk'

products_detail_view = ProductsDetailAPIView.as_view()


class ProductsUpdateAPIView(generics.UpdateAPIView):
    queryset = Products.objects.using('default').all()
    serializer_class = ProductsSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        # Get the product instance to update
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Validate the data with the serializer
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data['id'] = instance.pk
        
        # Call the update_product method with validated data
        update_response = Products.update_product(serializer.validated_data)
        
        # Check if update_product returned a message (indicating no update was performed)
        if isinstance(update_response, dict) and "message" in update_response:
            return Response(update_response, status=status.HTTP_400_BAD_REQUEST)

        # If update was successful, return the updated instance data
        serializer = self.get_serializer(update_response)
        return Response(serializer.data, status=status.HTTP_200_OK)

products_update_view = ProductsUpdateAPIView.as_view()



class ProductsDestroyAPIView(generics.DestroyAPIView):
    queryset = Products.objects.using('default').all()
    serializer_class = ProductsSerializer
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        # Get the product ID from the URL
        productid = self.kwargs.get(self.lookup_field)
        
        # Attempt to delete the product using the custom delete_product method
        result = Products.delete_product(productid)
        
        # Check if the result message indicates successful deletion
        if result.get("message") == "Product deleted successfully.":
            return Response(result, status=status.HTTP_204_NO_CONTENT)
        
        # Return the message from delete_product with a status of 400 Bad Request
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

products_destroy_view = ProductsDestroyAPIView.as_view()


class BranchesListCreateAPIView(generics.ListCreateAPIView):
    queryset = Branches.objects.using('default').all()
    serializer_class = BranchesSerializer

branches_listcreate_view = BranchesListCreateAPIView.as_view()


class BranchesDetailAPIView(generics.RetrieveAPIView):
    queryset = Branches.objects.using('default').all()
    serializer_class = BranchesSerializer
    lookup_field = 'id'

branches_detail_view = BranchesDetailAPIView.as_view()


class BranchesUpdateAPIView(generics.UpdateAPIView):
    queryset = Branches.objects.using('default').all()
    serializer_class = BranchesSerializer
    # lookup_field = 'id'

branches_update_view = BranchesUpdateAPIView.as_view()



class UsersListCreateAPIView(generics.ListCreateAPIView):
    queryset = Users.objects.using('default').all()
    serializer_class = UsersSerializer
    # lookup_field = 'id'

users_listcreate_view = UsersListCreateAPIView.as_view()



class UsersDetailAPIView(generics.RetrieveAPIView):
    queryset = Users.objects.using('default').all()
    serializer_class = UsersSerializer
    # lookup_field = 'id'

users_detail_view = UsersDetailAPIView.as_view()