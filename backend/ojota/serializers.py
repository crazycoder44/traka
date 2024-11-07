from rest_framework import serializers

from .models import Sales, Returns, Inventory


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = [
            'id',
            'orderid',
            'ordersrc',
            'productid',
            'quantity',
            'unit_price',
            'staffid',
            'date',
            'total_price',
            'return_amount',
            'order_total',
        ]

    def create(self, validated_data):
        # Create a Sales instance with the provided data
        sales_instance = Sales(**validated_data)

        # Execute the process_sale method, providing the appropriate app_label if needed
        result = sales_instance.process_sale(app_label='oshodi')  # Change app_label if needed

        # Check the result of the sale processing
        if result != 'Sale processed successfully':
            # Raise a validation error if the sale could not be processed
            raise serializers.ValidationError(result)
        
        # Save the instance after successful sale processing
        sales_instance.save()
        return sales_instance



class ReturnsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Returns
        fields = [
            'id',
            'orderid',
            'productid',
            'quantity',
            'action',
            'staffid',
            'date',
        ]
    

    def create(self, validated_data):
        # Create a Returns instance with the provided data
        returns_instance = Returns(**validated_data)

        # Execute the process_return method, passing the appropriate app_label
        result = returns_instance.process_return(app_label='oshodi')  # Change app_label if needed

        # Check the result of the return processing
        if result != 'Return processed successfully':
            # Raise a validation error if the return could not be processed
            raise serializers.ValidationError(result)
        
        # Save the instance after successful return processing
        returns_instance.save()
        return returns_instance


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = [
            'id',
            'productid',
            'serialnumber',
            'staffid',
            'date',
        ]