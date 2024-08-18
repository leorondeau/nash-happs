import sys
import os

# Add backend directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.ig_scraper import scrape_ig
from tools.image_processor import extract_text_from_image
from image_agent import process_events

def configure_workflow():
    from langgraph import StateGraph  # or the correct class if LangGraph is not available

    graph = StateGraph()  # Use StateGraph if LangGraph is not available
    
    graph.add_node('Instagram Scraper', function=scrape_ig)
    graph.add_node('Text Extraction', function=extract_text_from_image)
    graph.add_node('Event Processing', function=process_events)
    
    graph.add_edge('Instagram Scraper', 'Text Extraction')
    graph.add_edge('Text Extraction', 'Event Processing')
    
    return graph
