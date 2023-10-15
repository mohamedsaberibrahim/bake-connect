"""bake and connect models."""

def load_all_models() -> None:
    """Load all models from this folder."""

    __import__('app.api.users.models')
    __import__('app.api.bakeries.models')