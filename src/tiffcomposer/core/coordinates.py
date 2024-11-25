from __future__ import annotations

from math import atan2, cos, radians, sin, sqrt

import numpy as np


class GeoCoordinateError(Exception):
    """Custom exception for geographic coordinate errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class GeoCoordinate:
    """Geographic coordinate class."""

    def __init__(self, latitude: float, longitude: float) -> None:
        self.latitude = latitude
        self.longitude = longitude

    @property
    def latitude(self) -> float:
        """Get coordinate latitude.

        Returns:
            float: The latitude value.
        """
        return self._latitude

    @latitude.setter
    def latitude(self, value: float) -> None:
        """Set coordinate latitude.

        Args:
            value (float): The latitude value.
        """
        if not -90 <= value <= 90:
            raise GeoCoordinateError(
                "Latitude must be between -90 and 90 degrees."
            )

        self._latitude = value

    @property
    def longitude(self) -> float:
        """Get coordinate longitude.

        Returns:
            float: The longitude value.
        """
        return self._longitude

    @longitude.setter
    def longitude(self, value: float) -> None:
        """Set coordinate longitude.

        Args:
            value (float): The longitude value.
        """
        if not -180 <= value <= 180:
            raise GeoCoordinateError(
                "Longitude must be between -180 and 180 degrees."
            )

        self._longitude = value

    @property
    def inverted(self) -> GeoCoordinate:
        """Get the inverted coordinate.

        Returns:
            GeoCoordinate: The inverted GeoCoordinate object.
        """
        return GeoCoordinate(self.longitude, self.latitude)

    @staticmethod
    def earth_radius(latitude: float) -> float:
        """Calculate Earth's radius at a given latitude.

        Args:
            latitude (float): Geodetic latitude in degrees.

        Returns:
            float: Earth's radius at the given latitude in meters.
        """
        # WGS84 ellipsoid parameters
        a = 6378137.0  # Equatorial radius [m]
        b = 6356752.314245  # Polar radius [m]

        lat_rad = radians(latitude)

        radius = sqrt(
            ((a**2 * cos(lat_rad))**2 + (b**2 * sin(lat_rad))**2) /
            ((a * cos(lat_rad))**2 + (b * sin(lat_rad))**2)
        )

        return radius

    def distance_to(self, other: GeoCoordinate, step: float = 0) -> float:
        """
        Calculate the distance to another GeoCoordinate, accounting for Earth's radius variation.

        Args:
            other (GeoCoordinate): The other geographic coordinate.
            step (float, optional): Step size in radians for intermediate calculations.
                                    If 0, calculates directly without intermediate steps.

        Returns:
            float: The distance in meters.
        """
        if not isinstance(other, GeoCoordinate):
            raise GeoCoordinateError(
                "Cannot calculate distance to a non-GeoCoordinate object."
            )

        # Convert degrees to radians
        lat1 = radians(self.latitude)
        lon1 = radians(self.longitude)
        lat2 = radians(other.latitude)
        lon2 = radians(other.longitude)

        # Difference in latitude and longitude
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        # Great circle angular distance
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # Direct calculation if step is 0
        if step == 0:
            midpoint_lat = (self.latitude + other.latitude) / 2
            # Dynamic Earth radius at midpoint
            R = self.earth_radius(midpoint_lat)
            return R * c

        # Step-based calculation using NumPy
        steps = max(int(c / step), 1)  # Ensure at least one step if step > c
        # Create fractions for interpolation
        fractions = np.linspace(0, 1, steps + 1)

        # Interpolated latitudes and longitudes along the path
        interpolated_lats = lat1 + fractions * dlat

        # Calculate Earth's radius for each interpolated point
        radii = np.array([self.earth_radius(np.degrees(lat))
                         for lat in interpolated_lats])

        # Approximate distance for each segment and sum them up
        segment_distances = radii[:-1] * (c / steps)
        total_distance = np.sum(segment_distances)

        return total_distance

    def to_tuple(self) -> tuple[float, float]:
        """Convert the GeoCoordinate to a tuple.

        Returns:
            tuple[float, float]: The latitude and longitude as a tuple.
        """
        return self.latitude, self.longitude

    def to_list(self) -> list[float]:
        """Convert the GeoCoordinate to a list.

        Returns:
            list[float]: The latitude and longitude as a list.
        """
        return [self.latitude, self.longitude]

    def to_dict(self) -> dict[str, float]:
        """Convert the GeoCoordinate to a dictionary.

        Returns:
            dict[str, float]: The latitude and longitude as a dictionary.
        """
        return {"latitude": self.latitude, "longitude": self.longitude}

    @classmethod
    def from_tuple(cls, values: tuple[float, float]) -> GeoCoordinate:
        """Create a GeoCoordinate from a tuple.

        Args:
            values (tuple[float, float]): The latitude and longitude as a tuple.

        Returns:
            GeoCoordinate: The GeoCoordinate object.
        """
        return cls(*values)

    @classmethod
    def from_list(cls, values: list[float]) -> GeoCoordinate:
        """Create a GeoCoordinate from a list.

        Args:
            values (list[float]): The latitude and longitude as a list.

        Returns:
            GeoCoordinate: The GeoCoordinate object.
        """
        return cls(*values)

    @classmethod
    def from_dict(cls, values: dict[str, float]) -> GeoCoordinate:
        """Create a GeoCoordinate from a dictionary.

        Args:
            values (dict[str, float]): The latitude and longitude as a dictionary.

        Returns:
            GeoCoordinate: The GeoCoordinate object.
        """
        return cls(values["latitude"], values["longitude"])

    def __str__(self) -> str:
        return f"Latitude: {self.latitude}, Longitude: {self.longitude}"

    def __repr__(self) -> str:
        return f"GeoCoordinate(lat={self.latitude}, lon={self.longitude})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GeoCoordinate):
            raise GeoCoordinateError(
                "Cannot compare GeoCoordinate with non-GeoCoordinate object."
            )

        return (
            self.latitude == other.latitude
            and self.longitude == other.longitude
        )

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, GeoCoordinate):
            raise GeoCoordinateError(
                "Cannot compare GeoCoordinate with non-GeoCoordinate object."
            )

        return (
            self.latitude != other.latitude
            or self.longitude != other.longitude
        )

    def __hash__(self) -> int:
        return hash((self.latitude, self.longitude))

    def __add__(self, other: object) -> GeoCoordinate:
        if not isinstance(other, GeoCoordinate):
            raise GeoCoordinateError(
                "Cannot add GeoCoordinate with non-GeoCoordinate object."
            )

        return GeoCoordinate(
            self.latitude + other.latitude,
            self.longitude + other.longitude
        )

    def __sub__(self, other: object) -> GeoCoordinate:
        if not isinstance(other, GeoCoordinate):
            raise GeoCoordinateError(
                "Cannot subtract GeoCoordinate with non-GeoCoordinate object."
            )

        return GeoCoordinate(
            self.latitude - other.latitude,
            self.longitude - other.longitude
        )


class GeoCoordinateExtent:
    """Geographic coordinate extent class."""

    def __init__(self, start: GeoCoordinate, end: GeoCoordinate) -> None:
        self.start = start
        self.end = end

    @property
    def start(self) -> GeoCoordinate:
        """Get the starting coordinate of the extent."""
        return self._start

    @start.setter
    def start(self, value: GeoCoordinate) -> None:
        """Set the starting coordinate of the extent."""
        if not isinstance(value, GeoCoordinate):
            raise GeoCoordinateError(
                "Start coordinate must be a GeoCoordinate object."
            )

        self._start = value

    @property
    def end(self) -> GeoCoordinate:
        """Get the ending coordinate of the extent."""
        return self._end

    @end.setter
    def end(self, value: GeoCoordinate) -> None:
        """Set the ending coordinate of the extent."""
        if not isinstance(value, GeoCoordinate):
            raise GeoCoordinateError(
                "End coordinate must be a GeoCoordinate object."
            )

        self._end = value

    def to_tuple(self) -> tuple[float, float, float, float]:
        """Convert the GeoCoordinateExtent to a tuple."""
        return self.start.longitude, self.end.latitude, self.end.longitude, self.start.latitude

    def to_list(self) -> list[float]:
        """Convert the GeoCoordinateExtent to a list."""
        return [self.start.longitude, self.end.latitude, self.end.longitude, self.start.latitude]

    def to_dict(self) -> dict[str, float]:
        """Convert the GeoCoordinateExtent to a dictionary."""
        return {
            "left": self.start.longitude,
            "bottom": self.start.latitude,
            "right": self.end.longitude,
            "top": self.end.latitude
        }

    def __str__(self) -> str:
        return f"Start: {self.start}, End: {self.end}"

    def __repr__(self) -> str:
        return f"GeoCoordinateExtent(start={self.start}, end={self.end})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GeoCoordinateExtent):
            raise GeoCoordinateError(
                "Cannot compare GeoCoordinateExtent with non-GeoCoordinateExtent object."
            )

        return self.start == other.start and self.end == other.end

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, GeoCoordinateExtent):
            raise GeoCoordinateError(
                "Cannot compare GeoCoordinateExtent with non-GeoCoordinateExtent object."
            )

        return self.start != other.start or self.end != other.end

    def __hash__(self) -> int:
        return hash((self.start, self.end))
