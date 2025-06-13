import asyncio

class Matchmaker:
    """Handles queueing and pairing logic for text and voice sessions."""
    def __init__(self, voice: bool = False):
        self.voice = voice
        self.queue = []
        self.pairs = {}
        self.lock = asyncio.Lock()

    async def join_queue(self, user, custom_match=None):
        """Add a user to queue or match them via optional custom logic."""
        async with self.lock:
            if user in self.queue:
                return None
            if self.queue:
                partner = await custom_match(user) if custom_match else self.queue.pop(0)
                if partner:
                    self.pairs[user] = partner
                    self.pairs[partner] = user
                    return partner
            self.queue.append(user)
            return None

    async def leave_queue(self, user):
        """Remove a user from queue and their pair, returning the partner if existed."""
        async with self.lock:
            if user in self.queue:
                self.queue.remove(user)
            partner = self.pairs.pop(user, None)
            if partner:
                self.pairs.pop(partner, None)
                return partner