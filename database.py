import redis


def connect():
    """Connect to Redis database"""
    return redis.Redis(host="localhost", port=6379, password="", decode_responses=True)


if __name__ == "__main__":
    pass
