from django.db import models
from django.utils.functional import cached_property
from django.db.models import Sum



class Sales(models.Model):
    ORDER_SRC_CHOICES = [
        ('Facebook', 'Facebook'),
        ('Instagram', 'Instagram'),
        ('Twitter', 'Twitter'),
        ('Website', 'Website'),
        ('On premises', 'On premises'),
    ]


    orderid = models.IntegerField()
    ordersrc = models.CharField(max_length=15, choices=ORDER_SRC_CHOICES)
    productid = models.IntegerField()
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=15, decimal_places=2)
    staffid = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    
    
    @cached_property
    def total_price(self):
        return self.unit_price * self.quantity
    

    @cached_property
    def order_total(self):
        # Sum up the total_price for all sales instances with the same orderid
        related_sales = Sales.objects.filter(orderid=self.orderid)
        total_sales_price = sum(sale.total_price for sale in related_sales)

        # Subtract the return_amount from the total sales price
        return total_sales_price - self.return_amount

    

    @cached_property
    def return_amount(self):
        # Filter for return instances with the same orderid
        return_instances = Returns.objects.using('oshodi').filter(orderid=self.orderid)

        # If there are no matching returns, return 0
        if not return_instances.exists():
            return 0

        # Filter for refund instances where action='Refund'
        refund_instances = return_instances.filter(action='Refund')
        if not refund_instances.exists():
            return 0

        # Calculate the refund amount for each refund instance by finding the matching sales unit price
        refund_total = 0
        for refund_instance in refund_instances:
            # Find the corresponding sale instance for the refund
            sale_instance = Sales.objects.using('oshodi').filter(
                orderid=refund_instance.orderid,
                productid=refund_instance.productid
            ).first()

            # If a matching sale instance is found, calculate the refund amount for this instance
            if sale_instance:
                refund_total += sale_instance.unit_price * refund_instance.quantity

        return refund_total



    def process_sale(self, app_label='oshodi'):
        # Check if there are enough inventory items to fulfill the sale
        inventory_items = Inventory.objects.using(app_label).filter(productid=self.productid)

        # If no inventory items match the product ID
        if not inventory_items.exists():
            return 'Insufficient goods in inventory'

        # If the quantity in Sales exceeds available inventory items
        if self.quantity > inventory_items.count():
            return 'Insufficient goods in inventory'

        # Delete the required quantity of inventory items
        items_deleted = 0
        for item in inventory_items:
            item.delete(using=app_label)
            items_deleted += 1
            if items_deleted >= self.quantity:
                break
        return 'Sale processed successfully'

    def __str__(self):
        return (f"Order {self.orderid} - Product ID: {self.productid} - "
                f"Source: {self.ordersrc} - Quantity: {self.quantity} - "
                f"Total Price: {self.total_price}")



class Returns(models.Model):
    ACTION_CHOICES = [
        ('Replace', 'Replace'), 
        ('Refund', 'Refund'),
    ]

    orderid = models.DecimalField(max_digits=20, decimal_places=0)
    productid = models.IntegerField() 
    quantity = models.IntegerField()
    action = models.CharField(max_length=7, choices=ACTION_CHOICES)
    staffid = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)  # Automatically set timestamp on creation


    def process_return(self, app_label='oshodi'):
        # Query all Sales instances matching the orderid
        sale_instances = Sales.objects.using(app_label).filter(orderid=self.orderid)

        # If no matching sales exist, return an error
        if not sale_instances.exists():
            return 'Sale order does not exist'

        # Filter sale instances for matching product ID
        sale_instance = sale_instances.filter(productid=self.productid).first()
        
        # If no matching product found in sales, return an error
        if not sale_instance:
            return 'Returned product does not match Order product'

        # Check if the return quantity exceeds the sale quantity
        if self.quantity > sale_instance.quantity:
            return 'Return quantity exceeds Sale quantity'

        # Process inventory if action is 'Replace'
        if self.action == 'Replace':
            inventory_items = Inventory.objects.using(app_label).filter(productid=self.productid)[:self.quantity]

            if inventory_items.count() < self.quantity:
                return 'Insufficient goods in inventory'

            # Delete inventory items one by one for the required quantity
            for item in inventory_items:
                item.delete()

            return 'Return processed successfully'
        # For other actions, add additional handling here
        return 'Return action processed'


    def __str__(self):
        return f"Return {self.orderid} - Action: {self.action}"



class Inventory(models.Model):
    productid = models.IntegerField()
    serialnumber = models.CharField(max_length=50, null=True, blank=True)
    staffid = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Inventory - Product ID: {self.productid} - Serial Number: {self.serialnumber}"
