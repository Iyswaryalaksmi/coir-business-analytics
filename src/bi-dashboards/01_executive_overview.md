# Coir Business Analytics: Executive Dashboard

## Dashboard Scenario

An executive reviews monthly coir sales to decide whether a revenue increase
reflects broader demand or a change in order size or product mix. The attached
dashboard compares total revenue, order count, average order value, and quantity
sold for each month. In the illustrative January-to-February view, revenue rises
while order count and quantity sold fall. This may indicate larger or higher-value
orders, but the transaction data must be checked before making that conclusion.

The screenshot is a design reference, not verified project output. The project
currently has no transaction files in `data/`, so do not report values read from
the screenshot as findings. Rebuild the visuals from validated business data or
label any demonstration data and results as synthetic/illustrative.

## Dashboard Layout

Use a 2-by-2 grid of monthly column charts, with a shared Year and Month axis:

| Visual | Measure | Purpose |
| --- | --- | --- |
| Total Revenue | Sum of sales value for completed/shipped orders | Track monthly sales value |
| Total Orders | Distinct count of completed/shipped order IDs | Track transaction volume |
| Average Order Value | Total Revenue divided by Total Orders | Compare average order size/value |
| Quantity Sold | Sum of item quantities for completed/shipped orders | Track unit movement |

Use the same order-status definition, date field, month sorting, and date filters
across all four visuals. Format revenue and average order value as INR, and label
quantity with the product's unit of measure. If the business sells different
products in incompatible units, show quantity by product or category rather than
adding unlike units into one total.

## Data and Power BI Setup

Use `sales_orders` for the order date, order ID, status, and order total, and
`sales_order_items` for item quantities. Apply the same completed/shipped status
filter to both measures. Aggregate order totals by month separately from item
quantities, or aggregate each source to the order/month grain before joining, so
multiple order items do not multiply order revenue. Connect both to the date
dimension where available and use a Year-Month field sorted chronologically.

Create these measures (adjust names to the imported model):

```DAX
Total Revenue =
CALCULATE(
	SUM(sales_orders[total_amount]),
	sales_orders[order_status] IN { "Completed", "Shipped" }
)

Total Orders =
CALCULATE(
	DISTINCTCOUNT(sales_orders[order_id]),
	sales_orders[order_status] IN { "Completed", "Shipped" }
)

Average Order Value = DIVIDE([Total Revenue], [Total Orders])

Quantity Sold =
CALCULATE(
	SUM(sales_order_items[quantity]),
	sales_orders[order_status] IN { "Completed", "Shipped" }
)
```

The quantity measure requires an active relationship from `sales_orders` to
`sales_order_items` on `order_id`. If the business defines revenue from line
amounts instead of the order header, use the validated line amount consistently
and avoid summing both header and line revenue.

## Where It Fits in the Report

1. **Chapter 4 – Proposed Research Methodology:** In Section 4.5.6, state that
   Power BI will present monthly revenue, distinct completed/shipped orders,
   average order value, and quantity sold using a common date and status scope.
2. **Chapter 5 – Results and Discussion (Output):** Add a new first subsection,
   **5.1 Executive Dashboard**, before the detailed sales, product, customer,
   regional, inventory, and forecast results. Insert the exported dashboard
   screenshot with the caption below, followed by the scenario interpretation.
3. **Appendix:** Include the full-size dashboard export and, if required, the
   measure definitions or dashboard field mapping. Keep the main chapter focused
   on the readable dashboard and its business meaning.

Suggested figure caption: **Figure 5.1: Monthly executive dashboard of revenue,
orders, average order value, and quantity sold (2026; based on [actual/synthetic]
data).** Replace the bracketed data description and year with the actual study
period before submission.

## Report-Ready Scenario Interpretation

In the illustrative dashboard, February revenue is higher than January, although
fewer orders and a lower quantity are recorded. The increase in average order
value suggests that the average completed/shipped order had a higher value in
February. Management should check the product mix, unit prices, discounts, and
large orders before attributing the change to customer preference or sustained
demand. If these patterns are confirmed in actual records, the business can
review stock availability for high-value products while monitoring whether the
lower order and unit volumes continue in subsequent months.

**Data limitation:** Completed/shipped sales measure recorded sales, not total
market demand; they do not reveal lost sales from stockouts or unfulfilled orders.
