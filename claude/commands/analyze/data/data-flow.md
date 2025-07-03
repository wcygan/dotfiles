# /data-flow

Analyze, design, and implement data processing pipelines with automatic source detection, transformation logic, and destination configuration.

## Usage

```
/data-flow [source-type]
/data-flow [source] to [destination]
/data-flow
```

## Context Detection

**When no argument provided:**

- Scans project for data sources (databases, APIs, files)
- Discovers existing data processing code
- Suggests common data flow patterns for detected tech stack

**When source specified:**

- Auto-detects source format and connection requirements
- Suggests appropriate transformation patterns
- Recommends compatible destinations

**When source and destination specified:**

- Focuses on optimal transformation pipeline
- Provides data format conversion strategies
- Suggests monitoring and error handling

## Data Source Discovery

### Database Sources

**Relational Databases**

```sql
-- PostgreSQL/MySQL discovery
SELECT table_name, column_name, data_type 
FROM information_schema.columns 
WHERE table_schema = 'public';

-- Connection configuration detection
grep -r "DATABASE_URL\|DB_HOST\|DB_NAME" .env* config/
```

**NoSQL Databases**

```javascript
// MongoDB collection analysis
db.getCollectionNames()
db.[collection].findOne() // Sample document structure

// Redis key pattern discovery  
redis-cli --scan --pattern "*" | head -20
```

### File-Based Sources

**Structured Files**

- CSV/TSV: Column analysis and data type inference
- JSON/JSONL: Schema extraction and nested structure mapping
- Parquet/Avro: Metadata inspection and column statistics
- XML: XPath mapping and element hierarchy analysis

**Log Files**

- Application logs: Pattern recognition and field extraction
- Web server logs: Common log format parsing
- System logs: Structured logging format detection
- Custom formats: Regex pattern development

### API Sources

**REST APIs**

```bash
# API endpoint discovery
curl -H "Accept: application/json" [endpoint] | jq '.' | head -20

# Schema inspection
curl -H "Accept: application/json" [endpoint]/schema
curl -H "Accept: application/json" [endpoint]?_limit=1
```

**GraphQL APIs**

```graphql
# Schema introspection
query IntrospectionQuery {
  __schema {
    types {
      name
      kind
      fields {
        name
        type {
          name
        }
      }
    }
  }
}
```

### Stream Sources

**Message Queues**

- Kafka: Topic discovery and message schema analysis
- RabbitMQ: Queue inspection and message format detection
- Redis Streams: Stream key analysis and entry structure
- Apache Pulsar: Namespace and topic enumeration

**Real-time Streams**

- WebSocket connections: Message format analysis
- Server-Sent Events: Event type categorization
- Apache Kafka Connect: Connector configuration discovery
- Change Data Capture: Database event stream analysis

## Data Transformation Patterns

### Data Cleaning and Validation

**Data Quality Assessment**

```python
# Missing value analysis
data.isnull().sum()
data.dtypes
data.describe()

# Duplicate detection
data.duplicated().sum()
data[data.duplicated()].head()

# Outlier identification
Q1 = data.quantile(0.25)
Q3 = data.quantile(0.75)
IQR = Q3 - Q1
outliers = data[((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR))).any(axis=1)]
```

**Data Standardization**

- Date/time format normalization
- String case and encoding standardization
- Numeric precision and scale alignment
- Category value normalization

### Schema Transformation

**Structure Changes**

- Column renaming and type conversion
- Nested JSON flattening/nesting
- Array/list processing and expansion
- Pivot/unpivot operations

**Data Enrichment**

- Lookup table joins and enrichment
- Calculated field generation
- Data validation and flagging
- Reference data integration

### Aggregation and Summarization

**Temporal Aggregations**

```sql
-- Time-based grouping patterns
SELECT 
    DATE_TRUNC('hour', timestamp) as hour,
    COUNT(*) as event_count,
    AVG(value) as avg_value
FROM events 
GROUP BY DATE_TRUNC('hour', timestamp)
ORDER BY hour;
```

**Dimensional Analysis**

- Group-by operations with multiple dimensions
- Rolling window calculations
- Percentile and statistical computations
- Custom business logic aggregations

## Pipeline Architecture Patterns

### Batch Processing

**ETL (Extract, Transform, Load)**

```python
# Traditional ETL pattern
def etl_pipeline():
    # Extract
    raw_data = extract_from_source(source_config)
    
    # Transform
    cleaned_data = clean_and_validate(raw_data)
    transformed_data = apply_business_rules(cleaned_data)
    
    # Load
    load_to_destination(transformed_data, dest_config)
```

**ELT (Extract, Load, Transform)**

```sql
-- ELT pattern using SQL transformations
CREATE TABLE staging.raw_data AS 
SELECT * FROM source_system.table;

CREATE TABLE warehouse.processed_data AS
SELECT 
    id,
    UPPER(name) as normalized_name,
    CAST(amount AS DECIMAL(10,2)) as amount_decimal
FROM staging.raw_data
WHERE status = 'active';
```

### Stream Processing

**Real-time Transformations**

```python
# Kafka Streams pattern
from kafka import KafkaConsumer, KafkaProducer

consumer = KafkaConsumer('input-topic')
producer = KafkaProducer('output-topic')

for message in consumer:
    # Transform message
    transformed = transform_data(message.value)
    
    # Send to output topic
    producer.send('output-topic', transformed)
```

**Micro-batch Processing**

- Small batch windows for near real-time processing
- Checkpoint and recovery mechanisms
- Backpressure handling and flow control
- State management for stateful operations

### Hybrid Architectures

**Lambda Architecture**

- Batch layer for comprehensive historical processing
- Speed layer for real-time approximate results
- Serving layer for unified query interface

**Kappa Architecture**

- Stream-first approach with reprocessing capabilities
- Event sourcing and log-based data storage
- Unified real-time and batch processing

## Destination Configuration

### Data Warehouses

**Structured Storage**

```sql
-- Table creation with appropriate types
CREATE TABLE fact_sales (
    sale_id BIGINT PRIMARY KEY,
    customer_id INT REFERENCES dim_customer(customer_id),
    product_id INT REFERENCES dim_product(product_id),
    sale_date DATE,
    amount DECIMAL(10,2),
    quantity INT
);

-- Partitioning for performance
CREATE TABLE fact_sales_partitioned (
    LIKE fact_sales
) PARTITION BY RANGE (sale_date);
```

**Indexing Strategy**

- Primary key and foreign key indexes
- Query-specific composite indexes
- Partial indexes for filtered queries
- Full-text search indexes

### Data Lakes

**File Organization**

```
data-lake/
├── raw/
│   ├── year=2024/month=01/day=15/
│   └── source=api/format=json/
├── processed/
│   ├── year=2024/month=01/
│   └── table=customers/
└── curated/
    ├── marts/
    └── aggregations/
```

**Format Selection**

- Parquet for analytical workloads
- Avro for schema evolution
- Delta Lake for ACID transactions
- Iceberg for large-scale analytics

### Operational Databases

**Transactional Systems**

- ACID compliance requirements
- Connection pooling and retry logic
- Batch insert optimization
- Conflict resolution strategies

**NoSQL Destinations**

- Document structure optimization
- Sharding and distribution strategies
- Consistency level configuration
- Index design for query patterns

## Monitoring and Observability

### Pipeline Health Monitoring

**Data Quality Metrics**

```python
# Data quality checks
def validate_data_quality(df):
    metrics = {
        'row_count': len(df),
        'null_percentage': df.isnull().sum().sum() / (len(df) * len(df.columns)),
        'duplicate_count': df.duplicated().sum(),
        'schema_drift': detect_schema_changes(df)
    }
    return metrics
```

**Performance Monitoring**

- Processing throughput and latency
- Resource utilization (CPU, memory, I/O)
- Error rates and retry patterns
- Data freshness and staleness metrics

### Alerting and Error Handling

**Alert Conditions**

- Data volume anomalies (too high/low)
- Processing time threshold breaches
- Data quality threshold violations
- Pipeline failure and retry exhaustion

**Error Recovery**

- Dead letter queues for failed messages
- Idempotent processing design
- Checkpoint and restart capabilities
- Manual intervention procedures

## Framework-Specific Implementation

### Python Ecosystem

**Pandas/Dask**

```python
import pandas as pd
import dask.dataframe as dd

# Large dataset processing
df = dd.read_csv('large_file.csv')
result = df.groupby('category').amount.sum().compute()
```

**Apache Airflow**

```python
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

dag = DAG('data_pipeline', schedule_interval='@daily')

extract_task = PythonOperator(
    task_id='extract',
    python_callable=extract_data,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform',
    python_callable=transform_data,
    dag=dag
)

extract_task >> transform_task
```

### JVM Ecosystem

**Apache Spark**

```scala
import org.apache.spark.sql.SparkSession

val spark = SparkSession.builder()
  .appName("DataPipeline")
  .getOrCreate()

val df = spark.read
  .option("header", "true")
  .csv("input.csv")

val result = df
  .filter($"status" === "active")
  .groupBy($"category")
  .sum("amount")

result.write
  .mode("overwrite")
  .parquet("output/")
```

### Cloud-Native Solutions

**AWS**

- Glue: Serverless ETL service
- Kinesis: Real-time data streaming
- Lambda: Event-driven processing
- S3: Data lake storage

**GCP**

- Dataflow: Unified stream and batch processing
- Pub/Sub: Messaging and event ingestion
- BigQuery: Data warehouse and analytics
- Cloud Functions: Serverless processing

**Azure**

- Data Factory: Data integration service
- Stream Analytics: Real-time analytics
- Synapse: Analytics platform
- Event Hubs: Big data streaming

## Output and Recommendations

**Pipeline Design Document**

- Source and destination specifications
- Transformation logic and business rules
- Error handling and monitoring strategy
- Performance optimization recommendations

**Implementation Code**

- Framework-specific pipeline code
- Configuration files and connection strings
- Testing framework and data validation
- Deployment and orchestration scripts

**Operational Runbook**

- Monitoring dashboard configuration
- Alert threshold definitions
- Troubleshooting procedures
- Performance tuning guidelines

The command adapts its recommendations based on detected data sources, existing infrastructure, and performance requirements, providing a complete data flow solution tailored to the specific environment.
