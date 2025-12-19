import sqlite3
import os

DB = os.path.join(os.path.dirname(__file__), "orders.db")

ORDERS_DATA = [ ("ORD001","Dell Inspiron Laptop 1","Delivered","2025-01-01"), ("ORD002","HP Pavilion Laptop 2","Shipped","2025-01-02"), ("ORD003","Lenovo ThinkPad Laptop 3","Out for Delivery","2025-01-03"), ("ORD004","ASUS Vivobook Laptop 4","Processing","2025-01-04"), ("ORD005","Acer Aspire Laptop 5","Delivered","2025-01-05"), ("ORD006","MSI Gaming Laptop 6","Shipped","2025-01-06"), ("ORD007","Dell Inspiron Laptop 7","Out for Delivery","2025-01-07"), ("ORD008","HP Pavilion Laptop 8","Processing","2025-01-08"), ("ORD009","Lenovo ThinkPad Laptop 9","Delivered","2025-01-09"), ("ORD010","ASUS Vivobook Laptop 10","Shipped","2025-01-10"), ("ORD011","Acer Aspire Laptop 11","Out for Delivery","2025-01-11"), ("ORD012","MSI Gaming Laptop 12","Processing","2025-01-12"), ("ORD013","Dell Inspiron Laptop 13","Delivered","2025-01-13"), ("ORD014","HP Pavilion Laptop 14","Shipped","2025-01-14"), ("ORD015","Lenovo ThinkPad Laptop 15","Out for Delivery","2025-01-15"), ("ORD016","ASUS Vivobook Laptop 16","Processing","2025-01-16"), ("ORD017","Acer Aspire Laptop 17","Delivered","2025-01-17"), ("ORD018","MSI Gaming Laptop 18","Shipped","2025-01-18"), ("ORD019","Dell Inspiron Laptop 19","Out for Delivery","2025-01-19"), ("ORD020","HP Pavilion Laptop 20","Processing","2025-01-20"), ("ORD021","Lenovo ThinkPad Laptop 21","Delivered","2025-01-21"), ("ORD022","ASUS Vivobook Laptop 22","Shipped","2025-01-22"), ("ORD023","Acer Aspire Laptop 23","Out for Delivery","2025-01-23"), ("ORD024","MSI Gaming Laptop 24","Processing","2025-01-24"), ("ORD025","Dell Inspiron Laptop 25","Delivered","2025-01-25"), ("ORD026","HP Pavilion Laptop 26","Shipped","2025-01-26"), ("ORD027","Lenovo ThinkPad Laptop 27","Out for Delivery","2025-01-27"), ("ORD028","ASUS Vivobook Laptop 28","Processing","2025-01-28"), ("ORD029","Acer Aspire Laptop 29","Delivered","2025-01-29"), ("ORD030","MSI Gaming Laptop 30","Shipped","2025-01-30"), ("ORD031","Dell Inspiron Laptop 31","Out for Delivery","2025-01-31"), ("ORD032","HP Pavilion Laptop 32","Processing","2025-02-01"), ("ORD033","Lenovo ThinkPad Laptop 33","Delivered","2025-02-02"), ("ORD034","ASUS Vivobook Laptop 34","Shipped","2025-02-03"), ("ORD035","Acer Aspire Laptop 35","Out for Delivery","2025-02-04"), ("ORD036","MSI Gaming Laptop 36","Processing","2025-02-05"), ("ORD037","Dell Inspiron Laptop 37","Delivered","2025-02-06"), ("ORD038","HP Pavilion Laptop 38","Shipped","2025-02-07"), ("ORD039","Lenovo ThinkPad Laptop 39","Out for Delivery","2025-02-08"), ("ORD040","ASUS Vivobook Laptop 40","Processing","2025-02-09"), ("ORD041","Acer Aspire Laptop 41","Delivered","2025-02-10"), ("ORD042","MSI Gaming Laptop 42","Shipped","2025-02-11"), ("ORD043","Dell Inspiron Laptop 43","Out for Delivery","2025-02-12"), ("ORD044","HP Pavilion Laptop 44","Processing","2025-02-13"), ("ORD045","Lenovo ThinkPad Laptop 45","Delivered","2025-02-14"), ("ORD046","ASUS Vivobook Laptop 46","Shipped","2025-02-15"), ("ORD047","Acer Aspire Laptop 47","Out for Delivery","2025-02-16"), ("ORD048","MSI Gaming Laptop 48","Processing","2025-02-17"), ("ORD049","Dell Inspiron Laptop 49","Delivered","2025-02-18"), ("ORD050","HP Pavilion Laptop 50","Shipped","2025-02-19"), ("ORD051","Lenovo ThinkPad Laptop 51","Out for Delivery","2025-02-20"), ("ORD052","ASUS Vivobook Laptop 52","Processing","2025-02-21"), ("ORD053","Acer Aspire Laptop 53","Delivered","2025-02-22"), ("ORD054","MSI Gaming Laptop 54","Shipped","2025-02-23"), ("ORD055","Dell Inspiron Laptop 55","Out for Delivery","2025-02-24"), ("ORD056","HP Pavilion Laptop 56","Processing","2025-02-25"), ("ORD057","Lenovo ThinkPad Laptop 57","Delivered","2025-02-26"), ("ORD058","ASUS Vivobook Laptop 58","Shipped","2025-02-27"), ("ORD059","Acer Aspire Laptop 59","Out for Delivery","2025-02-28"), ("ORD060","MSI Gaming Laptop 60","Processing","2025-03-01"), ("ORD061","Dell Inspiron Laptop 61","Delivered","2025-03-02"), ("ORD062","HP Pavilion Laptop 62","Shipped","2025-03-03"), ("ORD063","Lenovo ThinkPad Laptop 63","Out for Delivery","2025-03-04"), ("ORD064","ASUS Vivobook Laptop 64","Processing","2025-03-05"), ("ORD065","Acer Aspire Laptop 65","Delivered","2025-03-06"), ("ORD066","MSI Gaming Laptop 66","Shipped","2025-03-07"), ("ORD067","Dell Inspiron Laptop 67","Out for Delivery","2025-03-08"), ("ORD068","HP Pavilion Laptop 68","Processing","2025-03-09"), ("ORD069","Lenovo ThinkPad Laptop 69","Delivered","2025-03-10"), ("ORD070","ASUS Vivobook Laptop 70","Shipped","2025-03-11"), ("ORD071","Acer Aspire Laptop 71","Out for Delivery","2025-03-12"), ("ORD072","MSI Gaming Laptop 72","Processing","2025-03-13"), ("ORD073","Dell Inspiron Laptop 73","Delivered","2025-03-14"), ("ORD074","HP Pavilion Laptop 74","Shipped","2025-03-15"), ("ORD075","Lenovo ThinkPad Laptop 75","Out for Delivery","2025-03-16"), ("ORD076","ASUS Vivobook Laptop 76","Processing","2025-03-17"), ("ORD077","Acer Aspire Laptop 77","Delivered","2025-03-18"), ("ORD078","MSI Gaming Laptop 78","Shipped","2025-03-19"), ("ORD079","Dell Inspiron Laptop 79","Out for Delivery","2025-03-20"), ("ORD080","HP Pavilion Laptop 80","Processing","2025-03-21"), ("ORD081","Lenovo ThinkPad Laptop 81","Delivered","2025-03-22"), ("ORD082","ASUS Vivobook Laptop 82","Shipped","2025-03-23"), ("ORD083","Acer Aspire Laptop 83","Out for Delivery","2025-03-24"), ("ORD084","MSI Gaming Laptop 84","Processing","2025-03-25"), ("ORD085","Dell Inspiron Laptop 85","Delivered","2025-03-26"), ("ORD086","HP Pavilion Laptop 86","Shipped","2025-03-27"), ("ORD087","Lenovo ThinkPad Laptop 87","Out for Delivery","2025-03-28"), ("ORD088","ASUS Vivobook Laptop 88","Processing","2025-03-29"), ("ORD089","Acer Aspire Laptop 89","Delivered","2025-03-30"), ("ORD090","MSI Gaming Laptop 90","Shipped","2025-03-31"), ("ORD091","Dell Inspiron Laptop 91","Out for Delivery","2025-04-01"), ("ORD092","HP Pavilion Laptop 92","Processing","2025-04-02"), ("ORD093","Lenovo ThinkPad Laptop 93","Delivered","2025-04-03"), ("ORD094","ASUS Vivobook Laptop 94","Shipped","2025-04-04"), ("ORD095","Acer Aspire Laptop 95","Out for Delivery","2025-04-05"), ("ORD096","MSI Gaming Laptop 96","Processing","2025-04-06"), ("ORD097","Dell Inspiron Laptop 97","Delivered","2025-04-07"), ("ORD098","HP Pavilion Laptop 98","Shipped","2025-04-08"), ("ORD099","Lenovo ThinkPad Laptop 99","Out for Delivery","2025-04-09"), ("ORD100","ASUS Vivobook Laptop 100","Delivered","2025-04-10") ]

def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            item TEXT NOT NULL,
            status TEXT NOT NULL,
            expected_delivery TEXT
        )
    """)

    cursor.executemany("""
        INSERT OR REPLACE INTO orders
        (order_id, item, status, expected_delivery)
        VALUES (?, ?, ?, ?)
    """, ORDERS_DATA)

    conn.commit()
    conn.close()

    print(f"✅ Inserted {len(ORDERS_DATA)} orders")

def get_order_by_id(order_id: str):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT order_id, item, status, expected_delivery
        FROM orders
        WHERE order_id = ?
    """, (order_id,))

    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None



if __name__ == "__main__":
    init_db()
