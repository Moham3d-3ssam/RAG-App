from pydantic import BaseModel
from typing import Optional

class PushRequest(BaseModel):
  do_rest = Optional[int] = 0
