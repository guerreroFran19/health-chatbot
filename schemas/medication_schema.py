# schemas/medication_schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MedicationCreate(BaseModel):
    name: str
    dosage: str
    frequency_hours: int
    end_date: Optional[datetime] = None
    instructions: Optional[str] = None

class MedicationResponse(BaseModel):
    id: int
    name: str
    dosage: str
    frequency_hours: int
    start_date: datetime
    end_date: Optional[datetime]
    instructions: Optional[str]
    is_active: bool