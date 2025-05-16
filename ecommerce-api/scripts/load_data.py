"""
Data Loading into Database

Name: Arowosegbe Victor Iyanuoluwa\n
Email: Iyanuvicky@gmail.com\n
GitHub: https://github.com/Iyanuvicky22/projects
"""
import pandas as pd
from database.db_setup import connect_db, CustomersTable, Products
from database.db_setup import OrderItemsTable, OrdersTable

pd.set_option('display.max_columns', None)

FILEPATH = 'data/ecommerce_dataset.csv'


def load_data():
    """
    Loading CSV file dataframe into the
    ecommerce database schema.
    All columns in the dataframe are mapped to different tables
    Relationships and constriants are also well defined.
    """
    Session, engine = connect_db()
    database_df = pd.read_csv(FILEPATH)
    database_df = database_df.dropna().reset_index()

    with Session.begin() as session:
        for _, row in database_df.iterrows():
            customer = session.query(CustomersTable).filter_by(
                       customer_id=str(row['Customer_Id'])
                       ).first()
            if not customer:
                customer = CustomersTable(
                    customer_id=str(row['Customer_Id']),
                    gender=row['Gender'],
                    device_type=row['Device_Type'],
                    login_type=row['Customer_Login_type']
                                               )
                session.add(customer)

            product = session.query(Products).filter_by(
                      product_category=row['Product_Category'],
                      product_name=row['Product']).first()

            if not product:
                product = Products(
                    product_category=row['Product_Category'],
                    product_name=row['Product']
                                        )
                session.add(product)

            orders = OrdersTable(
                customer_id=customer.customer_id,
                order_date=row['Order_Date'],
                order_priority=row['Order_Priority'],
                payment_method=row['Payment_method']
                                        )
            session.add(orders)

            order_item = OrderItemsTable(
                order_id=orders.id,
                product_id=product.id,
                quantity=row['Quantity'],
                discount=row['Discount'],
                sales=row['Sales'],
                profit=row['Profit'],
                shipping_cost=row['Shipping_Cost']
                                                )
            session.add(order_item)
        session.commit()


if __name__ == '__main__':
    load_data()
