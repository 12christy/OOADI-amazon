from flask_restful import Resource, Api, request
from package.model import conn

class PaymentsAPI(Resource):
    """This contains APIs to carry out activities with all payments"""

    def get(self):
        """Retrieve a list of all payments"""
        payments = conn.execute("SELECT * FROM payment ORDER BY payment_date DESC").fetchall()
        return {"payments": payments}

    def post(self):
        """Add a new payment"""
        payment_data = request.get_json(force=True)
        customer_id = payment_data['customer_id']
        payment_amount = payment_data['payment_amount']
        payment_date = payment_data['payment_date']
        new_payment_id = conn.execute('''INSERT INTO payment(customer_id, payment_amount, payment_date)
                                   VALUES(?, ?, ?)''', (customer_id, payment_amount, payment_date)).lastrowid
        conn.commit()
        return {"message": "Payment added successfully", "payment_id": new_payment_id}

class PaymentAPI(Resource):
    """This contains APIs for carrying out activities with a single payment"""

    def get(self, payment_id):
        """Get the details of a payment by the payment ID"""
        payment = conn.execute("SELECT * FROM payment WHERE payment_id=?", (payment_id,)).fetchall()
        if not payment:
            return {"message": "Payment not found"}, 404
        return {"payment": payment[0]}

    def delete(self, payment_id):
        """Delete a payment by its ID"""
        conn.execute("DELETE FROM payment WHERE payment_id=?", (payment_id,))
        conn.commit()
        return {"message": "Payment deleted successfully"}

    def put(self, payment_id):
        """Update a payment by its ID"""
        payment_data = request.get_json(force=true)
        customer_id = payment_data['customer_id']
        payment_amount = payment_data['payment_amount']
        payment_date = payment_data['payment_date']
        conn.execute(
            "UPDATE payment SET customer_id=?, payment_amount=?, payment_date=? WHERE payment_id=?",
            (customer_id, payment_amount, payment_date, payment_id)
        )
        conn.commit()
        return {"message": "Payment updated successfully"}