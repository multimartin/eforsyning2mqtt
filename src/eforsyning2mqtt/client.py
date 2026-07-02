from eforsyning2mqtt.mapper import MeasurementMapper
from eforsyning2mqtt.pyeforsyning.eforsyning import Eforsyning


class EForsyningClient:

    def __init__(self, config):

        self._client = Eforsyning(
            username=config.eforsyning.username,
            password=config.eforsyning.password,
            supplierid=config.eforsyning.supplier_id,
            billing_period_skew=0,
            is_water_supply=False,
        )

        self._authenticated = False

    def authenticate(self) -> bool:

        self._authenticated = self._client.authenticate()

        return self._authenticated

    @property
    def authenticated(self) -> bool:

        return self._authenticated

    def _ensure_authenticated(self) -> None:

        if self._authenticated:
            return

        if not self.authenticate():
            raise RuntimeError(
                "Authentication with eForsyning failed."
            )

    def get_user(self):

        self._ensure_authenticated()

        return self._client.get_user()

    def get_installations(self):

        self._ensure_authenticated()

        return self._client.get_installations()

    def get_latest_year(self):

        self._ensure_authenticated()

        return self._client.get_latest_year()

    def get_billing(self):

        self._ensure_authenticated()

        return self._client.get_billing()

    def get_latest(self):

        self._ensure_authenticated()

        raw = self._client.get_latest()

        if raw is None:
            return None

        return MeasurementMapper.from_api(raw)