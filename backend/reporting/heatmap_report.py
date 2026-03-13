from database.mongo_client import get_db

def generate_heatmap_data() -> dict:
    """
    Query the pii_inventory collection in MongoDB, group the data by 
    source (or file_name), and count the occurrences of each sensitive entity type.
    
    Returns a dictionary formatted for the heatmap visualization:
    {
        "source_name": {
            "entity_type_1": count,
            "entity_type_2": count
        },
        ...
    }
    """
    db = get_db()
    pii_collection = db["pii_inventory"]
    
    # Aggregation pipeline to group by source and entity_type and get counts
    pipeline = [
        # Group by both source and entity_type, counting occurrences
        {
            "$group": {
                "_id": {
                    "source": {"$ifNull": ["$source", "$file_name"]}, # Fallback to file_name if source is missing
                    "entity_type": "$entity_type"
                },
                "count": {"$sum": 1}
            }
        },
        # Sort by source for consistent output
        {
            "$sort": {
                "_id.source": 1
            }
        }
    ]
    
    results = pii_collection.aggregate(pipeline)
    
    # Format the results into the expected nested dictionary structure
    heatmap_data = {}
    
    for result in results:
        source = result["_id"].get("source", "Unknown")
        entity_type = result["_id"].get("entity_type", "Unknown")
        count = result.get("count", 0)
        
        # Initialize the source dict if it doesn't exist
        if source not in heatmap_data:
            heatmap_data[source] = {}
            
        # Add the count for this entity type
        heatmap_data[source][entity_type] = count
        
    return heatmap_data
