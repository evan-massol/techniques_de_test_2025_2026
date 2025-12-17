"""PointSet and Point classes for managing 2D point sets."""
import struct


class Point:
    """Represent a 2D point with x and y coordinates."""

    def __init__(self, x: float, y: float) -> None:
        """Initialize a Point with x and y coordinates."""
        self.x = x
        self.y = y

class PointSet:
    """Represent a set of 2D points."""

    def __init__(self, points=None) -> None:
        """Initialize a PointSet with an optional list of points."""
        self.points = points if points is not None else []

    def add_point(self, point: Point) -> None:
        """Add a point to the set."""
        self.points.append(point)
        
    def get_points(self) -> list:
        """Return the list of points."""
        return self.points

    def __len__(self) -> int:
        """Return the number of points in the set."""
        return len(self.points)

    @classmethod
    def from_bytes(cls, data):
        """Decode a PointSet from binary data."""
        n = struct.unpack('<I', data[:4])[0]
        ps = cls()
        for i in range(n):
            x, y = struct.unpack('<ff', data[4 + i*8: 4 + (i+1)*8])
            ps.add_point(Point(x, y))
        return ps

    def to_bytes(self):
        """Encode the PointSet to binary format."""
        b = struct.pack('<I', len(self.points))
        for point in self.points:
            b += struct.pack('<ff', point.x, point.y)
        return b