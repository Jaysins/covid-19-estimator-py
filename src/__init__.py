# coding=utf-8
"""
INIT
"""
# noinspection SpellCheckingInspection
import redis as redi
import settings


redis = redi.StrictRedis().from_url(settings.REDIS_URL)


