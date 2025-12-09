from typing import Any, List, Optional

from cruiseplan.core.operations import BaseOperation, CompositeOperation

# Assuming you have a StrategyEnum defined in cruiseplan.core.validation
from cruiseplan.core.validation import StrategyEnum


class Leg:
    """
    Discrete working area/time period container for cruise operations.
    The Leg class acts as the 'Chapter' in the cruise timeline, grouping related
    operations and composites (clusters/sections) and allowing for leg-specific
    overrides of cruise parameters like speed and station spacing.
    """

    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        strategy: StrategyEnum = StrategyEnum.SEQUENTIAL,
        ordered: bool = True,
    ):
        self.name = name
        self.description = description
        self.strategy = strategy
        self.ordered = ordered

        # Operation containers
        # Operations are simple, standalone tasks (e.g., a single CTD, a single Transit)
        self.operations: List[BaseOperation] = []
        # Composites are logical groups (e.g., a Section, an Array Cluster)
        self.composites: List[CompositeOperation] = []

        # Inheritance attributes (to be set by parent Cruise)
        # These allow a Leg to override global cruise settings.
        self.vessel_speed: Optional[float] = None
        self.distance_between_stations: Optional[float] = None

    def add_operation(self, operation: BaseOperation) -> None:
        """Add a single, standalone operation to this leg."""
        self.operations.append(operation)

    def add_composite(self, composite: CompositeOperation) -> None:
        """Add a composite operation (cluster/section) to this leg."""
        self.composites.append(composite)

    def get_all_operations(self) -> List[BaseOperation]:
        """
        Flatten all operations including those within composites' children.
        This provides a unified list of atomic operations for route optimization
        that respects the Leg's boundaries.
        """
        # Start with simple, direct operations
        all_ops = self.operations.copy()

        # Add children from all composite operations
        for composite in self.composites:
            all_ops.extend(composite.children)

        return all_ops

    def calculate_total_duration(self, rules: Any) -> float:
        """
        Calculate total duration for all operations in this leg.
        Note: The duration for composites includes internal routing/optimization
        logic defined within the CompositeOperation class itself.
        """
        total = 0.0

        # Duration of standalone operations (Point, Line, Area)
        for op in self.operations:
            total += op.calculate_duration(rules)

        # Duration of Composite operations (includes internal routing/optimization)
        for composite in self.composites:
            total += composite.calculate_duration(rules)

        return total

    def get_effective_speed(self, default_speed: float) -> float:
        """Get leg-specific vessel speed or fallback to the parent cruise's default."""
        return self.vessel_speed if self.vessel_speed is not None else default_speed

    def get_effective_spacing(self, default_spacing: float) -> float:
        """Get leg-specific station spacing or fallback to the parent cruise's default."""
        return (
            self.distance_between_stations
            if self.distance_between_stations is not None
            else default_spacing
        )
