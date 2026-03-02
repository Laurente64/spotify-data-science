import re
import pandas as pd
from json import load
from typing import List, Any, Optional, Callable, Generator

# ================================
#            Functions
# ================================

def camel_to_snake(camel_strings):
    snake_strings = []
    
    for string in camel_strings:
        temp = re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()
        snake_strings.append(temp)
        
    return snake_strings

# Description: Split a list into chunks of specified size
def chunk_list(data: List[Any], chunk_size: int = 0, max_chunk: int = 0) -> Generator[List[Any], None, None]:
    # Keeps the lowest size or default, disconsidering zero values, making sure the values are greater than zero
    size = min(chunk_size, max_chunk) if min(chunk_size, max_chunk) > 0 else 100
 
    for start in range(0, len(data), size):
        yield data[start:(start + size)]

# Default method for importing JSON files as DataFrames
def import_json(path: str, record_path=None, sep="_", transform: Optional[Callable] = None):
    with open(path, "r", encoding="utf-8") as f:
        data = load(f)

    if transform:
        result = transform(data)
        df = result if isinstance(result, pd.DataFrame) else pd.json_normalize(result, record_path=record_path, sep=sep)
    else:
        df = pd.json_normalize(data, record_path=record_path, sep=sep)

    df.columns = camel_to_snake(df.columns)
    return df.drop_duplicates()
