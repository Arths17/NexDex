"""
Simulation engine for service failure impact analysis
"""
from typing import List, Set
from datetime import datetime
import math

from .models import Service, ImpactResult, SimulationResult
from .dependency_manager import DependencyManager

# Configuration
PEAK_HOURS_MULTIPLIER = 1.2  # 20% increase in impact during peak hours


class SimulationEngine:
    """Simulates service failures and calculates business impact"""
    
    def __init__(self, dependency_manager: DependencyManager):
        self.dependency_manager = dependency_manager
    
    def simulate_failure(self, failed_services: List[str], peak_hours: bool = False) -> SimulationResult:
        """
        Simulate failure of one or more services and calculate impact
        
        Args:
            failed_services: List of service names to simulate as failed
            peak_hours: Whether this failure occurs during peak hours (default: False)
            
        Returns:
            SimulationResult with complete impact analysis
        
        Args:
            failed_services: List of service names to simulate as failed
            
        Returns:
            SimulationResult with complete impact analysis
        """
        # Validate services exist
        for service_name in failed_services:
            if service_name not in self.dependency_manager.services:
                raise ValueError(f"Service '{service_name}' not found in configuration")
        
        impacts_by_service = {}
        all_affected_services = set(failed_services)
        all_business_processes = set()
        
        # Calculate impact for each failed service and its dependents
        for failed_service_name in failed_services:
            # Get the service
            failed_service = self.dependency_manager.get_service(failed_service_name)
            
            # Direct impact
            direct_impact = self._calculate_impact(
                service=failed_service,
                is_direct_failure=True,
                cascade_depth=0,
                caused_by_services=[]
            )
            impacts_by_service[failed_service.name] = direct_impact
            all_business_processes.update(direct_impact.affected_business_processes)
            
            # Cascading impact
            affected_services = self.dependency_manager.get_all_dependents(failed_service_name)
            all_affected_services.update(affected_services)
            
            for affected_service_name in affected_services:
                if affected_service_name in failed_services:
                    continue
                affected_service = self.dependency_manager.get_service(affected_service_name)
                cascade_depth = self.dependency_manager.get_cascade_depth(
                    failed_service_name,
                    affected_service_name
                )
                
                # Calculate which failed services cause this impact
                causing_services = [
                    fs for fs in failed_services
                    if affected_service_name in self.dependency_manager.get_all_dependents(fs)
                ]
                
                cascade_impact = self._calculate_impact(
                    service=affected_service,
                    is_direct_failure=False,
                    cascade_depth=cascade_depth,
                    caused_by_services=causing_services
                )
                existing = impacts_by_service.get(affected_service_name)
                if existing is None or cascade_impact.impact_score > existing.impact_score:
                    impacts_by_service[affected_service_name] = cascade_impact
                all_business_processes.update(cascade_impact.affected_business_processes)
        
        # Calculate total impact score
        impacts = list(impacts_by_service.values())
        total_impact = sum(impact.impact_score for impact in impacts)
        
        # Apply peak hours multiplier if applicable
        if peak_hours:
            total_impact = total_impact * PEAK_HOURS_MULTIPLIER
        
        return SimulationResult(
            timestamp=datetime.now(),
            failed_services=failed_services,
            impacts=impacts,
            total_impact_score=total_impact,
            affected_business_processes=all_business_processes,
            total_services_affected=len(all_affected_services),
            peak_hours=peak_hours
        )
    
    def _calculate_impact(
        self,
        service: Service,
        is_direct_failure: bool,
        cascade_depth: int,
        caused_by_services: List[str]
    ) -> ImpactResult:
        """
        Calculate impact for a single service
        
        Impact Score Formula:
        - Base: MTTR × Importance
        - Cascade multiplier: 1.0 / (1 + cascade_depth) for indirect failures
        - Dependency multiplier: log2(1 + num_dependents)
        """
        # Get dependents
        dependents = self.dependency_manager.get_dependents(service.name)
        
        # Calculate base impact using business process importance if defined
        process_importance = None
        if service.business_process:
            process_importance = self.dependency_manager.get_process_importance(service.business_process)
        
        effective_importance = process_importance if process_importance is not None else service.importance
        effective_importance = max(1, min(10, int(effective_importance)))
        
        base_impact = service.mttr * effective_importance
        
        # Apply cascade reduction for indirect failures
        if is_direct_failure:
            cascade_multiplier = 1.0
        else:
            # Reduce impact based on cascade depth
            cascade_multiplier = 1.0 / (1 + cascade_depth * 0.5)
        
        # Apply dependency multiplier (services with more dependents are more critical)
        dependency_multiplier = math.log2(1 + len(dependents)) if dependents else 1.0
        
        # Final impact score
        impact_score = base_impact * cascade_multiplier * dependency_multiplier
        
        # Affected business processes
        affected_processes = [service.business_process] if service.business_process else []
        
        return ImpactResult(
            service=service,
            is_direct_failure=is_direct_failure,
            affected_business_processes=affected_processes,
            cascade_depth=cascade_depth,
            dependent_services=dependents,
            impact_score=round(impact_score, 2),
            estimated_downtime=service.mttr
        )
    
    def compare_scenarios(
        self,
        scenarios: List[List[str]]
    ) -> List[SimulationResult]:
        """
        Compare multiple failure scenarios
        
        Args:
            scenarios: List of failure scenarios (each scenario is a list of service names)
            
        Returns:
            List of SimulationResults, one for each scenario
        """
        results = []
        for scenario in scenarios:
            result = self.simulate_failure(scenario)
            results.append(result)
        
        return results
    
    def find_critical_paths(self, service_name: str) -> List[List[str]]:
        """
        Find all paths from a service to its dependents
        Useful for understanding failure propagation
        """
        if service_name not in self.dependency_manager.services:
            return []
        
        paths = []
        affected = self.dependency_manager.get_all_dependents(service_name)
        
        for affected_service in affected:
            path = self.dependency_manager.get_cascade_path(service_name, affected_service)
            if path:
                paths.append(path)
        
        return paths
    
    def get_worst_case_scenario(self) -> List[str]:
        """
        Identify the worst-case single service failure
        Returns the service that would cause the most impact
        """
        worst_impact = 0
        worst_service = None
        
        for service in self.dependency_manager.get_all_services():
            result = self.simulate_failure([service.name])
            if result.total_impact_score > worst_impact:
                worst_impact = result.total_impact_score
                worst_service = service.name
        
        return [worst_service] if worst_service else []
    
    def get_impact_summary(self, result: SimulationResult) -> dict:
        """Get a summary of the simulation result"""
        direct_failures = [i for i in result.impacts if i.is_direct_failure]
        cascade_failures = [i for i in result.impacts if not i.is_direct_failure]
        
        return {
            "total_services_affected": result.total_services_affected,
            "direct_failures": len(direct_failures),
            "cascade_failures": len(cascade_failures),
            "business_processes_affected": len(result.affected_business_processes),
            "total_impact_score": result.total_impact_score,
            "average_impact_per_service": (
                result.total_impact_score / result.total_services_affected
                if result.total_services_affected > 0 else 0
            ),
            "highest_impact_service": max(
                result.impacts,
                key=lambda x: x.impact_score
            ).service.name if result.impacts else None
        }
    
    def get_top_business_processes(self, result: SimulationResult, limit: int = 5) -> List[tuple]:
        """Get top N most impacted business processes by impact score"""
        process_impact = {}
        for impact in result.impacts:
            for process in impact.affected_business_processes:
                if process:
                    if process not in process_impact:
                        process_impact[process] = 0
                    process_impact[process] += impact.impact_score
        
        sorted_processes = sorted(
            process_impact.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return sorted_processes[:limit]
    
    def compare_results(self, result1: SimulationResult, result2: SimulationResult) -> dict:
        """
        Compare two simulation results and return comparison metrics.
        
        Args:
            result1: First simulation result
            result2: Second simulation result
            
        Returns:
            Dictionary with comparison data and difference calculations
        """
        impact_diff = result2.total_impact_score - result1.total_impact_score
        impact_pct_diff = (
            (impact_diff / result1.total_impact_score * 100)
            if result1.total_impact_score > 0 else 0
        )
        
        services_diff = result2.total_services_affected - result1.total_services_affected
        
        # Get highest impact services for each
        highest1 = max(result1.impacts, key=lambda x: x.impact_score) if result1.impacts else None
        highest2 = max(result2.impacts, key=lambda x: x.impact_score) if result2.impacts else None
        
        # Get unique services affected by each
        services1 = set(i.service.name for i in result1.impacts)
        services2 = set(i.service.name for i in result2.impacts)
        unique_to_first = services1 - services2
        unique_to_second = services2 - services1
        common_services = services1 & services2
        
        return {
            "result1": result1,
            "result2": result2,
            "impact_diff": impact_diff,
            "impact_pct_diff": impact_pct_diff,
            "services_diff": services_diff,
            "highest1": highest1,
            "highest2": highest2,
            "unique_to_first": unique_to_first,
            "unique_to_second": unique_to_second,
            "common_services": common_services,
            "worse_scenario": result2 if result2.total_impact_score > result1.total_impact_score else result1,
            "summary1": self.get_impact_summary(result1),
            "summary2": self.get_impact_summary(result2)
        }
