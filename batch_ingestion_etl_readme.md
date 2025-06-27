## 📦 Batch Ingestion Pipeline for E-commerce Transactions

This project implements a serverless **ETL (Extract, Transform, Load) pipeline** to process simulated e-commerce transaction data using **AWS Glue** and load it into **Amazon Redshift Serverless** for analytics and reporting.

---

### 📌 Project Overview

- **Data Source:** Raw transaction CSV files stored in Amazon S3
- **ETL Tool:** AWS Glue (PySpark ETL script)
- **Data Warehouse:** Amazon Redshift Serverless
- **Objective:** Clean, transform, and load e-commerce transaction data for scalable and efficient analytics

---

### 🔄 ETL Pipeline Workflow

1. **Extract**

   - Read raw `.csv` files from an S3 bucket containing transaction-level data (e.g., order IDs, user IDs, amounts, statuses, timestamps).

2. **Transform** (in AWS Glue with PySpark)

   - Normalize and clean column names
   - Remove nulls, duplicates, and invalid characters
   - Cast columns to Redshift-compatible data types
   - Derive new metrics (e.g., total amount per user, transaction category)
   - Perform basic aggregations for downstream analytics

3. **Load**

   - Write the cleaned and transformed data to **Redshift Serverless** via JDBC
   - Table: `payments` (or custom-defined)

---

### 🧠 Key Features

- **Serverless & Scalable:** Uses Glue Spark jobs and Redshift Serverless—no infrastructure to manage
- **Cloud-native:** Built entirely on AWS
- **Optimized Write:** Uses repartitioning and batching to reduce JDBC write overhead
- **Data Quality Handling:** Trims whitespace, removes non-UTF8 characters, fills in missing values
- **Modular Design:** Easily extendable to add joins, lookups, or enrichments

---

### 🗪 Technologies Used

| Tool                       | Purpose                          |
| -------------------------- | -------------------------------- |
| AWS Glue                   | ETL jobs with PySpark            |
| Amazon S3                  | Data lake storage                |
| Amazon Redshift Serverless | Scalable SQL warehouse           |
| PySpark                    | Transformations & data cleansing |
| JDBC Connector             | Redshift write operation         |

---

### 📁 Project Structure

```
Batch-Ingestion-Pipeline-for-E-commerce-Transactions/
🔽
├── scripts/
│   └── glue_etl_job.py              # PySpark job used in AWS Glue
│
├── data/
│   └── transactions_sample.csv      # Sample input file (optional)
│
├── README.md                        # Project documentation
└── requirements.txt                 # (Optional) Python packages used locally
```

---

### 🚀 How to Run

#### 🧰 Prerequisites:

- AWS account with access to Glue, S3, and Redshift Serverless
- IAM roles with proper permissions
- JDBC connection setup in Redshift Serverless

#### 🛠️ Steps:

1. Upload your CSV file(s) to S3
2. Set up a Redshift Serverless database and JDBC connection
3. Create an AWS Glue job with the provided PySpark script
4. Run the Glue job
5. Query the `payments` table in Redshift

---

### 📚 Future Improvements

- Add schema evolution and dynamic partitioning
- Integrate with AWS Lake Formation for data governance
- Automate pipeline with AWS Step Functions or Glue Workflows
- Extend data model to include user profiles or product data

---

### ✍️ Author

**Kondra Rakshith Reddy**\
AWS Data Engineer |


