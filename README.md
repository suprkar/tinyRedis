# Redis Clone

A lightweight Redis clone implemented in Python, supporting basic commands and providing functionality to handle multiple client connections. This project includes an Append-Only File (AOF) feature to ensure data persistence.

## Features

- **Basic Commands**: Supports PING, SET, GET, HSET, HGET, and HGETALL commands.
- **Data Persistence**: Uses an AOF to persist data.
- **Multithreaded Server**: Handles multiple client connections using threading.
- **RESP Protocol**: Implements the Redis Serialization Protocol (RESP) for communication.

## Requirements

- Python 3.6 or higher
- `resp` module (custom module for RESP handling)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/suprkar/tinyRedis.git
   cd redis-clone

2.Ensure all dependencies are installed. This project does not use any external libraries apart from the standard library and the custom resp module provided in the repository.

## Usage

Start the Redis clone server:
   ```bash
   python main.py
   ```
2.Connect to the server using a Redis client or any TCP client on port 6379.
