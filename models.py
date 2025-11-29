try:
    from pydantic import BaseModel
except Exception:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pydantic>=1.10.0"])
    from pydantic import BaseModel

from typing import Optional

class RowModel(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None
