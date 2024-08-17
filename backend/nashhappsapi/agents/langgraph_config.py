from langgraph import LangGraph
from tools.ig_scraper import download_images
from tools.image_processor import extract_text_from_image
from image_agent import process_events


def configure_workflow():
    graph = LangGraph()
    
    graph.add_node('Instagram Scraper', function=download_images)
    graph.add_node('Text Extraction', function=extract_text_from_image)
    graph.add_node('Event Processing', function=process_events)
    
    graph.add_edge('Instagram Scraper', 'Text Extraction')
    graph.add_edge('Text Extraction', 'Event Processing')
    
    return graph
