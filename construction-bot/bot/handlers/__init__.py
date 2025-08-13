from aiogram import Router

router = Router()

def _try_include(name: str):
    try:
        module = __import__(f"bot.handlers.{name}", fromlist=["router"])
        r = getattr(module, "router", None)
        if r is not None:
            router.include_router(r)
        print(f"[handlers] included: {name}")
    except Exception as e:
        print(f"[handlers] failed: {name} -> {e}")

# Финальный список модулей без тестов
for mod in [
    "start",
    "services",
    "portfolio",
    "reviews",
    "faq",
    "calc",
    "info",
    "promos",
    "request",
]:
    _try_include(mod)
