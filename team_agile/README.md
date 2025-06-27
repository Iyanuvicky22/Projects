# 🛒 Pakistan’s Largest E-Commerce Dataset – Data Pipeline

This project builds a **reproducible, cloud-native batch data pipeline** to clean, transform, and store Pakistan’s largest e-commerce dataset. The pipeline is optimized for **scalable analytics** using AWS Glue, and Athena, with smart partitioning and efficient columnar storage.

---

## 📦 Dataset Overview

- **Source**: Kaggle – *Pakistan’s Largest E-Commerce Dataset*
- **Fields**: `order_id`, `created_at`, `category`, `status`, `customer_id`, `price` etc...
- **Use Case**: Enables insights into order trends, category performance, and business growth metrics.

---

## 🎯 Project Goals

- ✅ Ingest raw CSV data into AWS S3 bucket
- ✅ Partition by `year`, `month`, and `category`
- ✅ Partition, clean and transform with AWS Glue
- ✅ Store in efficient format (Parquet) into another AWS S3 bucket
- ✅ Query using AWS Athena

---

## 🧰 Tech Stack

| Tool         | Purpose                                       |
|--------------|-----------------------------------------------|
| **Pandas**   | Lightweight preview / initial inspection       |
| **AWS S3**   | Cloud storage for input/output datasets        |
| **AWS Glue** | Managed ETL & data catalog for Athena          |
| **AWS Athena** | Serverless querying using standard SQL       |

---

## 📁 Folder Structure

```
team_agile/
│
├── images/                     # Architecture
│   └── agile_team_aws.jpg
│
├── scripts/                    # Python utility scripts
│   └── script.py               # Cleaning and transformation scripts
│   └── partition_data.py       # Partitioning scripts
│   └── transform_partition.py  # transforming partitioning scripts
│
├── tests/                      # Unit and integration tests
│
├── .env                        # Environment variables
├── .env.example                # Sample environment variables template
├── .gitignore                  # Git ignored files
├── config.py                   # Configuration constants and utilities
├── main.py                     # Main entry point for the pipeline
│
├── Makefile                    # CLI shortcuts for build/run/test
├── poetry.lock                 # Poetry lock file (dependency versions)
├── pyproject.toml              # Poetry project metadata & dependencies
├── README.md               
```

## 🔄 Step-by-Step Process Flow

The pipeline follows a typical **Extract → Transform → Load (ETL)** architecture using AWS services:

---

### 🟢 1. Extract: Ingest Raw Data

- 📥 **Download Dataset**  
  Fetch the e-commerce dataset from [text](https://www.kaggle.com/datasets/zusmani/pakistans-largest-ecommerce-dataset/data).

- ☁️ **Upload to S3**  
  Store the raw `.csv` files in a designated AWS S3 bucket (`s3://your-bucket/raw/`).

---

### 🧪 2. Transform: Clean & Process

- 📆 **Partition by Year and Month**  
  Extract `year` and `month`.

- 🧹 **Data Cleaning & Transformation**  
  - Remove nulls or invalid entries  
  - Standardize formats (e.g., lowercase categories)  
  - Convert date columns to proper formats

- 🛠️ **Apply ETL in AWS Glue**  
  Use PySpark scripts/visual ETL in AWS Glue to apply cleaning logic and partition data efficiently.

---

### 📤 3. Load: Save & Catalog

- 🧾 **Store as Parquet in S3**  
  Save the transformed data in columnar `Parquet` format in `s3://your-bucket/ecommerce_partitioned/`, partitioned by `year`, `month`.

- 🗃️ **Create a Data Catalog**  
  - Use **AWS Glue Crawlers** to create a database and table schema from the partitioned Parquet files.  
  - Enables SQL querying via **AWS Athena** or loading into **AWS Redshift**.

---

### 🧪 Optional: Load into AWS Athena (if needed)

- 🧱 **Create Schema in Redshift**  
  Use the Glue metadata to generate SQL schema.

- ⬆️ **Upload Transformed Data**  
  Copy partitioned Parquet data from S3 to AWS Athena for advanced analytics or BI dashboards.


## 📊 Use Cases

### 📈 Analyze Category Trends Over Time
Understand how different product categories perform across months and years to support strategic planning and product management.

### ❗ Monitor Failed or Delayed Orders
Use the `status` field to track and analyze failed or delayed orders, allowing for early identification of operational issues.

### 🌍 Visualize Revenue Across Regions *(if geo data is available)*
Enrich the dataset with regional or location data to map revenue geographically and identify market hotspots.

### 📊 Dashboard-Ready for BI Tools
The partitioned Parquet format enables seamless integration with BI tools like:
- Amazon QuickSight  
- Tableau  
- Microsoft Power BI  
for real-time analytics and data storytelling.


## AUTHORS : AGILE TEAM 