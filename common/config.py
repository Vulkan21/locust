"""Configuration management for load tests"""
import os


class Config:
    """Centralized configuration for REST and gRPC load tests"""
    
    REST_BASE_URL = os.getenv('REST_BASE_URL', 'http://localhost:8000')
    
    GRPC_TARGET = os.getenv('GRPC_TARGET', 'localhost:50051')
    GRPC_HOST = GRPC_TARGET.split(':')[0]
    GRPC_PORT = int(GRPC_TARGET.split(':')[1]) if ':' in GRPC_TARGET else 50051
    
    WAIT_TIME_MIN = float(os.getenv('WAIT_TIME_MIN', '1'))
    WAIT_TIME_MAX = float(os.getenv('WAIT_TIME_MAX', '3'))
    TERM_PREFIX = os.getenv('TERM_PREFIX', 'LoadTest')
    
    @classmethod
    def print_config(cls):
        """Print current configuration (useful for debugging)"""
        print("=" * 50)
        print("LOCUST CONFIGURATION")
        print("=" * 50)
        print(f"REST_BASE_URL:  {cls.REST_BASE_URL}")
        print(f"GRPC_TARGET:    {cls.GRPC_TARGET}")
        print(f"GRPC_HOST:      {cls.GRPC_HOST}")
        print(f"GRPC_PORT:      {cls.GRPC_PORT}")
        print(f"WAIT_TIME:      {cls.WAIT_TIME_MIN}s - {cls.WAIT_TIME_MAX}s")
        print(f"TERM_PREFIX:    {cls.TERM_PREFIX}")
        print("=" * 50)

