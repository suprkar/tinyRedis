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
   git clone https://github.com/yourusername/redis-clone.git
   cd redis-clone
