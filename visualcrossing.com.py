
from datetime import datetime
from pydantic import BaseModel
from uuid import uuid4
import requests
import os
from typing import Optional

CONNECTOR_NAME = 'visualcrossing.com'


class ConfigSpec(BaseModel):
    location: str
    date1: datetime
    date2: Optional[datetime] = None
    key: str


def config_spec():
    return ConfigSpec.schema_json()


def extract(**kwargs):
    import pyarrow.csv
    from io import BytesIO

    config = ConfigSpec(**kwargs)

    id = uuid4()

    # key = os.environ["VISUAL_CROSSING_API"]
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{config.location}/{config.date1.date().isoformat()}/?unitGroup=metric&include=days&key={config.key}&contentType=csv"

    res = requests.get(url)
    res.raise_for_status()

    table = pyarrow.csv.read_csv(BytesIO(res.content))

    return table


def inspect(table):
    res = f"table loaded with {table.num_columns} columns and {table.num_rows} rows and {table.nbytes} bytes"

    return res
