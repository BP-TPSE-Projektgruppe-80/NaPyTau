from dataclasses import dataclass
from typing import List


@dataclass
class RawNapatauSetupData:
    # The rows read from a saved .napset file
    napsetup_rows: List[str]
