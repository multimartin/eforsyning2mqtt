from eforsyning2mqtt.mapper import MeasurementMapper
from eforsyning2mqtt.pyeforsyning.eforsyning import (
    Eforsyning,
    LoginFailed,
)


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

    def _call(self, func):

        self._ensure_authenticated()

        try:

            return func()

        except LoginFailed:

            #
            # Session has most likely expired.
            # Authenticate again and retry once.
            #

            self._authenticated = False

            self._ensure_authenticated()

            return func()

    def get_user(self):

        return self._call(
            self._client.get_user
        )

    def get_installations(self):

        return self._call(
            self._client.get_installations
        )

    def get_latest_year(self):

        return self._call(
            self._client.get_latest_year
        )

    def get_billing(self):

        return self._call(
            self._client.get_billing
        )

    def get_latest(self):

        raw = self._call(
            self._client.get_latest
        )

        if raw is None:
            return None

        return MeasurementMapper.from_api(raw)