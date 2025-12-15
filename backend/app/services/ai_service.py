import random
import asyncio

class AIService:
    async def generate_image(self, prompt: str, input_image_url: str) -> str:
        """
        Mocks an AI generation process.
        Returns a random image URL from a placeholder service.
        """
        # Simulate processing delay (Kleppmann: Systems have latency)
        await asyncio.sleep(2) 
        
        # Random seed to get different images
        seed = random.randint(1, 1000)
        return f"https://picsum.photos/seed/{seed}/512/512"