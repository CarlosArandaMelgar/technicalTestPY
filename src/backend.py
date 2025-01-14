from fastapi import FastAPI, Query
from typing import Optional
import sqlite3
import pandas as pd


app = FastAPI()

DB_PATH = "sales_dashboard.db"

def query_db(query: str, params: tuple = ()):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
    return [dict(row) for row in rows]


# GET /sales/product
@app.get("/sales/product")
def get_sales_by_product(
    product_name: Optional[str] = Query(None),
    category: Optional[str] = Query(None)
):
    query = "SELECT product, category, SUM(total_sales) as total_sales FROM Transactions"
    filters = []
    params = []

    if product_name:
        filters.append("product = ?")
        params.append(product_name)
    if category:
        filters.append("category = ?")
        params.append(category)

    if filters:
        query += " WHERE " + " AND ".join(filters)

    query += " GROUP BY product, category"
    return query_db(query, tuple(params))

# GET /sales/day
@app.get("/sales/day")
def get_sales_by_day(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None)
):
    query = "SELECT date, SUM(total_sales) as total_sales FROM Transactions"
    filters = []
    params = []

    if start_date:
        filters.append("date >= ?")
        params.append(start_date)
    if end_date:
        filters.append("date <= ?")
        params.append(end_date)

    if filters:
        query += " WHERE " + " AND ".join(filters)

    query += " GROUP BY date"
    return query_db(query, tuple(params))

# GET /sales/category
@app.get("/sales/category")
def get_sales_by_category():
    query = "SELECT * FROM AggregatedMetricsByCategory"
    return query_db(query)