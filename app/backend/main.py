from datetime import datetime
import serial
import sqlite3
import time
from square import Square
from square.environment import SquareEnvironment
import keys
import uuid
import json
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

# 1. --- USER SETTINGS -------------------------------------------------
port       = "/dev/tty.usbmodemF412FA75DE8C2"        # Windows example – replace with /dev/ttyACM0, /dev/ttyUSB0, etc.
baud_rate  = 9600        # Must match Serial.begin() in your sketch
log_to_csv = False         # True => also append to a CSV file
csv_path   = "arduino_log.csv"
# ---------------------------------------------------------------------

def open_serial(wait_for_arduino_reset: bool = True) -> serial.Serial:
    """Open the serial port and optionally wait 2 s for the Arduino auto‑reset."""
    ser = serial.Serial(port, baud_rate, timeout=1)
    if wait_for_arduino_reset:
        time.sleep(2)      # most Arduinos reset when the port opens
        ser.reset_input_buffer()
    return ser

@app.route('/make_payment', methods=['GET'])
def make_payment(amount):
    # Connect to Arduino
    try:
            ser = SR.open_serial()
    except serial.SerialException as e:
            print(f"❌ Could not open serial port: {e}")
        

    # Connect to SQLite
    conn = sqlite3.connect('/fingerprints.db')
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

    result = {}

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
            resultDb = cursor.fetchone()

            if resultDb:
                client = Square(
                    token=keys.SQUARE_ACCESS_TOKEN,
                    environment=SquareEnvironment.SANDBOX)
                idempotency_key = str(uuid.uuid4()) 
                resultSquare = client.payments.create(
                    source_id="cnon:card-nonce-ok",
                    idempotency_key=idempotency_key,
                    amount_money={
                        "amount": amount * 100,  # Amount in cents
                        "currency": "USD"
                    },
                    autocomplete=True,
                    note="MILK",
                    buyer_email_address=resultDb[2],
                    card_brand = resultDb[3],
                    card_digits=resultDb[4],
                )
                if resultSquare.errors:
                    result['status'] = False;
                    result['message'] = resultSquare.errors
                    print(result.errors)
                    break
                else:
                    buyer_email = resultSquare.payment.buyer_email_address  # May be None if not collected

                    # Get card brand (from card_details)
                    card_brand = None
                    if resultSquare.payment.card_details and resultSquare.payment.card_details.card:
                        card_brand = resultSquare.payment.card_details.card.card_brand
                        card_digits = resultSquare.payment.card_details.card.last4
                    
                    result['status'] = True

                    # Build and print the thank you message
                    if buyer_email and card_brand:
                        result['message'] = f"Thanks {buyer_email} for the purchase of {result.note} for ${amount:.2f} on your {card_brand} card ending in {card_digits}!"
                        print(result['message'])
                    elif buyer_email:
                        result['message'] = f"Thanks {buyer_email} for the purchase of {result.note} for ${amount:.2f}!"
                        print(result['message'])
                    elif card_brand:
                        result['message'] = f"Thanks for your purchase of {result.note} for ${amount:.2f} on your {card_brand} card ending in {card_digits}!"
                        print(result['message'])
                    else:
                        result['message'] = f"Thanks for your purchase of {result.note} for ${amount:.2f}!"
                        print(result['message'])

                    break
            else:
                result['status'] = False
                result['message'] = "Fingerprint not found in database."
                print(result['message'])
                break
    except KeyboardInterrupt:
            print("\n👋 Exiting on Ctrl‑C")
    finally:
            ser.close()
            return jsonify(result)

@app.route('/add_user', methods=['GET'])
def add_user(info):
    
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

    result = {}

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
            resultDb = cursor.fetchone()

            if resultDb:
                result['status'] = False
                result['message'] = "Fingerprint already exists in database."
                print(result['message'])
                break
            else:
                cursor.execute("INSERT INTO users (id, name, email, credit_card_provider, credit_card_number, cvv, expiration) VALUES (?, ?, ?, ?, ?, ?, ?)", (fingerprint_id, info['name'], info['email'], info['provider'], info['number'], info['cvv'], info['expiry']))
                conn.commit()
                result['message'] = f"User {info[0]} added."
                result['status'] = True
                print(result['message'])
                break
    except KeyboardInterrupt:
            print("\n👋 Exiting on Ctrl‑C")
    finally:
            ser.close()
            return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)