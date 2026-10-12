USE coir_business_analytics;
GO

CREATE TABLE dbo.customers (
    customer_id INT IDENTITY(1,1) PRIMARY KEY,
    customer_name VARCHAR(150) NOT NULL,
    segment_id INT,
    location_id INT,
    customer_type VARCHAR(50),
    registration_date DATE,
    CONSTRAINT FK_customers_customer_segments
        FOREIGN KEY (segment_id) REFERENCES dbo.customer_segments(segment_id),
    CONSTRAINT FK_customers_locations
        FOREIGN KEY (location_id) REFERENCES dbo.locations(location_id)
);
GO
