"""
Seed Ai_tools data upload to database.

Name: Arowosegbe Victor Iyanuoluwa\n
Email: Iyanuvicky@gmail.com\n
GitHub: https://github.com/Iyanuvicky22/projects
"""

from utils.utils import read_data, transform_data
from utils.models import upsert_agents

seed_data_source = r"C:\Users\APIN PC\OneDrive\Documents\DS\DE_Inter\data_epic_capstone\etl\data\seeded_ai_agents.csv"


def trans_load_seed_df():
    """
    Function to Load Seed Data into Database
    """
    data = read_data(source_path=seed_data_source)

    trans_seed_df = transform_data(df=data)

    upsert_agents(trans_seed_df)

    return trans_seed_df

if __name__ == "__main__":
    trans_load_seed_df()
