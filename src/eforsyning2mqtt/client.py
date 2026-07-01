from .pyeforsyning.eforsyning import Eforsyning


class EForsyningClient:
    """Wrapper around the pyeforsyning library."""

    def __init__(self, config):

        self._client = Eforsyning(
            username=config.eforsyning.username,
            password=config.eforsyning.password,
            supplierid=config.eforsyning.supplier_id,
            billing_period_skew=0,
            is_water_supply=False,
        )

    def authenticate(self) -> bool:
        return self._client.authenticate()

    def get_latest(self) -> dict:
        """Return the raw dictionary from pyeforsyning."""
        return self._client.get_latest()