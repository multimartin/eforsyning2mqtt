from datetime import datetime

from .models import (
    BillingInfo,
    CurrentMeasurement,
    DailyMeasurement,
    Measurement,
)


class MeasurementMapper:
    @staticmethod
    def from_api(data: dict) -> Measurement:

        history = []

        for item in data.get("data", []):
            history.append(
                DailyMeasurement(
                    date_from=item.get("DateFrom", ""),
                    date_to=item.get("DateTo", ""),

                    energy_used=float(item.get("kWh-Used", 0)),
                    energy_total=float(item.get("kWh-End", 0)),

                    water_used=float(item.get("M3-Used", 0)),
                    water_total=float(item.get("M3-End", 0)),

                    supply_temperature=float(item.get("Temp-Forward", 0)),
                    return_temperature=float(item.get("Temp-Return", 0)),
                    cooling=float(item.get("Temp-Cooling", 0)),
                )
            )

        billing_raw = data.get("billing", {})

        billing = BillingInfo(
            amount_paid=float(billing_raw.get("Amount-Paid", 0)),
            amount_remaining=float(billing_raw.get("Amount-Remaining", 0)),
            amount_vat=float(billing_raw.get("Amount-VAT", 0)),
            mwh_price=float(billing_raw.get("MWh-Price", 0)),
            m3_price=float(billing_raw.get("M3-Price", 0)),
        )

        current = CurrentMeasurement(
            supply_temperature=float(data.get("temp-forward", 0)),
            return_temperature=float(data.get("temp-return", 0)),
            cooling=float(data.get("temp-cooling", 0)),

            energy_today=float(data.get("energy-used", 0)),
            energy_total=float(data.get("energy-end", 0)),
            energy_forecast=float(data.get("energy-use-prognosis", 0)),

            water_today=float(data.get("water-used", 0)),
            water_total=float(data.get("water-end", 0)),
        )

        return Measurement(
            timestamp=datetime.now(),
            current=current,
            billing=billing,
            history=history,
            raw=data,
        )