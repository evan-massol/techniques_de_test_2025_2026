# Test plan for the Triangulator module

## General information

Knowing that Python 3.13 has been used, there won't be any tests that check parameters types, as Python is a dynamically typed language. However, I will still include tests to ensure that the `Triangulator` class behaves correctly when given expected input types and/or values.

## Unit Tests

Knowing that the `PointSet` class is made so that the 4 first bytes of its binary representation is an integer representing the number of points in the set, we can create the following unit tests for the `Triangulator` class:

**Basic functionality tests:**

- Test the `Triangulator` class with a simple set of points and return how many points are in the set.

- Test the `Triangulator` class with less than 3 points and ensure it handles this case correctly (e.g., returns an empty triangulation).

**Conversion tests:**

- Test the `Triangulator` class making sure the conversion from `PointSet` to its binary representation is correct.

- Test the `Triangulator` class making sure the conversion from the binary representation back to a `PointSet` instance is correct.

**API tests:**

- Test the `Triangulator` API to ensure the `/triangulation/{pointSetId}` endpoint returns a correct Triangle structure in binary format for a given `PointSet` ID (response code is 200).

- Test the `Triangulator` API to ensure the `/triangulation/{pointSetId}` endpoint returns a 400 error for an invalid `PointSet` ID format.

- Test the `Triangulator` API to ensure the `/triangulation/{pointSetId}` endpoint returns a 404 error for an unknown `PointSet` ID.

- Test the `Triangulator` API to ensure the `/triangulation/{pointSetId}` endpoint returns a 400 error for an invalid `PointSet` ID format.

- Test the `Triangulator` API to ensure the `/triangulation/{pointSetId}` endpoint returns a 503 error when the triangulation service is unavailable.


**Advanced cases:**

- Checks the 4 first bytes of the binary representation of a `PointSet` instance to verify it matches the expected number of points.

- Test the `Triangulator` class with an empty set of points and ensure it handles this case correctly.

- Test the `Triangulator` class with a set of points that form a concave polygon and verify the triangulation result.

- Test the `Triangulator` class with a two conflicting points (same coordinates) and ensure it handles duplicates correctly.

- Tests for parameters types and values (e.g., passing `None`, strings, negative numbers, etc.) to ensure proper error handling.

## Performance Tests

- Test the `Triangulator` class with a large number of points (e.g., 1000 points) to evaluate performance and ensure it completes within a reasonable time frame. It will potentially retrieves the time taken for triangulation and checks if it is below a certain threshold (e.g., 1 second).