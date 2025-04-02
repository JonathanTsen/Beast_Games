import os
import sys
from dotenv import load_dotenv

from src.utils.video_processor import VideoProcessor
from src.utils.excel_exporter import ExcelExporter


def main():
    """
    Main entry point for the Beast Games video analyzer.
    """
    # Load environment variables
    load_dotenv()
    
    # Get output path from environment or use default
    output_path = os.getenv("OUTPUT_EXCEL_PATH", "./data/output/contestant_data.xlsx")
    
    print("Beast Games Contestant Video Analyzer")
    print("=====================================")
    
    try:
        # Process videos
        print("\nProcessing contestant videos...")
        processor = VideoProcessor()
        contestant_info_list = processor.process_videos()
        
        if not contestant_info_list:
            print("\nNo contestant information extracted. Please check your input directory.")
            return
        
        # Export to Excel
        print(f"\nExporting data for {len(contestant_info_list)} contestants to Excel...")
        ExcelExporter.export_to_excel(contestant_info_list, output_path)
        
        print("\nProcessing complete!")
        print(f"Results saved to: {os.path.abspath(output_path)}")
        
    except Exception as e:
        print(f"\nError: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 