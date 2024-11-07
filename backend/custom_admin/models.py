from django.db import models
from django.contrib.auth.hashers import make_password
from oshodi.models import Sales as oshodi_sales
from oshodi.models import Inventory as oshodi_inventory
from ojota.models import Sales as ojota_sales
from ojota.models import Inventory as ojota_inventory


class Products(models.Model):
    productname = models.CharField(max_length=150)
    desc = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)

    STATUS_CHOICES = [
        (0, 'Unavailable'),
        (1, 'Available')
    ]
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)


    @staticmethod
    def add_product(validated_data):
        if 'status' not in validated_data:
            validated_data['status'] = 0

        product_instance = Products(**validated_data)
        product_instance.save(using='default')  # Always use 'default' database
        return product_instance
    
    @staticmethod
    def update_product(validated_data):
        # Check if productname is in the validated data
        if 'productname' in validated_data:
            return {"message": "Product name update is not allowed."}

        # Retrieve product instance by id (ensure 'id' is in validated_data)
        product_id = validated_data.get("id")
        if not product_id:
            return {"message": "Product ID is required for update."}

        # Check if at least 'price' or 'desc' or 'status' is provided
        if 'price' not in validated_data and 'desc' not in validated_data and 'status' not in validated_data:
            return {"message": "Price, desc, or status values are required to perform update."}

        # Get the existing product instance from the 'default' database
        try:
            product_instance = Products.objects.using('default').get(id=product_id)
        except Products.DoesNotExist:
            return {"message": "Product does not exist."}

        # Update only the fields present in validated_data
        if 'price' in validated_data:
            product_instance.price = validated_data['price']
        if 'desc' in validated_data:
            product_instance.desc = validated_data['desc']
        if 'status' in validated_data:
            product_instance.status = validated_data['status']

        product_instance.save(using='default')  # Save to 'default' database
        return product_instance
    
    @staticmethod
    def delete_product(productid):
        tables = [
            {"db": "oshodi", "table": oshodi_sales},
            {"db": "oshodi", "table": oshodi_inventory},
            {"db": "ojota", "table": ojota_sales},
            {"db": "ojota", "table": ojota_inventory}
        ]


        # Check if the product exists in the 'default' database
        try:
            product_instance = Products.objects.using('default').get(id=productid)
        except Products.DoesNotExist:
            return {"message": "Product does not exist."}

        for entry in tables:
            try:
                # Check for sales or inventory records in the specified table of each database
                exists = entry["table"].objects.using(entry["db"]).filter(productid=productid).exists()

                print(f"Checking {entry['name']} in {entry['db']} for product_id {productid}: {'Exists' if exists else 'Does not exist'}")
                
                # If any records are found, return a message and stop deletion
                if exists:
                    return {"message": "Products with sales or inventory records cannot be deleted."}
            
            except Exception as e:
                # If an error occurs due to a missing table, log it and continue
                print(f"Skipping check for {entry['name']} due to error: {e}")
                continue
        # No records found in sales or inventory; proceed with deletion in 'default' database
        product_instance.delete(using='default')
        return {"message": "Product deleted successfully."}
    


class Branches(models.Model):
    branchname = models.CharField(max_length=50)
    address = models.TextField()
    mobile = models.CharField(max_length=15, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.branchname
    
    @staticmethod
    def add_branch(validated_data):
        branchname = validated_data.get('branchname')
        address = validated_data.get('address')
        mobile = validated_data.get('mobile')

        # Check if a branch with the same name already exists
        if Branches.objects.using('default').filter(branchname=branchname).exists():
            return {"message": "A branch with this name already exists."}

        # Check if a branch with the same address already exists
        if Branches.objects.using('default').filter(address=address).exists():
            return {"message": "A branch already exists at this address."}

        # No conflicts found, create a new branch
        branch_instance = Branches(branchname=branchname, address=address, mobile=mobile)
        branch_instance.save(using='default')  # Save to the database
        return branch_instance
    
    @staticmethod
    def update_branch(branch_id, validated_data):
        # Log the branch ID for debugging
        print("Branch ID from URL:", branch_id)

        # Retrieve branch details from the validated data
        branchname = validated_data.get('branchname')
        address = validated_data.get('address')
        mobile = validated_data.get('mobile')

        # Retrieve the existing branch instance by ID
        try:
            branch_instance = Branches.objects.using('default').get(id=branch_id)
        except Branches.DoesNotExist:
            return {"message": "Branch does not exist."}

        # Check for duplicate branch name, excluding the current branch
        if branchname and Branches.objects.using('default').filter(branchname=branchname).exclude(id=branch_id).exists():
            return {"message": "A branch with this name already exists."}

        # Check for duplicate address, excluding the current branch
        if address and Branches.objects.using('default').filter(address=address).exclude(id=branch_id).exists():
            return {"message": "A branch already exists at this address."}

        # Check for duplicate mobile number, excluding the current branch
        if mobile and Branches.objects.using('default').filter(mobile=mobile).exclude(id=branch_id).exists():
            return {"message": "A branch already exists with this mobile number."}

        # Update the branch instance with the new data
        if branchname is not None:
            branch_instance.branchname = branchname
        if address is not None:
            branch_instance.address = address
        if mobile is not None:
            branch_instance.mobile = mobile

        # Save the updated instance to the database
        branch_instance.save(using='default')
        return branch_instance



class Users(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    ROLE_CHOICES = [
        ('Superadmin', 'Superadmin'),
        ('Admin', 'Admin'),
        ('Sales Rep', 'Sales Rep'),
    ]

    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    address = models.TextField()
    role = models.CharField(max_length=11, choices=ROLE_CHOICES)
    datejoined = models.DateTimeField(auto_now_add=True)
    branch = models.ForeignKey(Branches, on_delete=models.PROTECT, null=True, blank=True)
    password = models.CharField(max_length=128, default=make_password("1234567"))

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    @classmethod
    def add_user(cls, validated_data):
        # Check if a user with the given email already exists
        if cls.objects.using('default').filter(email=validated_data.get('email')).exists():
            return {"message": "A user already exists with this email."}

        # Hash the password and create a new user
        password = validated_data.get('password', "1234567")  # Default if password not in validated_data
        hashed_password = make_password(password)
        
        # Save the new user instance with hashed password
        new_user = cls(
            firstname=validated_data.get('firstname'),
            lastname=validated_data.get('lastname'),
            gender=validated_data.get('gender'),
            email=validated_data.get('email'),
            mobile=validated_data.get('mobile'),
            address=validated_data.get('address'),
            role=validated_data.get('role'),
            branch=validated_data.get('branch'),
            password=hashed_password
        )
        new_user.save(using='default')
        return new_user

   
