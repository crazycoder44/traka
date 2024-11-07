import requests

endpoint = "http://localhost:8000/api/"

get_response = requests.get(
    endpoint, 
    # json={"orderid": 2, "ordersrc": "Facebook", "productid": 4, "quantity": 1, "unit_price": 305000.00, "staffid": 1}
    # json={"productid": 1, "staffid": 1}
    # json = {"orderid": 1, "productid": 1, "quantity": 1, "action": "Replace", "staffid": 1}
    # json= {"branchname": "lekki", "address": "7, Admiralty Way Lekki Phase 1, Lekki, Lagos"}
    # json= {"productname": "Toaster", "price": 45000.00}
    # json= {
    #     "firstname": "Agba", 
    #     "lastname": "koda", 
    #     "gender": "Male", 
    #     "email": "agba@gmail.com", 
    #     "mobile": 8123456789, 
    #     "address": "fuckoff", 
    #     "role": "Sales Rep",
    # }
    params={"id": 1}
    )

print(get_response.json())