from fastapi import APIRouter
from backend.schemas.request import QueryRequest
import os
import re
import psycopg2

# Import Existing System
from backend.scripts.orchestrator.query_router import QueryRouter

router=APIRouter()
SALES_DATA_TABLE = "walmart_sales_refined"

# Initialize once
query_router=QueryRouter()


def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "chaitra_db"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "root64"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
    )


def quick_sales_answer(user_query: str):
    q = user_query.lower()
    store_match = re.search(r"store\s+(\d+)", q)
    if not store_match:
        return None

    store_id = int(store_match.group(1))
    if "sales" not in q:
        return None

    conn = get_db_connection()
    cursor = conn.cursor()
    table = SALES_DATA_TABLE
    try:
        cursor.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s
            """,
            (table,),
        )
        cols = {r[0] for r in cursor.fetchall()}
        if "store" not in cols:
            return (
                "Store-level query is unavailable for current analytics table "
                f"({table}) because it does not contain a store column."
            )

        # last month sales for store X
        if "last month" in q:
            cursor.execute(
                f"""
                WITH latest AS (
                    SELECT MAX(date) AS max_date FROM {table}
                )
                SELECT COALESCE(SUM(weekly_sales), 0)
                FROM {table}, latest
                WHERE store = %s
                  AND date >= date_trunc('month', latest.max_date) - interval '1 month'
                  AND date < date_trunc('month', latest.max_date)
                """,
                (store_id,),
            )
            total = cursor.fetchone()[0] or 0
            return (
                f"Store {store_id} total sales for last month: {round(float(total), 2)}."
            )

        # this month sales for store X
        if "this month" in q or "current month" in q:
            cursor.execute(
                f"""
                WITH latest AS (
                    SELECT MAX(date) AS max_date FROM {table}
                )
                SELECT COALESCE(SUM(weekly_sales), 0)
                FROM {table}, latest
                WHERE store = %s
                  AND date >= date_trunc('month', latest.max_date)
                  AND date <= latest.max_date
                """,
                (store_id,),
            )
            total = cursor.fetchone()[0] or 0
            return (
                f"Store {store_id} total sales for current month-to-date: {round(float(total), 2)}."
            )

        if "average" in q or "avg" in q:
            cursor.execute(
                f"SELECT COALESCE(AVG(weekly_sales), 0) FROM {table} WHERE store = %s",
                (store_id,),
            )
            avg_val = cursor.fetchone()[0] or 0
            return f"Average weekly sales for store {store_id}: {round(float(avg_val), 2)}."

        if "max" in q or "highest" in q:
            cursor.execute(
                f"SELECT COALESCE(MAX(weekly_sales), 0) FROM {table} WHERE store = %s",
                (store_id,),
            )
            max_val = cursor.fetchone()[0] or 0
            return f"Highest weekly sales for store {store_id}: {round(float(max_val), 2)}."

        if "min" in q or "lowest" in q:
            cursor.execute(
                f"SELECT COALESCE(MIN(weekly_sales), 0) FROM {table} WHERE store = %s",
                (store_id,),
            )
            min_val = cursor.fetchone()[0] or 0
            return f"Lowest weekly sales for store {store_id}: {round(float(min_val), 2)}."

        if "total" in q:
            cursor.execute(
                f"SELECT COALESCE(SUM(weekly_sales), 0) FROM {table} WHERE store = %s",
                (store_id,),
            )
            total_all = cursor.fetchone()[0] or 0
            return f"Total sales for store {store_id} (all available data): {round(float(total_all), 2)}."

        if "trend" in q:
            cursor.execute(
                f"""
                SELECT year, month, ROUND(SUM(weekly_sales)::numeric, 2) AS sales
                FROM {table}
                WHERE store = %s
                GROUP BY year, month
                ORDER BY year DESC, month DESC
                LIMIT 3
                """,
                (store_id,),
            )
            rows = cursor.fetchall()
            if not rows:
                return f"No trend data found for store {store_id}."
            trend_text = ", ".join([f"{int(r[0])}-{int(r[1]):02d}: {float(r[2])}" for r in rows[::-1]])
            return f"Recent monthly sales trend for store {store_id}: {trend_text}."

        return None
    finally:
        conn.close()

@router.post("/query")
def handle_query(request:QueryRequest):
    
    user_query=request.query
    user_id = request.user_id or "default_user"
    chat_mode = request.chat_mode or "auto"
    quick_response = quick_sales_answer(user_query)
    if quick_response:
        query_router.memory.save_chat(user_id, "user", user_query, quick_response)
        return {
            "query": user_query,
            "user_id": user_id,
            "response": quick_response,
            "source": "sql",
            "status": "success"
        }

    # Keep default path responsive for UI while heavy models run.
    mode_override = None if chat_mode == "auto" else chat_mode
    response=query_router.route(user_query, user_id=user_id, mode_override=mode_override)
    return {
        "query":user_query,
        "user_id": user_id,
        "response":response,
        "source":"rag" if "why" in user_query.lower() else "llm",
        "status":"success"
    }