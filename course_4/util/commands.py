CREATE_TRADING_RESULTS_TABLE = """
CREATE TABLE IF NOT EXISTS spimex_trading_results(
id SERIAL PRIMARY KEY,
exchange_product_id TEXT NOT NULL,
exchange_product_name TEXT NOT NULL,
oil_id TEXT NOT NULL,
delivery_basis_id TEXT NOT NULL,
delivery_basis_name TEXT NOT NULL,
delivery_type_id TEXT NOT NULL,
volume INT NOT NULL,
total INT NOT NULL,
count INT NOT NULL,
date DATE NOT NULL,
created_on TIMESTAMP NOT NULL,
updated_on TIMESTAMP NOT NULL
);"""
