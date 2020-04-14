# coding=utf-8
"""
settings.py

The base settings file for the project. This file will be imported by any modules that require settings functionality.
"""
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
API_PREFIX = os.getenv("API_PREFIX", "/api/v1")
LOGS_PATH = os.getenv("LOGS_PATH", "./logs.txt")



