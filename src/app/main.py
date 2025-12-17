"""Main application module for the Triangulation Service."""
import os
import struct
import urllib.error
import urllib.request
import uuid

from flask import Flask, Response, jsonify

from app.pointset import PointSet
from app.triangulator import Triangulator

app = Flask(__name__)

POINT_SET_MANAGER_URL = os.environ.get("POINT_SET_MANAGER_URL", "http://localhost:5001/pointset/")

def triangles_to_bytes(point_set: PointSet, triangles: list) -> bytes:
    """Encode triangles to bytes.

    Format:
    - 4 bytes: number of points (unsigned int)
    - For each point:
      - 4 bytes: x coordinate (float)
      - 4 bytes: y coordinate (float)
    - 4 bytes: number of triangles (unsigned int)
    - For each triangle:
      - 4 bytes: index of first point (unsigned int)
      - 4 bytes: index of second point (unsigned int)
      - 4 bytes: index of third point (unsigned int)
    """
    b = point_set.to_bytes()
    
    # Add triangles part
    b += struct.pack('<I', len(triangles))
    for i, j, k in triangles:
        b += struct.pack('<III', i, j, k)
    return b

@app.route("/triangulation/<point_set_id>", methods=["GET"])
def get_triangulation(point_set_id: str):
    """Endpoint to get the triangulation for a given PointSetID.

    Retrieves the PointSet from the PointSetManager service (we suppose it
    is reachable at POINT_SET_MANAGER_URL), performs triangulation,
    and returns the triangles in binary format.
    """
    try:
        uuid.UUID(point_set_id)
    except ValueError:
        return jsonify({
            "code": "INVALID_ID",
            "message": "Invalid PointSetID format."
        }), 400
    if not point_set_id or len(point_set_id) < 10:
        return jsonify({
            "code": "INVALID_ID",
            "message": "Invalid PointSetID format."
        }), 400
    try:
        url = f"{POINT_SET_MANAGER_URL}{point_set_id}"
        with urllib.request.urlopen(url) as resp:
            if resp.status == 200:
                pointset_bytes = resp.read()
            elif resp.status == 404:
                return jsonify({
                    "code": "NOT_FOUND",
                    "message": "PointSetID not found."
                }), 404
            else:
                return jsonify({
                    "code": "POINTSET_MANAGER_ERROR",
                    "message": f"PointSetManager error: {resp.status}"
                }), 503
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return jsonify({
                "code": "NOT_FOUND",
                "message": "PointSetID not found."
            }), 404
        elif e.code == 400:
            return jsonify({
                "code": "INVALID_ID",
                "message": "Invalid PointSetID format."
            }), 400
        else:
            return jsonify({
                "code": "POINTSET_MANAGER_ERROR",
                "message": f"PointSetManager error: {e.code}"
            }), 503
    except Exception as e:
        return jsonify({
            "code": "POINTSET_MANAGER_UNAVAILABLE",
            "message": f"Failed to contact PointSetManager: {e}"
        }), 503
    try:
        points_ps = PointSet.from_bytes(pointset_bytes)
    except Exception:
        return jsonify({
            "code": "INVALID_POINTSET",
            "message": "Could not decode PointSet."
        }), 400
    try:
        triangles = Triangulator(points_ps).triangulate(points_ps)
    except Exception:
        return jsonify({
            "code": "TRIANGULATION_FAILED",
            "message": "Triangulation could not be computed."
        }), 500
    triangles_bytes = triangles_to_bytes(points_ps, triangles)
    return Response(triangles_bytes, content_type="application/octet-stream"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
