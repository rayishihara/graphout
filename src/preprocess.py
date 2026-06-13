import pandas as pd
import json

def extract_csv_metadata(file_path):
    df = pd.read_csv(file_path)
    
    metadata = {}

    metadata['shape'] = {
        'row_count': df.shape[0],
        'column_count': df.shape[1]
    }
    
    metadata['schemma'] = {}
    metadata['stats'] = {}
    
    for col in df.columns:
        col_data = df[col]

        # TODO: nullability check
        
        # Inferred type routing
        if pd.api.types.is_bool_dtype(col_data):
            inferred_type = 'boolean'
        elif pd.api.types.is_datetime64_any_dtype(col_data):
            inferred_type = 'datetime'
        elif pd.api.types.is_numeric_dtype(col_data):
            inferred_type = 'numerical'
        else:
            inferred_type = 'categorical'
            
        metadata['schema'][col] = {
            'inferred_type': inferred_type
        }
        
        # Statistical profile
        if inferred_type == 'numerical':
            metadata['stats'][col] = {
                'min': float(col_data.min()) if not pd.isna(col_data.min()) else None,
                'max': float(col_data.max()) if not pd.isna(col_data.max()) else None,
                'mean': float(col_data.mean()) if not pd.isna(col_data.mean()) else None,
                'std': float(col_data.std()) if not pd.isna(col_data.std()) else None,
                'skewness': float(col_data.skew()) if col_data.notna().sum() >= 3 else None
            }
            
        elif inferred_type in ['categorical', 'boolean']:
            metadata['stats'][col] = {
                'cardinality': int(col_data.nunique(dropna=True)),
                'top_frequent': {str(k): int(v) for k, v in col_data.value_counts().head(5).items()}
            }
            
        elif inferred_type == 'datetime':
            metadata['stats'][col] = {
                'min': str(col_data.min()) if not pd.isna(col_data.min()) else None,
                'max': str(col_data.max()) if not pd.isna(col_data.max()) else None
            }

    return metadata