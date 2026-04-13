import asyncio
import websockets
import aiosqlite
from websockets.exceptions import ConnectionClosed

async def init_db():
    async with aiosqlite.connect("sensor_data.db") as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                temperature REAL,
                humidity REAL,
                moisture REAL
            )
        ''')
        await db.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp ON sensor_data(timestamp)
        ''')
        await db.commit()

async def echo(websocket):
    print(f"Client connected: {websocket.remote_address}")
    try:
        async for message in websocket:
            print(f"Received: {message}")
            try:
                parts = [float(p.strip()) for p in message.split(',')]
                if len(parts) == 3:
                    temp, hum, moist = parts
                    async with aiosqlite.connect("sensor_data.db") as db:
                        await db.execute('''
                            INSERT INTO sensor_data (temperature, humidity, moisture)
                            VALUES (?, ?, ?)
                        ''', (temp, hum, moist))
                        await db.commit()
                    print(f"Saved: Temp={temp}, Hum={hum}, Moist={moist}")
                else:
                    print("Invalid message format: expected 3 comma-separated values")
            except ValueError:
                print("Failed to parse values from message")

    except ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")
    

async def main():
    await init_db()
    async with websockets.serve(echo, "0.0.0.0", 8765):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
