"""
Dependency management and graph operations for NexDex
"""
import json
import os
from typing import Dict, List, Set, Optional
import networkx as nx
from pathlib import Path

from .models import Service


class DependencyManager:
    """Manages service dependencies and builds dependency graphs"""
    
    def __init__(self):
        self.services: Dict[str, Service] = {}
        self.graph: nx.DiGraph = nx.DiGraph()
        self.business_process_importance: Dict[str, int] = {}
    
    def load_from_json(self, filepath: str) -> None:
        """Load service definitions from JSON file"""
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"Configuration file not found: {filepath}")
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Clear existing data
        self.services.clear()
        self.graph.clear()
        self.business_process_importance.clear()
        
        # Load business process importance
        self.business_process_importance = {
            k: int(v) for k, v in data.get("business_processes", {}).items()
        }
        
        # Load services
        services_data = data.get("services", [])
        for service_data in services_data:
            service = Service.from_dict(service_data)
            self.add_service(service)
    
    def save_to_json(self, filepath: str) -> None:
        """Save service definitions to JSON file"""
        data = {
            "business_processes": self.business_process_importance,
            "services": [service.to_dict() for service in self.services.values()]
        }
        
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_service(self, service: Service) -> None:
        """Add a service to the dependency graph"""
        self.services[service.name] = service
        self.graph.add_node(service.name, service=service)
        
        # Add dependency edges (reversed - dependencies point TO this service)
        for dependency in service.depends_on:
            if dependency not in self.services:
                # Create placeholder service if dependency doesn't exist yet
                placeholder = Service(name=dependency)
                self.services[dependency] = placeholder
                self.graph.add_node(dependency, service=placeholder)
            
            # Edge from dependency to dependent service
            self.graph.add_edge(dependency, service.name)
    
    def get_service(self, name: str) -> Optional[Service]:
        """Get a service by name"""
        return self.services.get(name)
    
    def get_all_services(self) -> List[Service]:
        """Get all services"""
        return list(self.services.values())

    def get_process_importance(self, process_name: str) -> Optional[int]:
        """Get importance score for a business process"""
        return self.business_process_importance.get(process_name)

    def set_process_importance(self, process_name: str, importance: int) -> None:
        """Set importance score for a business process"""
        self.business_process_importance[process_name] = int(importance)
    
    def get_dependencies(self, service_name: str) -> List[str]:
        """Get direct dependencies of a service"""
        if service_name not in self.services:
            return []
        return self.services[service_name].depends_on
    
    def get_dependents(self, service_name: str) -> List[str]:
        """Get services that depend on this service (reverse dependencies)"""
        if service_name not in self.graph:
            return []
        return list(self.graph.successors(service_name))
    
    def get_all_dependents(self, service_name: str) -> Set[str]:
        """Get all services affected by this service's failure (recursive)"""
        if service_name not in self.graph:
            return set()
        
        affected = set()
        to_check = [service_name]
        
        while to_check:
            current = to_check.pop()
            for dependent in self.graph.successors(current):
                if dependent not in affected:
                    affected.add(dependent)
                    to_check.append(dependent)
        
        return affected
    
    def get_cascade_path(self, from_service: str, to_service: str) -> Optional[List[str]]:
        """Get the shortest path from one service to another"""
        if from_service not in self.graph or to_service not in self.graph:
            return None
        
        try:
            return nx.shortest_path(self.graph, from_service, to_service)
        except nx.NetworkXNoPath:
            return None
    
    def get_cascade_depth(self, from_service: str, to_service: str) -> int:
        """Get the depth of cascade from one service to another"""
        path = self.get_cascade_path(from_service, to_service)
        if path is None:
            return -1
        return len(path) - 1
    
    def detect_circular_dependencies(self) -> List[List[str]]:
        """Detect circular dependencies in the graph"""
        try:
            cycles = list(nx.simple_cycles(self.graph))
            return cycles
        except:
            return []
    
    def get_critical_services(self) -> List[tuple[str, int]]:
        """Get services sorted by number of dependents (most critical first)"""
        criticality = []
        for service_name in self.services:
            dependent_count = len(self.get_all_dependents(service_name))
            criticality.append((service_name, dependent_count))
        
        return sorted(criticality, key=lambda x: x[1], reverse=True)
    
    def validate_dependencies(self) -> List[str]:
        """Validate that all dependencies exist"""
        errors = []
        for service in self.services.values():
            for dep in service.depends_on:
                if dep not in self.services:
                    errors.append(f"Service '{service.name}' depends on non-existent service '{dep}'")
        return errors
    
    def get_graph_stats(self) -> Dict:
        """Get statistics about the dependency graph"""
        return {
            "total_services": len(self.services),
            "total_dependencies": self.graph.number_of_edges(),
            "circular_dependencies": len(self.detect_circular_dependencies()),
            "isolated_services": len([n for n in self.graph.nodes() if self.graph.degree(n) == 0]),
            "most_critical": self.get_critical_services()[:5] if self.services else []
        }
