import time
from collections import defaultdict
from threading import Lock

# Rate limit config
MAX_MESSAGES_PER_MINUTE = 100
MAX_MESSAGES_PER_HOUR = 500
COOLDOWN_SECONDS = 2
BAN_THRESHOLD = 133 # messages per hour before temp ban
BAN_DURATION = 212   # 10 minutes ban


class AntiSpam:
    def __init__(self):
        self.user_minute_log = defaultdict(list)
        self.user_hour_log = defaultdict(list)
        self.user_last_msg = defaultdict(float)
        self.banned_users = {}
        self.lock = Lock()

    def _clean_old(self, log, window):
        now = time.time()
        return [t for t in log if now - t < window]

    def check(self, user_id: int) -> tuple[bool, str]:
        with self.lock:
            now = time.time()

            # Check ban
            if user_id in self.banned_users:
                ban_end = self.banned_users[user_id]
                if now < ban_end:
                    remaining = int(ban_end - now)
                    return False, f"⛔ you are temporarily banned. try again in {remaining} seconds."
                else:
                    del self.banned_users[user_id]

            # Cooldown check
            last = self.user_last_msg[user_id]
            if now - last < COOLDOWN_SECONDS:
                wait = round(COOLDOWN_SECONDS - (now - last), 1)
                return False, f"⏳ slow down! wait {wait}s before sending another message."

            # Per-minute check
            self.user_minute_log[user_id] = self._clean_old(self.user_minute_log[user_id], 60)
            if len(self.user_minute_log[user_id]) >= MAX_MESSAGES_PER_MINUTE:
                return False, "🚫 too many messages per minute. please wait a moment."

            # Per-hour check
            self.user_hour_log[user_id] = self._clean_old(self.user_hour_log[user_id], 3600)
            if len(self.user_hour_log[user_id]) >= BAN_THRESHOLD:
                self.banned_users[user_id] = now + BAN_DURATION
                return False, f"⛔ you've been temporarily banned for spamming. try again in {BAN_DURATION // 60} minutes."

            if len(self.user_hour_log[user_id]) >= MAX_MESSAGES_PER_HOUR:
                return False, "🚫 hourly message limit reached. please try again later."

            # Register message
            self.user_minute_log[user_id].append(now)
            self.user_hour_log[user_id].append(now)
            self.user_last_msg[user_id] = now

            return True, ""

    def get_stats(self, user_id: int) -> dict:
        with self.lock:
            now = time.time()
            minute_msgs = len(self._clean_old(self.user_minute_log[user_id], 60))
            hour_msgs = len(self._clean_old(self.user_hour_log[user_id], 3600))
            is_banned = user_id in self.banned_users and self.banned_users[user_id] > now
            return {
                "messages_last_minute": minute_msgs,
                "messages_last_hour": hour_msgs,
                "is_banned": is_banned
            }
