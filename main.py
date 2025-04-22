import serial
import sqlite3
import time
import square
from square.client import Client
import os
import uuid
import json
import serialRead as SR

# Connect to Arduino
try:
        ser = SR.open_serial()
except serial.SerialException as e:
        print(f"❌ Could not open serial port: {e}")
    

# Connect to SQLite
conn = sqlite3.connect('fingerprints.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    credit_card_provider TEXT NOT NULL,
    credit_card_number TEXT NOT NULL,
    cvv TEXT NOT NULL,
    expiration TEXT NOT NULL
)
''')
conn.commit()

# Listen to serial
print("Listening for fingerprint IDs...")
try:
    while True:
        line = ser.readline()          # reads up to '\n'
        if not line:
            continue                   # timeout without data
        fingerprint_id = line.decode(errors="replace").rstrip()
        print(f"Received Fingerprint ID: {fingerprint_id}")

        # Query or Insert
        cursor.execute("SELECT name FROM users WHERE id=?", (fingerprint_id,))
        result = cursor.fetchone()

        if result:
            client = Client(
                access_token=os.environ['SQUARE_ACCESS_TOKEN'],
                environment='sandbox')
            idempotency_key = str(uuid.uuid4()) 
            payment_details = {
                "source_id": "cnon:card-nonce-ok",
                "idempotency_key": idempotency_key,
                "amount_money": {
                    "amount": 100,
                    "currency": "USD"
                },
                "autocomplete": True,
                "note": "INSERT ITEM HERE",
                "buyer_email_address": result[2],
            }
            result = client.payments.create_payment(body = payment_details)
            if result.is_success():
                print(json.dumps(result.body, indent=2))
            elif result.is_error():
                print(result.errors)
        else:
            name = input("New fingerprint detected. Enter name: ")
            cursor.execute("INSERT INTO users (id, name) VALUES (?, ?)", (fingerprint_id, name))
            conn.commit()
            print(f"User {name} added.")
except KeyboardInterrupt:
        print("\n👋 Exiting on Ctrl‑C")
finally:
        ser.close()