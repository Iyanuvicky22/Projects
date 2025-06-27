import pymupdf 
import pandas as pd


def parse_bank_statement(file_path: str)-> pd.DataFrame:
    """
    Bank Statement Parser
    Args:
        file_path (str): PDF Bank Statement filepath 

    Returns:
        pd.DataFrame: Extracted Bank Statement in pandas Dataframe
    """

    tables = []
    with pymupdf.open(file_path) as doc:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text_blocks = page.get_text('blocks')

            sorted_blocks = sorted(text_blocks, key=lambda b: b[1])

            table_data = []
            for block in sorted_blocks:
                lines = block[4].split('\n')
                table_data.append(lines)

            if table_data:
                df = pd.DataFrame(table_data)
                processed_df = df

                if not processed_df.empty:
                    tables.append(processed_df)
                    # print(tables)

    if tables:
        concat_df = pd.concat(tables, ignore_index=True)
        bank_statement = concat_df
    else:
        bank_statement = pd.DataFrame()


filepath = 'C:/Users/APIN PC/OneDrive/Documents/DS/circle_funds_externship/bank_statement_parser/gtb_bs/Gtb_bs.pdf'

ab = parse_bank_statement(file_path=filepath)
print(ab)

