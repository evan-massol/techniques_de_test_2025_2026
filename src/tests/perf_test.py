"""Performance tests for the Triangulator."""
import random

import pytest

from app.pointset import Point, PointSet
from app.triangulator import Triangulator


def generate_random_points(num_points):
    """Generate a list of random 2D points."""
    for _ in range(num_points):
        yield Point(random.randint(0, 10000000), random.randint(0, 10000000))


class TestPerformanceTriangulator:
    """Test class for performance with large point sets."""
    
    @pytest.mark.parametrize("size", [3, 10, 100, 500, 1000, 10000, 100000, 1000000])
    def test_large_pointset_triangulation(self, size):
        """Tests triangulation performance with a large PointSet."""
        points = PointSet(list(generate_random_points(size)))
        tri = Triangulator(points)
        
        import time
        start_time = time.time()
        result = tri.triangulate(points)
        end_time = time.time()
        
        # Replace with actual expected result check
        assert result is not None
        # Ensure triangulation takes less than 5 seconds (or any other threshold)
        assert (end_time - start_time) < 5.0