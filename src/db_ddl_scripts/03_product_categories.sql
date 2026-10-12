USE coir_business_analytics;
GO

CREATE TABLE dbo.product_categories (
    category_id INT IDENTITY(1,1) PRIMARY KEY,
    category_name VARCHAR(100),
    description VARCHAR(255)
);
GO
