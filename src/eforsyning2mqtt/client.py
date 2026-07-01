from .mapper import MeasurementMapper
from .pyeforsyning.eforsyning import Eforsyning


class EForsyningClient:

    def __init__(self, config):

        self._client = Eforsyning(
            username=config.eforsyning.username,
            password=config.eforsyning.password,
            supplierid=config.eforsyning.supplier_id,
            billing_period_skew=0,
            is_water_supply=False,
        )

    def authenticate(self):
        return self._client.authenticate()

    def get_user(self):
        return self._client._get_ebrugerinfo()

    def get_installations(self):
        return self._client._get_installations()

    def update(self):

        raw = self._client.get_latest()

        return MeasurementMapper.from_api(data)
