COIR BUSINESS ANALYTICS — SQL SERVER TABLE SCRIPTS

Contents:
- 00_create_database.sql: creates the database if it does not already exist.
- 01–20: one CREATE TABLE script per table (20 tables total).

How to run in SQL Server Management Studio (SSMS):
1. Extract this ZIP file.
2. Open and execute 00_create_database.sql first.
3. Execute the remaining scripts in numeric order: 01, 02, ... 20.
4. Verify the tables with:

USE coir_business_analytics;
GO
SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_NAME;

Important:
- Scripts are for Microsoft SQL Server / SSMS and use SQL Server's GO batch separator.
- Run the scripts only once on a fresh database. They do not drop or recreate existing tables.
- Foreign-key dependencies are handled by the numeric execution order.
- These files create table structures only; they do not insert sample data.
