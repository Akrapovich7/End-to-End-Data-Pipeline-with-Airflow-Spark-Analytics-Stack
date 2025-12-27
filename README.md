# 📈 Stock Data Pipeline  
### End-to-End Analytics Platform with Airflow, Spark & Modern Analytics Stack

This project demonstrates the design and implementation of a **modern, containerized data engineering pipeline** for ingesting, processing, and analyzing stock market data.

It follows common **data platform and lakehouse principles**, using industry-standard open-source tools.

The pipeline fetches **NVIDIA (NVDA) stock price data** from a public API, processes it through a scalable transformation layer, and exposes it for analytics and visualization.

---

## 🎯 Project Goals

The primary goals of this project are to:

- Demonstrate a complete **end-to-end data pipeline architecture**
- Showcase **orchestration, transformation, storage, and analytics layers**
- Apply **production-style data engineering practices**
- Provide a reusable foundation for **market and financial analytics**
- Serve as a **portfolio project** for data engineering and analytics roles

---

## 🏗️ Architecture Overview

The solution is built as a **modular, loosely coupled architecture**, where each component has a clearly defined responsibility.

### High-level architecture layers:
- **Ingestion & Orchestration**
- **Raw & Processed Data Storage**
- **Distributed Data Processing**
- **Analytics & Visualization**
- **Monitoring & Notifications**

---

## 🧱 Technology Stack

### 🔄 Orchestration
**Apache Airflow**
- Controls execution order  
- Handles retries and failures  
- Coordinates interactions between all services  

---

### ⚙️ Data Processing
**Apache Spark**
- Performs data transformations  
- Normalizes and prepares datasets for analytics  
- Enables scalable processing logic  

---

### 💾 Storage

**MinIO**
- Acts as object storage / data lake  
- Stores both raw and processed datasets  

**PostgreSQL**
- Serves as the analytics database  
- Optimized for BI queries and reporting  

---

### 📊 Analytics & Visualization
**Metabase**
- Provides dashboards and exploratory analytics  
- Connects directly to PostgreSQL  

---

### 🔔 Integration & Notifications
**Slack**
- Receives pipeline execution notifications  
- Used for monitoring success and failure states  

---

### 🐳 Infrastructure
**Docker & Docker Compose**
- Entire platform runs in isolated containers  
- Simplifies local development and deployment  

---

## 🔄 Data Pipeline Flow

The pipeline follows a clear, linear flow designed for **reliability and transparency**:

1. **API Availability Check**  
   Verifies whether the external stock market API is reachable.

2. **Data Ingestion**  
   Stock price data for NVIDIA (NVDA) is fetched from the Yahoo Finance API.

3. **Raw Data Storage**  
   The unprocessed API response is stored in MinIO, preserving the original structure.

4. **Data Transformation**  
   Apache Spark reads raw data from MinIO and performs:
   - Schema normalization  
   - Data type conversions  
   - Metric extraction (prices, timestamps, metadata)

5. **Processed Data Storage**  
   The transformed dataset is written back to MinIO in a clean, analytics-ready format.

6. **Data Loading**  
   Final datasets are loaded into PostgreSQL for analytical querying.

7. **Notifications**  
   Pipeline execution status is sent to Slack.

8. **Analytics & BI**  
   Metabase connects to PostgreSQL to enable dashboards and ad-hoc analysis.

---

## 📊 Analytics Capabilities

With the processed data available in PostgreSQL, the platform supports:

- Stock price trend analysis  
- Daily and historical comparisons  
- Exploratory BI dashboards  
- Foundation for volatility or return calculations  
- Extension to multi-symbol or multi-market analysis  

Metabase allows **non-technical users** to explore the data visually without writing SQL.

---

## 🧪 Design Considerations

Key architectural decisions include:

- Clear **separation of concerns** between ingestion, processing, and analytics  
- **Object storage as the system of record**  
- **Spark-based transformations** for scalability  
- **Database optimized for BI**, not raw ingestion  
- **Containerized deployment** for portability  

---

## 🚧 Future Improvements

Planned and potential enhancements:

- Support for multiple stock symbols  
- Data quality validation steps  
- Partitioned data lake layout  
- Incremental loading strategy  
- CI/CD validation for Airflow DAGs  
- Cloud deployment (AWS / GCP)  
- Monitoring metrics and observability  

---

## 👩‍💻 Author

**Ali Lučkin**  
Data Engineering & Analytics  

This project was built as a hands-on demonstration of modern data engineering concepts and tooling.
