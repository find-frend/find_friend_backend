from rest_framework.routers import DefaultRouter

DISALLOWED_ACTIONS = (
    "activation",
    "resend_activation",
    "reset_password",
    "reset_password_confirm",
    "reset_username",
    "reset_username_confirm",
    "set_username",
)


class CustomRouter(DefaultRouter):

    def get_method_map(self, viewset, method_map):
        """Исключение неподдерживаемых приложением методов."""
        method_map = super().get_method_map(viewset, method_map)
        return {
            key: val
            for key, val in method_map.items()
            if val not in DISALLOWED_ACTIONS
        }
