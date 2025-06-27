"""
Contains any script to be written
"""

import pandas as pd


def df_cleaning(partition_df):
    """
    This function drops irrelevant columns and selected
    rows from the partitions.
    Args:
        partition_df (_type_): _description_
    """
    try:
        col_to_drop = ["sales_commission_code", "Working Date", "M-Y"]
        for cols in col_to_drop:
            if cols in partition_df.columns:
                partition_df = partition_df.drop(columns=cols)
            else:
                pass

        vals_dropped_df = partition_df.dropna()

        vals_dropped_df = vals_dropped_df[~(vals_dropped_df["category_name_1"] == r"\N")]
        vals_dropped_df = vals_dropped_df[~(vals_dropped_df["status"] == r"\N")]
        vals_dropped_df = vals_dropped_df[~(vals_dropped_df["BI Status"] == r"#REF!")]
        # vals_dropped_df = vals_dropped_df.reset_index()
        vals_dropped_df.reset_index(inplace=True)
    except Exception as e:
        return f'Error Raised: {e}'
    return vals_dropped_df


def df_transforming(clean_data):
    """
    This function transforms the clean_data
    Args:
        clean_data (pd.clean_dataFrame): Cleaned clean_dataframe

    Returns:
        pd.clean_dataFrame: Transformed clean_data
    """
    try:
        clean_data[" MV "] = clean_data[" MV "].replace(r",", "", regex=True)
        clean_data[' MV '] = (clean_data[' MV '].replace(r'-', 0, regex=True))
        clean_data["Customer ID"] = clean_data["Customer ID"].astype(int)
        clean_data[" MV "] = pd.to_numeric(clean_data[" MV "], errors="coerce")
        month_map = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December",
        }
        clean_data["Month"] = clean_data["Month"].map(month_map)

        clean_data = clean_data.rename(
            columns={
                "sku": "stock_keeping_unit",
                "category_name_1": "category_name",
                " MV ": "market_value",
                "BI Status": "BI_status",
                "Customer Since": "customer_since",
                "Customer ID": "customer_id",
            }
        )
        clean_data = clean_data.drop(columns="index")
    except Exception as e:
        return f'Exception raised: {e}'
    return clean_data
