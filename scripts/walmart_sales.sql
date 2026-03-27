DROP TABLE IF EXISTS walmart_sales;

CREATE TABLE walmart_sales (
    store INT,
    dept INT,
    date DATE,
    weekly_sales FLOAT,
    isholiday BOOLEAN,
    temperature FLOAT,
    fuel_price FLOAT,
    cpi FLOAT,
    unemployment FLOAT,
    type VARCHAR(10),
    size INT,
    week INT,
    month INT,
    year INT
);
