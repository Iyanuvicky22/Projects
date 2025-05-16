"""
FastAPI Interface for Database Fundamentals Project

Name: Arowosegbe Victor Iyanuoluwa\n
Email: Iyanuvicky@gmail.com\n
GitHub: https://github.com/Iyanuvicky22/projects
"""
import logging
from fastapi import FastAPI
from database.crud import *
from database.db_setup import *

app = FastAPI()
session, engine = connect_db()


@app.get("/")
async def root():
    """
    Welcome Message

    Returns:
        dict: Welcome message
    """
    return {"message": "Arowosegbe Victor's Database fundamental project"}


@app.get("/customers/")
def get_all_customers(page: int = 1, size: int = 25):
    """
    Getting customers information. Default is first 25 customers.
    Args:
        page (int, optional): _description_. Defaults to 1.
        size (int, optional): _description_. Defaults to 25.

    Returns:
        dict: Dict response of successful/failed api call.
    """
    try:
        if session is None:
            raise "Failed to connect to database"
        offset = (page - 1) * size
        filter_customers = session().query(
            CustomersTable).offset(offset).limit(size)
        customer_list = [
            {"id": customer.id,
             "customer_id": customer.customer_id,
             "gender": customer.gender,
             "device_type": customer.device_type,
             "login_type": customer.login_type
             }
            for customer in filter_customers
        ]
        session().close()
        return {
            "message": "Customers fetched",
            "success": True,
            "data": {
                "page": page,
                "size": size,
                "customers": customer_list,
            },
        }
    except Exception as e:
        logging.error("Unexpected error in get_all_customers:%s", str(e))
        return {
            "message": "An unexpected error occurred",
            "success": False,
            "data": None
        }


@app.get("/customers/{customer_id}")
def get_customers_by_customer_id(customer_id):
    """
    Getting customers info by their id.
    Returns:
        dict: Dict of successful/failed api response
    """
    try:
        if session is None:
            raise "Failed to connect to database"
        filter_customers = session().query(CustomersTable).filter_by(
            customer_id=customer_id).scalar()
        customer = {"id": filter_customers.id,
                    "customer_id": filter_customers.customer_id,
                    "gender": filter_customers.gender,
                    "device_type": filter_customers.device_type,
                    "login_type": filter_customers.login_type
                    }
        session().close()
        return {
            "message": "Customer fetched",
            "success": True,
            "data": customer,
        }
    except Exception as e:
        logging.error("Unexpected error in get_all_products: %s", {str(e)})
        return {
            "message": "An unexpected error occurred",
            "success": False,
            "data": None
        }


@app.get("/orders/")
def get_all_orders(page: int = 1, size: int = 50):
    """
    Getting all orders. Default is first 50 orders.
    Args:
        page (int, optional): _description_. Defaults to 1.
        size (int, optional): _description_. Defaults to 50.
    Returns:
        dict: Dict of successful/failed api response
    """
    try:
        if session is None:
            raise "Failed to connect to database"
        offset = (page - 1) * size
        filter_orders = session().query(OrdersTable).offset(offset).limit(size)
        order_list = [
            {
                "id": order.id,
                "customer_id": order.customer_id,
                "order_date": order.order_date,
                "order_priority": order.order_priority,
                "payment_method": order.payment_method
            }
            for order in filter_orders
        ]
        session().close()
        return {
            "message": "Orders fetched",
            "success": True,
            "data": {
                "page": page,
                "size": size,
                "customers": order_list,
            },
        }
    except Exception as e:
        logging.error(f"Unexpected error in get_all_products: {str(e)}")
        return {
            "message": "An unexpected error occurred",
            "success": False,
            "data": None
        }


@app.get("/orders/{order_id}")
def get_order_by_order_id(order_id):
    """
    Getting order by its id.
    Returns:
        dict: Dict of successful/failed api response
    """
    try:
        if session is None:
            raise "Failed to connect to database"
        filter_orders = session().query(OrdersTable).filter_by(id=order_id).scalar()
        order = {
            "id": filter_orders.id,
            "customer_id": filter_orders.customer_id,
            "order_date": filter_orders.order_date,
            "order_priority": filter_orders.order_priority,
            "payment_method": filter_orders.payment_method
        }
        session().close()
        return {
            "message": "Order fetched",
            "success": True,
            "data": order,
        }
    except Exception as e:
        logging.error(f"Unexpected error in get_all_products: {str(e)}")
        return {
            "message": "An unexpected error occurred",
            "success": False,
            "data": None
        }


@app.get("/products/")
def get_all_products(page: int = 1, size: int = 25):
    """
    Getting all products. Defaults to first 25 products.
    Args:
        page (int, optional): _description_. Defaults to 1.
        size (int, optional): _description_. Defaults to 25.
    Returns:
        dict: Dict of successful/failed api response
    """
    try:
        if session is None:
            raise "Failed to connect to database"
        offset = (page - 1) * size
        filter_products = session().query(Products).offset(offset).limit(size)
        product_list = [
            {
                "id": product.id,
                "product_category": product.product_category,
                "product_name": product.product_name
            }
            for product in filter_products
        ]
        session().close()
        return {
            "message": "Products fetched",
            "success": True,
            "data": {
                "page": page,
                "size": size,
                "customers": product_list,
            },
        }
    except Exception as e:
        logging.error(f"Unexpected error in get_all_products: {str(e)}")
        return {
            "message": "An unexpected error occurred",
            "success": False,
            "data": None
        }


@app.get("/analytics/top-products/")
def get_top_products():
    """
    Getting top products
    Returns:
        dict: Dict of successful/failed api response
    """
    try:
        session = session
        top_products = product_performance(session)
        session.close()

        return {
            "message": "Products fetched",
            "success": True,
            "data": top_products,
        }

    except Exception as e:
        logging.error(f"Unexpected error in get_top_products: {str(e)}")
        return {
            "message": "An unexpected error occurred",
            "success": False,
            "data": None
        }


@app.get("/analytics/revenue/")
def get_total_profit_revenue():
    """
    Getting total profits 
    Returns:
        dict: Dict of successful/failed api response
    """
    try:
        total__revenue = order_analysis(session=session())
        return {
            "message": "Products fetched",
            "success": True,
            "data": total__revenue,
        }
    except Exception as e:
        logging.error("Unexpected error in get_total_profit_revenue %s", str(e))
        return {
            "message": f"An error occurred. Details: {str(e)}",
            "success": False,
            "data": None
        }


@app.get("/analytics/discount-impact/")
def get_discount_impact():
    """
    Getting discounts impact
    Returns:
        dict: Dict of successful/failed api response
    """
    try:
        impact = discount_impact(session=session())

        return {
            "message": "Discount impact data fetched successfully",
            "success": True,
            "data": impact,
        }
    except Exception as e:
        logging.error("Unexpected error in get_discount_impact %s", str(e))
        return {
            "message": f"An error occurred. Details: {str(e)}",
            "success": False,
            "data": None
        }
