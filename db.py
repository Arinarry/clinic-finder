import sqlite3

conn = sqlite3.connect('addresses.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS addresses
                (user_id INTEGER, address TEXT)''')

def add_address(user_id, address):
    cursor.execute("INSERT INTO addresses (user_id, address) VALUES (?, ?)", (user_id, address))
    conn.commit()

def get_addresses(user_id):
    cursor.execute("SELECT address FROM addresses WHERE user_id=?", (user_id,))
    addresses = cursor.fetchall()
    return [address[0] for address in addresses]

def update_address(user_id, new_address):
    cursor.execute("UPDATE addresses SET address=? WHERE user_id=?", (new_address, user_id))
    conn.commit()