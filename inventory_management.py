import sqlite3

class InventorySystem:
    def __init__(self):
        """Initialize inventory system"""
        self.conn = sqlite3.connect("inventory.db")
        self.cursor = self.conn.cursor()
        self.setup_database()
    
    def setup_database(self):
        """Create products table"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER DEFAULT 0,
                price REAL NOT NULL,
                min_stock INTEGER DEFAULT 10
            )
        ''')
        self.conn.commit()
    
    def add_product(self, name, category, quantity, price, min_stock):
        """Add new product"""
        self.cursor.execute('''
            INSERT INTO products (name, category, quantity, price, min_stock)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, category, quantity, price, min_stock))
        self.conn.commit()
        print(f"✓ Product '{name}' added!")
    
    def view_all_products(self):
        """Show all products"""
        self.cursor.execute("SELECT id, name, category, quantity, price, min_stock FROM products")
        products = self.cursor.fetchall()
        
        if products:
            print("\n" + "="*80)
            print(f"{'ID':<5} {'Name':<20} {'Category':<15} {'Stock':<10} {'Price':<10} {'Status'}")
            print("-"*80)
            for p in products:
                # Check stock status
                if p[3] == 0:
                    status = "OUT"
                elif p[3] <= p[5]:
                    status = "LOW"
                else:
                    status = "OK"
                
                print(f"{p[0]:<5} {p[1]:<20} {p[2]:<15} {p[3]:<10} ₹{p[4]:<9.2f} {status}")
            print("="*80)
        else:
            print("\n✗ No products found!")
    
    def search_product(self, keyword):
        """Search products by name"""
        self.cursor.execute('''
            SELECT id, name, category, quantity, price 
            FROM products 
            WHERE name LIKE ?
        ''', (f"%{keyword}%",))
        
        products = self.cursor.fetchall()
        
        if products:
            print("\n" + "="*70)
            print(f"{'ID':<5} {'Name':<25} {'Category':<15} {'Stock':<10} {'Price'}")
            print("-"*70)
            for p in products:
                print(f"{p[0]:<5} {p[1]:<25} {p[2]:<15} {p[3]:<10} ₹{p[4]:.2f}")
            print("="*70)
        else:
            print("\n✗ No products found!")
    
    def add_stock(self, product_id, quantity):
        """Add stock to product"""
        self.cursor.execute("SELECT name, quantity FROM products WHERE id = ?", (product_id,))
        result = self.cursor.fetchone()
        
        if result:
            new_quantity = result[1] + quantity
            self.cursor.execute("UPDATE products SET quantity = ? WHERE id = ?", (new_quantity, product_id))
            self.conn.commit()
            print(f"✓ Added {quantity} units. New stock: {new_quantity}")
        else:
            print("✗ Product not found!")
    
    def remove_stock(self, product_id, quantity):
        """Remove stock (for sales)"""
        self.cursor.execute("SELECT name, quantity FROM products WHERE id = ?", (product_id,))
        result = self.cursor.fetchone()
        
        if result:
            current = result[1]
            if current >= quantity:
                new_quantity = current - quantity
                self.cursor.execute("UPDATE products SET quantity = ? WHERE id = ?", (new_quantity, product_id))
                self.conn.commit()
                print(f"✓ Sold {quantity} units. Remaining: {new_quantity}")
            else:
                print(f"✗ Not enough stock! Only {current} units available.")
        else:
            print("✗ Product not found!")
    
    def low_stock_alert(self):
        """Show products with low stock"""
        self.cursor.execute('''
            SELECT id, name, quantity, min_stock 
            FROM products 
            WHERE quantity <= min_stock
        ''')
        
        products = self.cursor.fetchall()
        
        if products:
            print("\n⚠ LOW STOCK ALERT")
            print("="*60)
            print(f"{'ID':<5} {'Name':<30} {'Stock':<15} {'Min Level'}")
            print("-"*60)
            for p in products:
                print(f"{p[0]:<5} {p[1]:<30} {p[2]:<15} {p[3]}")
            print("="*60)
        else:
            print("\n✓ All products have sufficient stock!")
    
    def total_inventory_value(self):
        """Calculate total value"""
        self.cursor.execute("SELECT SUM(quantity * price) FROM products")
        total = self.cursor.fetchone()[0]
        print(f"\nTotal Inventory Value: ₹{total:,.2f}" if total else "\nTotal Inventory Value: ₹0.00")
    
    def close(self):
        """Close database"""
        self.conn.close()


def main():
    inventory = InventorySystem()
    
    print("\n*** INVENTORY SYSTEM ***\n")
    
    while True:
        print("\n1. Add Product")
        print("2. View All Products")
        print("3. Search Product")
        print("4. Add Stock")
        print("5. Sell Product (Remove Stock)")
        print("6. Low Stock Alert")
        print("7. Total Inventory Value")
        print("8. Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == '1':
            name = input("Product Name: ")
            category = input("Category: ")
            quantity = int(input("Quantity: "))
            price = float(input("Price: "))
            min_stock = int(input("Min Stock Level [10]: ") or 10)
            inventory.add_product(name, category, quantity, price, min_stock)
        
        elif choice == '2':
            inventory.view_all_products()
        
        elif choice == '3':
            keyword = input("Search: ")
            inventory.search_product(keyword)
        
        elif choice == '4':
            product_id = int(input("Product ID: "))
            quantity = int(input("Quantity to add: "))
            inventory.add_stock(product_id, quantity)
        
        elif choice == '5':
            product_id = int(input("Product ID: "))
            quantity = int(input("Quantity to sell: "))
            inventory.remove_stock(product_id, quantity)
        
        elif choice == '6':
            inventory.low_stock_alert()
        
        elif choice == '7':
            inventory.total_inventory_value()
        
        elif choice == '8':
            print("\nGoodbye!")
            inventory.close()
            break
        
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()