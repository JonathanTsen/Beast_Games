import os
import pandas as pd
from typing import List
from src.models.contestant import ContestantInfo


class ExcelExporter:
    """
    Utility to export contestant information to Excel.
    """
    
    @staticmethod
    def export_to_excel(contestants: List[ContestantInfo], output_path: str):
        """
        Export a list of ContestantInfo objects to Excel.
        
        Args:
            contestants: List of ContestantInfo objects
            output_path: Path to save the Excel file
        """
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Convert to dictionary format for pandas
        data = []
        for contestant in contestants:
            # Convert the Pydantic model to dict and process list fields
            contestant_dict = contestant.model_dump()
            
            # Convert list fields to comma-separated strings
            if contestant_dict.get('uniqueness_factors'):
                contestant_dict['uniqueness_factors'] = ', '.join(contestant_dict['uniqueness_factors'])
            
            if contestant_dict.get('prize_plans'):
                contestant_dict['prize_plans'] = ', '.join(contestant_dict['prize_plans'])
            
            # Remove the full transcript from the Excel export to keep it clean
            contestant_dict.pop('transcript', None)
            
            data.append(contestant_dict)
        
        # Create DataFrame and export to Excel
        df = pd.DataFrame(data)
        
        # Reorder columns for better readability
        column_order = [
            'name', 'age', 'location', 'occupation', 
            'strategist_type', 
            'favorite_challenge', 'favorite_challenge_reason',
            'favorite_contestant', 'favorite_contestant_reason',
            'uniqueness_factors', 'prize_plans',
            'video_filename'
        ]
        
        # Only include columns that exist in the DataFrame
        ordered_columns = [col for col in column_order if col in df.columns]
        df = df[ordered_columns]
        
        # Export to Excel
        df.to_excel(output_path, index=False, engine='openpyxl')
        
        print(f"Data exported to {output_path}") 