# module schemas

# fastapi
from pydantic import BaseModel


class SaveGraphRequest(BaseModel):
    file_name: str
    graph_data: dict

