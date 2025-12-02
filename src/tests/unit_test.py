"""Unit tests of the project."""

import struct
from unittest.mock import patch

import pytest

from app.main import app
from app.pointset import Point, PointSet
from app.triangulator import Triangulator


class TestTriangulator:
    """Test cases for the Triangulator class."""
    
    @pytest.mark.parametrize("points,expected_count", [
        ([Point(0.0, 0.0), Point(1.0, 0.0), Point(0.0, 1.0)], 3),
        ([Point(0.0, 0.0), Point(1.0, 1.0)], 2),
        ([Point(0.0, 0.0)], 1),
        ([], 0),
    ])
    def test_amount_of_points(self, points, expected_count):
        """Test that the Triangulator correctly counts the number of points."""
        ps = PointSet()
        for p in points:
            ps.add_point(p)
        tri = Triangulator(ps)
        assert tri.point_set.get_points() == expected_count

    def test_below_minimum_points(self):
        """Test triangulation with less than 3 points."""
        points = [Point(0.0, 0.0), Point(1.0, 0.0)]
        ps = PointSet()
        for p in points:
            ps.add_point(p)
        tri = Triangulator(ps)
        with pytest.raises(ValueError) as _:
            tri.triangulate(ps)

    def test_empty_pointset(self):
        """Test triangulation with an empty PointSet."""
        ps = PointSet()
        tri = Triangulator(ps)
        assert tri.point_set.get_points() == 0

    def test_correct_triangulation(self):
        """Test triangulation with a valid set of points."""
        points = [Point(0.0, 0.0), Point(1.0, 0.0), Point(0.0, 1.0)]
        ps = PointSet()
        for p in points:
            ps.add_point(p)
        tri = Triangulator(ps)
        result = tri.triangulate(ps)
        assert result is not None

    def test_conflicting_points(self):
        """Test triangulation with conflicting points."""
        points = [Point(0.0, 0.0), Point(1.0, 0.0), Point(0.0, 0.0)]
        ps = PointSet()
        for p in points:
            ps.add_point(p)
        tri = Triangulator(ps)
        with pytest.raises(ValueError) as _:
            tri.triangulate(ps)

    @pytest.mark.parametrize("invalid_input", [
        None,
        "not a pointset",
        123,
        [],
    ])
    def test_invalid_types(self, invalid_input):
        """Test Triangulator initialization with invalid types."""
        with pytest.raises(Exception) as _:
            Triangulator(invalid_input)
    
    def test_negative_coordinates(self):
        """Test that negative coordinates are accepted."""
        ps = PointSet()
        ps.add_point(Point(-1.0, -2.0))
        tri = Triangulator(ps)
        assert tri.point_set.get_points() == 1


class TestPointSet:
    """Test cases for the PointSet class."""
    
    @pytest.mark.parametrize("points,expected_bytes", [
        ([(1.0, 2.0), (3.0, 4.0)], 
         struct.pack('<Iff', 2, 1.0, 2.0) + struct.pack('<ff', 3.0, 4.0)),
        ([(0.0, 0.0)], 
         struct.pack('<Iff', 1, 0.0, 0.0)),
        ([], 
         struct.pack('<I', 0)),
    ])
    def test_pointset_to_bytes_conversion(self, points, expected_bytes):
        """Test the conversion of a PointSet to its binary representation."""
        ps = PointSet()
        for x, y in points:
            ps.add_point(Point(x, y))
        result = ps.to_bytes()
        assert result == expected_bytes

    def test_pointset_from_bytes_conversion(self):
        """Test the creation of a PointSet from its binary representation."""
        # 2 points, (1.0,2.0), (3.0,4.0)
        data = struct.pack('<Iff', 2, 1.0, 2.0) + struct.pack('<ff', 3.0, 4.0)
        ps = PointSet()
        ps.from_bytes(data)
        pts = ps.get_points()
        assert len(pts) == 2
        assert pts[0].x == 1.0 and pts[0].y == 2.0
        assert pts[1].x == 3.0 and pts[1].y == 4.0

    def test_check_binary_representation(self):
        """Test the binary representation of a PointSet."""
        points = [(1.0, 2.0), (3.0, 4.0), (5.0, 6.0)]
        ps = PointSet()
        for x, y in points:
            ps.add_point(Point(x, y))
        binary = ps.to_bytes()
        n = struct.unpack('<I', binary[:4])[0]
        assert n == 3
        assert len(binary) == 4 + 3 * 8


class TestTriangulatorAPI:
    """Test cases for the Triangulator API endpoint."""
    
    @pytest.fixture
    def client(self):
        """Flask test client fixture."""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_triangulation_200(self, client):
        """Mocking a successful triangulation request returning 200 OK."""
        valid_uuid = '123e4567-e89b-12d3-a456-426614174000'
        pointset_bytes = struct.pack('<Iff', 3, 0.0, 0.0) + \
                        struct.pack('<ff', 1.0, 0.0) + \
                        struct.pack('<ff', 0.0, 1.0)
        class DummyResp:
            status = 200
            def read(self):
                return pointset_bytes
            def __enter__(self): return self
            def __exit__(self, exc_type, exc_val, exc_tb): pass
        with patch('app.main.urllib.request.urlopen', return_value=DummyResp()):
            resp = client.get(f'/triangulation/{valid_uuid}')
            assert resp.status_code == 200
            assert resp.data

    @pytest.mark.parametrize("invalid_id", [
        'invalid_id',
        'not-a-uuid',
        '12345',
        'abc-def-ghi',
    ])
    def test_triangulation_400(self, client, invalid_id):
        """Test invalid PointSetID format."""
        resp = client.get(f'/triangulation/{invalid_id}')
        assert resp.status_code == 400
        data = resp.get_json()
        assert data['code'] == 'INVALID_ID'

    def test_triangulation_404(self, client):
        """Test PointSetID not found scenario."""
        class DummyResp:
            status = 404
            def read(self): return b''
            def __enter__(self): return self
            def __exit__(self, exc_type, exc_val, exc_tb): pass
        with patch('app.main.urllib.request.urlopen', return_value=DummyResp()):
            resp = client.get('/triangulation/123e4567-e89b-12d3-a456-426614174000')
            assert resp.status_code == 404
            data = resp.get_json()
            assert data['code'] == 'NOT_FOUND'

    def test_triangulation_503(self, client):
        """Test PointSetManager service unavailable scenario."""
        with patch('app.main.urllib.request.urlopen', 
                   side_effect=Exception('Service unavailable')):
            resp = client.get('/triangulation/123e4567-e89b-12d3-a456-426614174000')
            assert resp.status_code == 503
            data = resp.get_json()
            assert data['code'] == 'POINTSET_MANAGER_UNAVAILABLE'

