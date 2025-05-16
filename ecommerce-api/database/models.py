"""
Tables Creation

Name: Arowosegbe Victor Iyanuoluwa\n
Email: Iyanuvicky@gmail.com\n
GitHub: https://github.com/Iyanuvicky22/projects
"""
from sqlalchemy import ForeignKey, Column, Integer
from sqlalchemy import String, Date, DECIMAL, Index
from sqlalchemy.orm import relationship, backref, declarative_base

Base = declarative_base()


class CustomersTable(Base):
    """
    Customer Table Definition Class

    Args:
        Base (Class): Table declarative class.
    """
    __tablename__ = 'Customers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(String(20), unique=True)
    gender = Column(String(10))
    device_type = Column(String(20))
    login_type = Column(String(20))
    customers = relationship('OrdersTable', backref='Customers')


class OrdersTable(Base):
    """
    Orders Table Definition Class

    Args:
        Base (Class): Table declarative class.
    """
    __tablename__ = 'Orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(String(20), ForeignKey('Customers.customer_id'))
    order_date = Column(Date)
    order_priority = Column(String(10))
    payment_method = Column(String(20))
    orders_ids = relationship('OrderItemsTable', backref=backref('Orders'))

    __table_args__ = (
        Index('idx_order_customer', 'customer_id'),
        )


class Products(Base):
    """
    Products Table Definition Class

    Args:
        Base (Class): Table declarative class.
    """
    __tablename__ = 'Products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_category = Column(String(50))
    product_name = Column(String(100))
    product_ids = relationship('OrderItemsTable', backref=backref('Products'))


class OrderItemsTable(Base):
    """
    Orders Items Table Definition Class

    Args:
        Base (Class): Table declarative class.
    """
    __tablename__ = 'Order_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('Orders.id'))
    product_id = Column(Integer, ForeignKey('Products.id'))
    quantity = Column(Integer)
    discount = Column(DECIMAL(5, 2))
    sales = Column(DECIMAL(10, 2))
    profit = Column(DECIMAL(10, 2))
    shipping_cost = Column(DECIMAL(10, 2))

    __table_args__ = (
        Index("idx_product_sales", 'product_id'),
    )
