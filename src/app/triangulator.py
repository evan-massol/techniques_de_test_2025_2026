"""Triangulator module for computing triangulations."""
from app.pointset import PointSet


class Triangulator:
    """Compute triangulations from point sets."""

    def __init__(self, point_set) -> None:
        """Initialize Triangulator with a point set."""
        if not isinstance(point_set, PointSet):
            raise TypeError("point_set must be a PointSet instance")
        self.point_set = point_set
        
    def triangulate(self, points):
        """Compute triangulation for the given points."""
        # Check minimum number of points
        if len(points) < 3:
            raise ValueError(
                "At least 3 points are required for triangulation."
            )
        
        # Detect duplicate points
        point_list = points.get_points() if isinstance(points, PointSet) else points
        coords = [(p.x, p.y) for p in point_list]
        if len(coords) != len(set(coords)):
            raise ValueError("Duplicate points detected.")
        
        n = len(point_list)
        
        # Base case with 3 points
        if n == 3:
            return [(0, 1, 2)]
        
        # Find the point with the smallest y (and x if tie)
        min_idx = 0
        for i in range(1, n):
            if (point_list[i].y < point_list[min_idx].y or 
                (point_list[i].y == point_list[min_idx].y and 
                 point_list[i].x < point_list[min_idx].x)):
                min_idx = i
        
        # Sort points by polar angle from the minimum point
        sorted_indices = self.sort_by_polar_angle(point_list, min_idx)
        
        # Triangulation by fan from the first point
        triangles = []
        for i in range(1, len(sorted_indices) - 1):
            triangles.append((sorted_indices[0], 
                              sorted_indices[i], 
                              sorted_indices[i + 1]))
        
        return triangles

    def sort_by_polar_angle(self, points, start_idx):
        """Sort points by polar angle from a starting point."""
        start_point = points[start_idx]
        
        def polar_angle_and_dist(idx):
            if idx == start_idx:
                return (-3.14159, 0)
            p = points[idx]
            import math
            angle = math.atan2(p.y - start_point.y, p.x - start_point.x)
            dist = (p.x - start_point.x) ** 2 + (p.y - start_point.y) ** 2
            return (angle, dist)
        
        sorted_indices = sorted(range(len(points)), key=polar_angle_and_dist)
        return sorted_indices