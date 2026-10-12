USE coir_business_analytics;
GO

CREATE TABLE dbo.dim_date (
    date_id INT PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    [day] TINYINT,
    [month] TINYINT,
    month_name VARCHAR(20),
    [quarter] TINYINT,
    [year] SMALLINT,
    [week] TINYINT,
    financial_year VARCHAR(9)
);
GO
