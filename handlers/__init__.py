from . import commands
from . import feedback_handlers
from . import support_handlers
from . import admin_handlers
from . import product_handlers
from webapp import webapp_handlers

routers_list = [
    commands.router,
    feedback_handlers.router,
    support_handlers.router,
    admin_handlers.router,
    product_handlers.router,
    webapp_handlers.router,
]

__all__ = [
    "routers_list",
]
