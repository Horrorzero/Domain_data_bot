import json

from aiogram.filters import Filter
from aiogram.types import Message

with open('parser\data\ all_tdl.json', 'r', encoding="utf-8") as f:
    all_tdl = json.load(f)


class Domain(Filter):
    async def __call__(self, message: Message) -> bool:
        words = message.text.split()
        for word in words:
            if any(word.endswith(f'{a}') for a in all_tdl):
                return True
        return False
