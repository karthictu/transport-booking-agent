import os
import json
from typing import Dict, Any

import redis
import psycopg2

class UserProfileService:
    def __init__(self):
        # Initialize Redis cache connection
        self.redis_client = redis.from_url(os.environ.get("REDIS_URL", "redis://localhost:6379"))
        
        # Initialize PostgreSQL connection
        self.db_conn = psycopg2.connect(os.environ.get("DATABASE_URL", "dbname=transport_agent user=postgres password=postgres host=localhost"))

    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        print(f"Retrieving profile for user: {user_id}")

        # 1. Try to get from cache
        cached_profile = self.redis_client.get(f"user_profile:{user_id}")
        if cached_profile:
            print(f"Cache hit for user: {user_id}")
            return json.loads(cached_profile)

        print(f"Cache miss for user: {user_id}. Fetching from DB.")
        # 2. If not in cache, get from DB
        with self.db_conn.cursor() as cur:
            cur.execute("SELECT profile_data FROM user_profiles WHERE user_id = %s", (user_id,))
            result = cur.fetchone()
            if result and result[0]:
                profile_data = result[0]
                # 3. Store in cache for future requests
                self.redis_client.set(f"user_profile:{user_id}", json.dumps(profile_data), ex=3600) # Cache for 1 hour
                return profile_data
            else:
                # 4. If not in DB, create a default profile and store it
                print(f"No profile found for user {user_id}. Creating default.")
                default_profile = {
                    "user_id": user_id,
                    "preferences": ["cheapest", "window seat"],
                    "past_trips": [],
                    "personal_info": {"name": "New User", "email": ""},
                    "preferred_providers": {}
                }
                cur.execute("INSERT INTO user_profiles (user_id, profile_data) VALUES (%s, %s)", (user_id, json.dumps(default_profile)))
                self.db_conn.commit()
                self.redis_client.set(f"user_profile:{user_id}", json.dumps(default_profile), ex=3600)
                return default_profile