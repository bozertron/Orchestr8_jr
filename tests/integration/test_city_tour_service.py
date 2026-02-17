import pytest
from orchestr8_next.city.tour_service import TourService, TourStep

def test_tour_lifecycle():
    """Verify TourService (C3-01) flow."""
    service = TourService()
    
    steps = [
        TourStep(id="s1", title="Welcome", content="Start here"),
        TourStep(id="s2", title="Middle", content="Look around"),
        TourStep(id="s3", title="End", content="Done")
    ]
    
    service.load_tour(steps)
    assert not service.is_active()
    
    # Start
    current = service.start_tour()
    assert service.is_active()
    assert current.id == "s1"
    
    # Next
    current = service.next_step()
    assert current.id == "s2"
    
    # Next
    current = service.next_step()
    assert current.id == "s3"
    
    # Finish
    current = service.next_step()
    assert current is None
    assert not service.is_active()

def test_tour_navigation():
    """Verify prev/next logic."""
    service = TourService()
    service.load_tour([TourStep("1", "A", ""), TourStep("2", "B", "")])
    
    service.start_tour() # At 1
    service.next_step()  # At 2
    
    prev = service.previous_step()
    assert prev.id == "1"
    
    # Cannot ensure 'previous' from start doesn't crash or behave weirdly
    prev = service.previous_step()
    assert prev is None # At start
