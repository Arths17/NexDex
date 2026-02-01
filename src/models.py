"""
Data models for NexDex Business Impact Simulator
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Set
from datetime import datetime


@dataclass
class Service:
    """Represents a service/application in the system"""
    name: str
    depends_on: List[str] = field(default_factory=list)
    business_process: str = ""
    importance: int = 5  # 1-10 scale
    mttr: int = 30  # Mean Time To Repair in minutes
    description: Optional[str] = None
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        if isinstance(other, Service):
            return self.name == other.name
        return False
    
    def to_dict(self) -> Dict:
        """Convert service to dictionary"""
        return {
            "name": self.name,
            "depends_on": self.depends_on,
            "business_process": self.business_process,
            "importance": self.importance,
            "mttr": self.mttr,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Service':
        """Create service from dictionary"""
        return cls(
            name=data["name"],
            depends_on=data.get("depends_on", []),
            business_process=data.get("business_process", ""),
            importance=data.get("importance", 5),
            mttr=data.get("mttr", 30),
            description=data.get("description")
        )


@dataclass
class ImpactResult:
    """Represents the impact of a service failure"""
    service: Service
    is_direct_failure: bool
    affected_business_processes: List[str]
    cascade_depth: int  # How many hops from original failure
    dependent_services: List[str]
    impact_score: float
    estimated_downtime: int  # minutes
    
    def to_dict(self) -> Dict:
        """Convert impact result to dictionary"""
        return {
            "service": self.service.name,
            "is_direct_failure": self.is_direct_failure,
            "affected_business_processes": self.affected_business_processes,
            "cascade_depth": self.cascade_depth,
            "dependent_services": self.dependent_services,
            "impact_score": self.impact_score,
            "estimated_downtime": self.estimated_downtime
        }


@dataclass
class SimulationResult:
    """Complete simulation results"""
    timestamp: datetime
    failed_services: List[str]
    impacts: List[ImpactResult]
    total_impact_score: float
    affected_business_processes: Set[str]
    total_services_affected: int
    peak_hours: bool = False  # Whether peak hours multiplier was applied
    
    def to_dict(self) -> Dict:
        """Convert simulation result to dictionary"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "failed_services": self.failed_services,
            "impacts": [impact.to_dict() for impact in self.impacts],
            "total_impact_score": self.total_impact_score,
            "affected_business_processes": list(self.affected_business_processes),
            "total_services_affected": self.total_services_affected,
            "peak_hours": self.peak_hours
        }


@dataclass
class Scenario:
    """Saved simulation scenario"""
    name: str
    description: str
    failed_services: List[str]
    created_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    peak_hours: bool = False  # Whether this failure occurs during peak hours
    
    def to_dict(self) -> Dict:
        """Convert scenario to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "failed_services": self.failed_services,
            "created_at": self.created_at.isoformat(),
            "tags": self.tags,
            "peak_hours": self.peak_hours
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Scenario':
        """Create scenario from dictionary"""
        return cls(
            name=data["name"],
            description=data.get("description", ""),
            failed_services=data["failed_services"],
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            tags=data.get("tags", []),
            peak_hours=data.get("peak_hours", False)
        )
