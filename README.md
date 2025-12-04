# Inventory-Management-System

A simple inventory tracking system built with Python and SQLite to manage product stock levels, pricing, and automated low-stock alerts.

## Features

- Add new products with name, category, quantity, and price
- View all products with stock status (OUT/LOW/OK)
- Search products by name
- Add stock (restocking)
- Remove stock (sales)
- Automated low-stock alerts
- Calculate total inventory value

## Technologies Used

- **Python 3.x**
- **SQLite3** (built-in, no installation needed)

## How to Run

1. Make sure Python 3 is installed on your system
2. Download the `inventory_system.py` file
3. Run the program:
```bash
   python inventory_system.py
```
4. Follow the on-screen menu to manage inventory

## Database Structure

The application uses a single table:

**products**
- `id` - Primary key (auto-generated)
- `name` - Product name
- `category` - Product category
- `quantity` - Current stock quantity
- `price` - Price per unit
- `min_stock` - Minimum stock level for alerts

## Sample Usage
```
*** INVENTORY SYSTEM ***

1. Add Product
2. View All Products
3. Search Product
4. Add Stock
5. Sell Product (Remove Stock)
6. Low Stock Alert
7. Total Inventory Value
8. Exit

Choice: 1
Product Name: Laptop
Category: Electronics
Quantity: 50
Price: 45000
Min Stock Level [10]: 5
✓ Product 'Laptop' added!
```

## Stock Status Logic

- **OUT** - Quantity = 0 (out of stock)
- **LOW** - Quantity ≤ Min Stock Level (needs restocking)
- **OK** - Quantity > Min Stock Level (sufficient stock)

## What I Learned

- Working with SQLite databases in Python
- CRUD operations with business logic
- Stock validation (preventing negative inventory)
- SQL aggregate functions (SUM for inventory value)
- Conditional logic for status checking
- Real-world application of inventory management

## Future Improvements

- Add transaction history tracking
- Generate reports (sales, restocking)
- Add product suppliers
- Export inventory to CSV/Excel
- Add barcode/SKU support

## Author

Amit Pharkya
