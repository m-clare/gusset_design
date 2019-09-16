'''
Run this script once to generate a JSON file containing all steel shapes
'''
import pandas as pd
import json

steel_shapes_df = pd.read_excel('aisc-shapes-database-v15.0.xlsx',
                                sheet_name='Database v15.0')

output_path = 'aisc_shapes_database_v15.json'

steel_shapes_df.to_json(output_path, orient='index')
