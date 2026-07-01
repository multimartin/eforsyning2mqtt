from datetime import datetime

from .measurement import Measurement


class MeasurementMapper:
    """Converts raw eForsyning data to our internal model."""

    @staticmethod
    def from_api(data: dict) -> Measurement:
        return Measurement(
            timestamp=datetime.now(),
            raw=data,
        )
    
history = []

for item in data["data"]:

    history.append(

        DailyMeasurement(

            date_from=item["DateFrom"],

            date_to=item["DateTo"],

            energy_used=item["kWh-Used"],

            water_used=item["M3-Used"],

            supply_temperature=item["Temp-Forward"],

            return_temperature=item["Temp-Return"],

            cooling=item["Temp-Cooling"],
        )
    )

current = CurrentMeasurement(

    supply_temperature=data["temp-forward"],

    return_temperature=data["temp-return"],

    cooling=data["temp-cooling"],

    energy_today=data["energy-used"],

    energy_total=data["energy-end"],

    energy_forecast=data["energy-use-prognosis"],

    water_today=data["water-used"],

    water_total=data["water-end"],
)

billing = BillingInfo(

    amount_paid=data["billing"]["Amount-Paid"],

    amount_remaining=data["billing"]["Amount-Remaining"],

    amount_vat=data["billing"]["Amount-VAT"],

    mwh_price=data["billing"]["MWh-Price"],

    m3_price=data["billing"]["M3-Price"],
)

return Measurement(

    timestamp=datetime.now(),

    current=current,

    billing=billing,

    history=history,

    raw=data,
)