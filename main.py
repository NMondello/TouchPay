import serial
import sqlite3
import time
from square import Square
from square.environment import SquareEnvironment
import keys
import uuid
import json
import serialRead as SR

infoMap = {"Nick":['nmondello@hmc.edu', "Visa", "1839403849283947", "344", "3/27"], "Max":['mdesomma@hmc.edu', "AMEX", "3748594758374857", "485", "2/22"], "Luke":['lsummers@hmc.edu', "Discover", "2749847583748574", "999", "1/10"]}
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
        cursor.execute("SELECT * FROM users WHERE id=?", (fingerprint_id,))
        result = cursor.fetchone()

        if result:
            client = Square(
                token=keys.SQUARE_ACCESS_TOKEN,
                environment=SquareEnvironment.SANDBOX)
            idempotency_key = str(uuid.uuid4()) 
            result = client.payments.create(
                source_id="cnon:card-nonce-ok",
                idempotency_key=idempotency_key,
                amount_money={
                    "amount": 1000,
                    "currency": "USD"
                },
                autocomplete=True,
                note="MILK",
                buyer_email_address=result[2],
                card_brand = result[3],
                card_digits=result[4],
            )
            if result.errors:
                print(result.errors)
            else:
                #response_json = json.dumps(result.to_dict(), indent=2)
                #print(response_json)

                buyer_email = result.payment.buyer_email_address  # May be None if not collected
                

                # Get the amount
                amount_paid_cents = result.payment.amount_money.amount  # In cents
                currency = result.payment.amount_money.currency

                # Get card brand (from card_details)
                card_brand = None
                if result.payment.card_details and result.payment.card_details.card:
                    card_brand = result.payment.card_details.card.card_brand
                    card_digits = result.payment.card_details.card.last4

                # Format amount to dollars
                amount_paid_dollars = amount_paid_cents / 100

                # Build and print the thank you message
                if buyer_email and card_brand:
                    print(f"Thanks {buyer_email} for the purchase of {result.note} for ${amount_paid_dollars:.2f} on your {card_brand} card ending in {card_digits}!")
                else:
                    print(f"Thanks for your purchase of {result.note} for ${amount_paid_dollars:.2f}!")
        else:
            name = input("New fingerprint detected. Enter name: ")
            cursor.execute("INSERT INTO users (id, name, email, credit_card_provider, credit_card_number, cvv, expiration) VALUES (?, ?, ?, ?, ?, ?, ?)", (fingerprint_id, name, infoMap[name][0], infoMap[name][1], infoMap[name][2], infoMap[name][3], infoMap[name][4]))
            conn.commit()
            print(f"User {name} added.")
except KeyboardInterrupt:
        print("\n👋 Exiting on Ctrl‑C")
finally:
        ser.close()