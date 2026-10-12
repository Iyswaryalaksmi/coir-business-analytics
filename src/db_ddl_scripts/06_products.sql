USE coir_business_analytics;
GO

CREATE TABLE dbo.products (
    product_id INT IDENTITY(1,1) PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category_id INT,
    unit_of_measure VARCHAR(50),
    standard_cost DECIMAL(12,2),
    selling_price DECIMAL(12,2),
    CONSTRAINT FK_products_product_categories
        FOREIGN KEY (category_id) REFERENCES dbo.product_categories(category_id)
);
GO
