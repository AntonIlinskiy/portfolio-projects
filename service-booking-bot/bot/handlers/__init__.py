from aiogram import Router

router = Router()

def _include(name: str):
    try:
        module = __import__(f"bot.handlers.{name}", fromlist=["router"])
        r = getattr(module, "router", None)
        if r:
            router.include_router(r)
    except Exception as e:
        print(f"[handlers] failed {name}: {e}")

for mod in ["start", "booking"]:
    _include(mod)                