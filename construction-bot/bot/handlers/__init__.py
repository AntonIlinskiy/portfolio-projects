from aiogram import Router
import importlib

router = Router()
print("[handlers] init: router created")

def _try_include(name: str):
    try:
        module = importlib.import_module(f"bot.handlers.{name}")
        r = getattr(module, "router", None)
        if r is not None:
            router.include_router(r)
            print(f"[handlers] included: {name}")
        else:
            print(f"[handlers] skipped: {name} (no 'router' attr)")
    except Exception as e:
        print(f"[handlers] failed: {name} -> {e}")

for mod in ["start", "services", "portfolio", "reviews", "faq", "calc", "info", "request", "promos", "test_google"]:
    _try_include(mod)


