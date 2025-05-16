"""
Database Analysis for Business Insights

Name: Arowosegbe Victor Iyanuoluwa\n
Email: Iyanuvicky@gmail.com\n
GitHub: https://github.com/Iyanuvicky22/projects
"""
from decimal import Decimal
from sqlalchemy import func, desc, case
from database.db_setup import CustomersTable, Products, OrdersTable
from database.db_setup import OrderItemsTable
from database.db_setup import connect_db

# Defining Session and Engine
Session, engine = connect_db()


def to_float(item) -> float:
    """
    Converts decimal values to float type.

    Args:
        value (Decimal): Database Decimal datatype

    Returns:
        float: float data type.
    """
    return float(item) if isinstance(item, Decimal) else value


# CUSTOMER INSIGHTS ANALYSIS
def customer_insights(session) -> dict:
    """
    Customer table insights.
    Args:
        session (Session): Persistence operation manager in ORM

    Returns:
        dict : Customer table insights.
    """
    total_customers = session.query(CustomersTable).count()
    customer_web_device = session.query(CustomersTable).filter(
        CustomersTable.device_type.ilike('Web')).count()
    customer_mobile_device = session.query(CustomersTable).filter(
        CustomersTable.device_type.ilike('Mobile')).count()
    customer_login_member = session.query(CustomersTable).filter(
        CustomersTable.login_type.ilike('Member')).count()
    customer_login_guest = session.query(CustomersTable).filter(
        CustomersTable.login_type.ilike('Guest')).count()
    percentage_member = f'{round(customer_login_member / total_customers,
                                 2) * 100}%'
    percentage_guest = f'{round(customer_login_guest / total_customers,
                                2) * 100}%'
    return {"total_customers": total_customers,
            "web_customer": customer_web_device,
            "mobile_customer": customer_mobile_device,
            "percentage_member": percentage_member,
            "percentage_guest": percentage_guest}


# PRODUCTS INSIGHTS ANALYSIS
def top_product_by_sales(session) -> list:
    """
    Selecting top 5 products by sales
    Args:
        session (Session): Connection Session
        SQL syntax: select p.product_name,sum(o.sales) as total_sales
                    from products p
                    join orderitemstable o on o.id = p.id
                    group by p.id, p.product_name
                    order_by total_sales desc
                    limit 5;
    Returns:
        list: Dict summary of top 5 products and sales.
    """
    top_5_product_by_sales = (session.query(
        Products.product_name,
        func.sum(OrderItemsTable.sales).label("total_sales")
    ).join(Products, OrderItemsTable.product_id == Products.id)
                              .group_by(Products.id, Products.product_name)
                              .order_by(desc('total_sales'))
                              .limit(5))

    summary = [{column: to_float(value) for column,
                value in row._mapping.items()}
               for row in top_5_product_by_sales.all()]
    return summary


def top_product_by_profit(session) -> list:
    """
    Selecting top 5 profitable products.
    Args:
        session (Session): Connection Session 
        SQL Syntax: select p.product_name, sum(o.profit) as total_profit
                    from products p
                    join orderitemstable o on o.id = p.id
                    group by p.id, p.product_name
                    order by total_profits desc
                    limit 5;

    Returns:
        list: Dictionary summary of top 5 products by profits.
    """
    top_5_product_by_profit = (session.query(
        Products.product_name,
        func.sum(OrderItemsTable.profit).label("total_profit")
    ).join(Products, OrderItemsTable.product_id == Products.id)
                               .group_by(Products.id, Products.product_name)
                               .order_by(desc('total_profit'))
                               .limit(5))

    summary = [{column: to_float(value) for column,
                value in row._mapping.items()}
               for row in top_5_product_by_profit.all()]
    return summary


def top_product_categories_by_revenue(session) -> list:
    """
    Selecting top 3 categories by revenue generated.
    Args:
        session (Session): Connection Session
        SQL Syntax: select c.product_category, sum(c.total_sales)
                            as total_category_sales
                    from  (select p.product_category, sum(o.sales)
                            as total_sales
                    from products p
                    join orderitemstable o on o.id = p.id
                    group by p.id, p.product_category) as c
                    group by c.product_category
                    order by total_category_sales desc
                    limit 3;

    Returns:
        list: Dict summary of top 3 products categories by revenue.
    """
    subquery = (session.query(
        Products.product_category,
        func.sum(OrderItemsTable.sales).label("total_sales")
    ).join(Products, OrderItemsTable.product_id == Products.id)
                .group_by(Products.id, Products.product_category)
                .subquery()
                )
    top_3_product_category_by_revenue = (session.query(
        subquery.c.product_category, func.sum(subquery.c.total_sales).label(
            "total_category_sales")
    ).group_by(subquery.c.product_category).order_by(desc(
        "total_category_sales")).limit(3))
    summary = [{column: to_float(value) for column,
                value in row._mapping.items()}
               for row in top_3_product_category_by_revenue.all()]
    return summary


def product_performance(session) -> dict:
    """
    Returning all Products insights.
    Args:
        session (Session): Connection Session

    Returns:
        list: Dict summary of products insights.
    """
    products_per_profits = top_product_by_profit(session)
    products_per_sales = top_product_by_sales(session)
    products_per_category = top_product_categories_by_revenue(session)
    return {
        "top_product_by_profit": products_per_profits,
        "top_product_by_sales": products_per_sales,
        "top_product_categories_by_revenue": products_per_category
    }


# ORDER INSIGHTS ANALYSIS
def avg_order_size(session) -> float:
    """
    Calculates average order per quantity of item.
    Args:
        session (Session): _description_
        SQL Syntax: select round(avg(average_quantity),2)
                    from
                    (select order_id, avg(quantity) as average_quantity
                    group by order_id);

    Returns:
        float: Average order per quantity
    """
    subquery = (session.query(OrderItemsTable.order_id, func.avg(
                OrderItemsTable.quantity).label(
                    "average_quantity")).group_by(
                        OrderItemsTable.order_id)).subquery()
    get_avg_order = session.query(
        func.round(func.avg(subquery.c.average_quantity), 2)
    ).scalar()
    return to_float(get_avg_order)


def total_profit_sales(session) -> list:
    """
    Total profit sales function
    Args:
        session (Session): Connection Session
        SQL Syntax: select sum(sales) as total_sales,
                           sum(profit) as total profit
                    from OrderItemsTable;

    Returns:
        list: Dictionary of total sales and price
    """
    total = (session.query(func.sum(OrderItemsTable.sales).label(
                           "total_sales"),
                           func.sum(OrderItemsTable.profit)
                           .label("total_profit")))
    summary = [{column: to_float(value) for column,
                value in row._mapping.items()}
               for row in total.all()]
    return summary


def order_percentage(session) -> float:
    """
    Query to check and get the percentage of succesful orders
    Args:
        session (Session): Connection Session
        SQL Syntax: select round(sum(case when order_priority in
                    ('High', 'Critical') then 1
                        else 0
                    end) * 100.0) / count(*), 2) as order_percentage
                    from OrdersTable;

    Returns:
        float: Percentage of successful orders.
    """
    percent = session.query(
        func.round(
            (func.sum(
                case(
                    (OrdersTable.order_priority.in_(['High', 'Critical']), 1),
                    else_=0
                )
            ) * 100.0) / func.count('*'),
            2
        ).label('order_percentage')
    ).select_from(OrdersTable).scalar()

    return to_float(percent)


def order_analysis(session) -> dict:
    """

    Args:
        session (Session): _description_

    Returns:
        _type_: _description_
    """
    order_percent = order_percentage(session)
    profit_sales = total_profit_sales(session)
    average_order = avg_order_size(session)
    return {
        "order_percentage": order_percent,
        "total_profit_revenue": profit_sales,
        "avg_order_size": average_order
    }


# DISCOUNT IMPACT ANALYSIS
def discount_impact(session) -> list:
    """

    Args:
        session (Session): _description_

    Returns:
        _type_: _description_
    """
    total = (
        session.query(
            OrderItemsTable.discount,
            func.sum(OrderItemsTable.sales).label('total_sales')
        )
        .group_by(OrderItemsTable.discount)
        .order_by(desc('total_sales'))
    )
    print(total)
    summary = [{column: to_float(value) for column,
                value in row._mapping.items()}
               for row in total.all()]
    return summary



if __name__ == '__main__':
    # # Customers Analysis Insights
    # cus_insights = customer_insights(session=Session())
    # print('CUSTOMER INSIGHTS!!!')
    # for key, value in cus_insights.items():
    #     print(key, ":", value)

    # # Products Analysis Insights
    # products_insights = product_performance(session=Session())
    # print('\n\nPRODUCT INSIGHTS!!!')
    # for key, value in products_insights.items():
    #     print(key, value, '\n')

    # # Order Analysis Insights
    # order_insights = order_analysis(session=Session())
    # print('\nORDER ANALYSIS INSIGHTS')
    # for key, value in order_insights.items():
    #     print(key, value)

    # Discount Impact Analysis
    dis_impact = discount_impact(session=Session())
    print('DISCOUNT IMPACT ANALYSIS')
    for dis in dis_impact:
        print('Discount Effect %s', dis)
