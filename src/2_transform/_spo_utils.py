import re
import pandas as pd
from json import load
from typing import List, Any, Optional, Callable

# ================================
#            Functions
# ================================

def camel_to_snake(camel_strings):
    snake_strings = []
    
    for string in camel_strings:
        temp = re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()
        snake_strings.append(temp)
        
    return snake_strings

# Split a list into chunks of specified size
def chunk_list(data: List[Any], max_chunk: int, chunk_size: int = 0):
    if chunk_size > 0:
        size = chunk_size
        if max_chunk is not None:
            size = min(chunk_size, max_chunk)
    elif max_chunk is not None and max_chunk > 0:
        size = max_chunk
    else:
        size = 100  # default chunk size

    for i in range(0, len(data), size):
        yield data[i:(i + size)]

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
