from pydantic import BaseModel
from typing import Optional

class ProjectCreate(BaseModel):
    # Define the parameters needed to create a project
    title: str
    description: str
    mc_version: str
    mod_loader: str
    build_version: str
    client_side: Optional[bool] = False
    server_side: Optional[bool] = False

class ProjectLoad(BaseModel):
    filename: str
