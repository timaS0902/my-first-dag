# 🚀 Airflow Hello-World ETL (Extract → Transform → Load)

A minimal example of running **Apache Airflow** using **Docker Compose**.  
This demo DAG performs a simple ETL workflow:

1. **Extract** — generates a simple message `hello world`  
2. **Transform** — converts it to uppercase  
3. **Load** — writes the result to PostgreSQL (`demo.hello_events` table)

---

## 🧩 Project Structure

```
airflow-hello-world/
├─ docker-compose.yaml
├─ .env
├─ dags/
│  └─ hello_world_etl.py
├─ logs/        
└─ plugins/    
```

---

## ⚙️ Prerequisites

- Docker Desktop (latest version)
- `docker compose` v2 or higher
- Free ports:
  - **8081** → Airflow Web UI
  - **5431** → PostgreSQL (external port)

---

## 🚀 Setup Instructions

### 1. Copy the environment file

```bash
cp .env.example .env
```

`.env` already includes:

```env
AIRFLOW_UID=50000
_PIP_ADDITIONAL_REQUIREMENTS=apache-airflow-providers-postgres==5.*
AIRFLOW_CONN_PG_DEMO=postgresql+psycopg2://airflow:airflow@postgres:5432/airflow
AIRFLOW__API__AUTH_BACKENDS=airflow.api.auth.backend.basic_auth,airflow.api.auth.backend.session
```

### 2. Initialize Airflow

```bash
docker compose up airflow-init
```

### 3. Start the cluster

```bash
docker compose up -d
```

### 4. Copy file 

Create a new file and copy the code from hello_world_etl.example.py in the dags folder.

### 5. Access the Web UI

Open: [http://localhost:8081](http://localhost:8081)  
Credentials: **airflow / airflow**

### 6. Restart airflow-scheduler

```bash
docker compose restart airflow-scheduler
```

---

## ▶️ Run the DAG

1. Go to the **DAGs** tab → enable `hello_world_etl`  
2. Click ▶ **Trigger DAG**  
3. Wait until all tasks (`extract → transform → load`) turn **green**

---

## 🔍 Verify Data in PostgreSQL

### Linux / macOS:

```bash
docker compose exec postgres psql -U airflow -d airflow -c 'select id, run_id, message_upper, msg_len, inserted_at from demo.hello_events order by id desc limit 5;'
```

### Windows PowerShell:

```powershell
docker compose exec postgres psql -U airflow -d airflow -c 'select id, run_id, message_upper, msg_len, inserted_at from demo.hello_events order by id desc limit 5;'
```

---

## ✅ Success Criteria

| Step | Check |
|------|-------|
| 1 | Containers `airflow-webserver`, `airflow-scheduler`, `airflow-worker`, `postgres`, and `redis` are **Up (healthy)** |
| 2 | DAG `hello_world_etl` is visible in the UI |
| 3 | All 3 tasks succeed (green) |
| 4 | PostgreSQL contains a new row in `demo.hello_events` |

---

## 🧹 Stop and Clean Up

```bash
docker compose down -v
```

---

## 🧰 Useful Commands

List all DAGs:
```bash
docker compose exec airflow-scheduler airflow dags list
```

Check import errors:
```bash
docker compose exec airflow-scheduler airflow dags list-import-errors
```

View task logs:
```bash
docker compose exec airflow-worker cat /opt/airflow/logs/dag_id=hello_world_etl/task_id=load/latest/1.log
```

---

## 🧑‍💻 Homework for Students

1. Run the provided Airflow project locally.  
2. Trigger the existing DAG `hello_world_etl`.  
3. Provide screenshots:
   - Airflow UI with all tasks succeeded (green)
   - SQL output from `demo.hello_events`  
4. Submit the screenshots + a short note describing how you ran it.

---
