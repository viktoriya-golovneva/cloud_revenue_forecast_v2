import duckdb
from pathlib import Path

_PROJECT_ROOT = Path(__file__).parent
_DATA_DIR = _PROJECT_ROOT / "data"
_DB_PATH = _PROJECT_ROOT / "nimbus.duckdb"

_TABLES = {
    "billing_customers":       "billing_customers.csv",
    "monthly_usage":           "monthly_usage.csv",
    "price_list":              "price_list.csv",
    "contracts":               "contracts.csv",
    "invoices":                "invoices.csv",
    "crm_accounts":            "crm_accounts.csv",
    "crm_opportunities":       "crm_opportunities.csv",
    "crm_opportunity_products":"crm_opportunity_products.csv",
    "business_events":         "business_events.csv",
}


def get_con() -> duckdb.DuckDBPyConnection:
    for path in [_DB_PATH, _DB_PATH.with_suffix(".duckdb.wal")]:
        if path.exists():
            path.unlink()

    con = duckdb.connect(str(_DB_PATH))

    print("Setting up database tables...")
    for table_name, filename in _TABLES.items():
        csv_path = _DATA_DIR / filename
        con.execute(
            f"CREATE TABLE {table_name} AS "
            f"SELECT * FROM read_csv_auto('{csv_path.as_posix()}')"
        )
    print("Done. All tables are ready.")

    return con
