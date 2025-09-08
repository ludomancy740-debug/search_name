# ========== Mixin ==========
class LoggingMixin:
    logging_enabled = True   # global toggle

    def log(self, message):
        if LoggingMixin.logging_enabled:   # only log if enabled
            print(f"[LOG] {getattr(self, 'owner', 'UNKNOWN')}: {message}")