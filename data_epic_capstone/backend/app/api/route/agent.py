from fastapi import APIRouter, Depends, HTTPException


router = APIRouter()


@router.get("/agent")
def list_agents(category: str = None, trending: bool = False or True):
    """
    List all agents.
    """
    # * Sample data for agents
    return {
        "agents": [
            {"id":1, "name":"Agent 1", "category":category, "trending":trending},
            {"id":2, "name":"Agent 2", "category":category, "trending":trending},
            {"id":3, "name":"Agent 3", "category":category, "trending":trending}
            ]}

@router.get("/agent/{agent_id}")
def get_agent(agent_id: int):
    """
    Get details of a specific agent by ID.
    """
    # * Sample data for agents
    agents = {
        1: {"id": 1, "name": "Agent 1", "category": "Category A", "trending": True},
        2: {"id": 2, "name": "Agent 2", "category": "Category B", "trending": False},
        3: {"id": 3, "name": "Agent 3", "category": "Category C", "trending": True}
    }
    
    agent = agents.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return agent

@router.post("/agent/{agent_id}/review")
def review_agent(agent_id: int, review: str):
    if not review:
        raise HTTPException(status_code=400, detail="Review cannot be empty")
    
    return {"message": "Review submitted successfully", "agent_id": agent_id, "review": review}
