from flask_restful import Resource, Api, request
from package.model import conn

class CustomersAPI(Resource):
    """This contains APIs to carry out activities with all customers"""

    def get(self):
        """Retrieve a list of all customers"""
        customers = conn.execute("SELECT * FROM customer ORDER BY cust_date DESC").fetchall()
        return {"customers": customers}

    def post(self):
        """Add a new customer"""
        customer_data = request.get_json(force=True)
        cust_first_name = customer_data['cust_first_name']
        cust_last_name = customer_data['cust_last_name']
        cust_ph_no = customer_data['cust_ph_no']
        cust_address = customer_data['cust_address']
        new_customer_id = conn.execute('''INSERT INTO customer(cust_first_name, cust_last_name, cust_ph_no, cust_address)
                                   VALUES(?, ?, ?, ?)''', (cust_first_name, cust_last_name, cust_ph_no, cust_address)).lastrowid
        conn.commit()
        return {"message": "Customer added successfully", "customer_id": new_customer_id}

class CustomerAPI(Resource):
    """This contains APIs for carrying out activities with a single customer"""

    def get(self, customer_id):
        """Get the details of a customer by the customer ID"""
        customer = conn.execute("SELECT * FROM customer WHERE cust_id=?", (customer_id,)).fetchall()
        if not customer:
            return {"message": "Customer not found"}, 404
        return {"customer": customer[0]}

    def delete(self, customer_id):
        """Delete a customer by its ID"""
        conn.execute("DELETE FROM customer WHERE cust_id=?", (customer_id,))
        conn.commit()
        return {"message": "Customer deleted successfully"}

    def put(self, customer_id):
        """Update a customer by its ID"""
        customer_data = request.get_json(force=true)
        cust_first_name = customer_data['cust_first_name']
        cust_last_name = customer_data['cust_last_name']
        cust_ph_no = customer_data['cust_ph_no']
        cust_address = customer_data['cust_address']
        conn.execute(
            "UPDATE customer SET cust_first_name=?, cust_last_name=?, cust_ph_no=?, cust_address=? WHERE cust_id=?",
            (cust_first_name, cust_last_name, cust_ph_no, cust_address, customer_id)
        )
        conn.commit()
        return {"message": "Customer updated successfully"}