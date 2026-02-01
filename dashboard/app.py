#!/usr/bin/env python3
"""
NexDex Dashboard - Flask Web Interface
Production-ready web dashboard for cross-system business impact simulation
"""
import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.exceptions import HTTPException

from src.dependency_manager import DependencyManager
from src.simulation_engine import SimulationEngine
from src.report_generator import ReportGenerator
from src.models import Scenario

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file upload

# Global instances (loaded on startup)
dependency_manager = None
simulation_engine = None
report_generator = None


def initialize_services(config_path: str = "config/services.json"):
    """Initialize NexDex services"""
    global dependency_manager, simulation_engine, report_generator
    
    try:
        dependency_manager = DependencyManager()
        dependency_manager.load_from_json(config_path)
        simulation_engine = SimulationEngine(dependency_manager)
        report_generator = ReportGenerator()
        return True
    except Exception as e:
        print(f"Error initializing services: {e}")
        return False


def load_scenario(scenario_name: str) -> Scenario:
    """Load a scenario from the scenarios directory"""
    scenarios_dir = Path("scenarios")
    filepath = scenarios_dir / f"{scenario_name}.json"
    
    if not filepath.exists():
        raise FileNotFoundError(f"Scenario '{scenario_name}' not found")
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    return Scenario.from_dict(data)


def get_all_scenarios() -> List[Dict[str, Any]]:
    """Get all scenarios with metadata"""
    scenarios_dir = Path("scenarios")
    scenarios = []
    
    if not scenarios_dir.exists():
        return scenarios
    
    for filepath in sorted(scenarios_dir.glob("*.json")):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            scenario = Scenario.from_dict(data)
            scenarios.append({
                'name': scenario.name,
                'failed_services': scenario.failed_services,
                'description': scenario.description,
                'tags': scenario.tags,
                'created_at': scenario.created_at.isoformat(),
                'peak_hours': scenario.peak_hours
            })
        except Exception as e:
            print(f"Error loading {filepath.name}: {e}")
    
    return scenarios


def format_impact_summary(result) -> Dict[str, Any]:
    """Format simulation result for JSON response"""
    summary = simulation_engine.get_impact_summary(result)
    
    return {
        'total_services_affected': summary['total_services_affected'],
        'direct_failures': summary['direct_failures'],
        'cascade_failures': summary['cascade_failures'],
        'business_processes_affected': summary['business_processes_affected'],
        'total_impact_score': round(summary['total_impact_score'], 2),
        'highest_impact_service': summary['highest_impact_service'],
        'peak_hours_applied': result.peak_hours,
        'timestamp': result.timestamp.isoformat()
    }


def format_detailed_impacts(result) -> List[Dict[str, Any]]:
    """Format detailed impact information"""
    impacts = []
    
    for impact in sorted(result.impacts, key=lambda x: x.impact_score, reverse=True):
        failure_type = "Direct" if impact.is_direct_failure else f"Cascade (depth: {impact.cascade_depth})"
        bp = impact.affected_business_processes[0] if impact.affected_business_processes else "N/A"
        
        impacts.append({
            'service': impact.service.name,
            'impact_score': round(impact.impact_score, 2),
            'failure_type': failure_type,
            'business_process': bp,
            'estimated_downtime': impact.estimated_downtime,
            'service_importance': impact.service.importance,
            'cascade_depth': impact.cascade_depth
        })
    
    return impacts


# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    """Dashboard home page"""
    try:
        scenarios = get_all_scenarios()
        return render_template('index.html', scenarios=scenarios)
    except Exception as e:
        return render_template('error.html', error=str(e)), 500


@app.route('/api/scenarios')
def api_list_scenarios():
    """API endpoint to list all scenarios"""
    try:
        scenarios = get_all_scenarios()
        return jsonify({
            'success': True,
            'scenarios': scenarios,
            'count': len(scenarios)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/scenarios/<scenario_name>')
def api_get_scenario(scenario_name: str):
    """API endpoint to get scenario details"""
    try:
        scenario = load_scenario(scenario_name)
        return jsonify({
            'success': True,
            'name': scenario.name,
            'description': scenario.description,
            'failed_services': scenario.failed_services,
            'tags': scenario.tags,
            'peak_hours': scenario.peak_hours,
            'created_at': scenario.created_at.isoformat()
        })
    except FileNotFoundError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/simulate', methods=['POST'])
def api_simulate():
    """API endpoint to run a simulation"""
    try:
        data = request.get_json()
        scenario_name = data.get('scenario_name')
        
        if not scenario_name:
            return jsonify({'success': False, 'error': 'scenario_name is required'}), 400
        
        # Load and run scenario
        scenario = load_scenario(scenario_name)
        result = simulation_engine.simulate_failure(
            scenario.failed_services,
            peak_hours=scenario.peak_hours
        )
        
        # Get impacts
        impacts = format_detailed_impacts(result)
        summary = format_impact_summary(result)
        
        # Get top business processes
        top_processes = simulation_engine.get_top_business_processes(result, limit=5)
        
        # Get affected services
        affected_services = {impact.service.name: impact.impact_score for impact in result.impacts}
        
        return jsonify({
            'success': True,
            'scenario_name': scenario_name,
            'summary': summary,
            'impacts': impacts,
            'top_processes': [{'name': p[0], 'impact_score': round(p[1], 2)} for p in top_processes],
            'affected_services': {k: round(v, 2) for k, v in affected_services.items()}
        })
    except FileNotFoundError as e:
        return jsonify({'success': False, 'error': f'Scenario not found: {str(e)}'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/compare', methods=['POST'])
def api_compare():
    """API endpoint to compare two scenarios"""
    try:
        data = request.get_json()
        scenario1_name = data.get('scenario1_name')
        scenario2_name = data.get('scenario2_name')
        
        if not scenario1_name or not scenario2_name:
            return jsonify({'success': False, 'error': 'Both scenario names are required'}), 400
        
        # Load scenarios
        scenario1 = load_scenario(scenario1_name)
        scenario2 = load_scenario(scenario2_name)
        
        # Run simulations
        result1 = simulation_engine.simulate_failure(scenario1.failed_services, peak_hours=scenario1.peak_hours)
        result2 = simulation_engine.simulate_failure(scenario2.failed_services, peak_hours=scenario2.peak_hours)
        
        # Get comparison
        comparison = simulation_engine.compare_results(result1, result2)
        
        # Format results
        summary1 = format_impact_summary(result1)
        summary2 = format_impact_summary(result2)
        impacts1 = format_detailed_impacts(result1)
        impacts2 = format_detailed_impacts(result2)
        
        worse_scenario = "Scenario 2" if comparison["worse_scenario"] == result2 else "Scenario 1"
        
        return jsonify({
            'success': True,
            'scenario1': {
                'name': scenario1_name,
                'summary': summary1,
                'impacts': impacts1,
                'failed_services': scenario1.failed_services
            },
            'scenario2': {
                'name': scenario2_name,
                'summary': summary2,
                'impacts': impacts2,
                'failed_services': scenario2.failed_services
            },
            'comparison': {
                'impact_diff': round(comparison['impact_diff'], 2),
                'impact_pct_diff': round(comparison['impact_pct_diff'], 1),
                'services_diff': comparison['services_diff'],
                'worse_scenario': worse_scenario,
                'unique_to_first': list(comparison['unique_to_first']),
                'unique_to_second': list(comparison['unique_to_second'])
            }
        })
    except FileNotFoundError as e:
        return jsonify({'success': False, 'error': f'Scenario not found: {str(e)}'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/scenario/<scenario_name>')
def scenario_detail(scenario_name: str):
    """Scenario detail page"""
    try:
        scenario = load_scenario(scenario_name)
        scenarios = get_all_scenarios()
        return render_template(
            'scenario.html',
            scenario_name=scenario_name,
            scenarios=scenarios
        )
    except FileNotFoundError:
        return render_template('error.html', error='Scenario not found'), 404
    except Exception as e:
        return render_template('error.html', error=str(e)), 500


@app.route('/compare')
def comparison():
    """Scenario comparison page"""
    try:
        scenarios = get_all_scenarios()
        return render_template('comparison.html', scenarios=scenarios)
    except Exception as e:
        return render_template('error.html', error=str(e)), 500


@app.route('/api/services')
def api_list_services():
    """API endpoint to list all services"""
    try:
        services = dependency_manager.get_all_services()
        service_list = [
            {
                'name': service.name,
                'business_process': service.business_process,
                'importance': service.importance,
                'mttr': service.mttr,
                'depends_on': service.depends_on
            }
            for service in sorted(services, key=lambda s: s.name)
        ]
        return jsonify({
            'success': True,
            'services': service_list,
            'count': len(service_list)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/statistics')
def api_statistics():
    """API endpoint to get system statistics"""
    try:
        stats = dependency_manager.get_graph_stats()
        return jsonify({
            'success': True,
            'total_services': stats['total_services'],
            'total_dependencies': stats['total_dependencies'],
            'circular_dependencies': stats['circular_dependencies'],
            'most_critical': [
                {'service': name, 'dependents': count}
                for name, count in stats['most_critical']
            ]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors"""
    return render_template('error.html', error='Page not found'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('error.html', error='Internal server error'), 500


# ============================================================================
# APPLICATION STARTUP
# ============================================================================

if __name__ == '__main__':
    # Initialize services
    if not initialize_services():
        print("Failed to initialize NexDex services")
        sys.exit(1)
    
    # Run Flask app
    print("=" * 60)
    print("🚀 NexDex Dashboard Starting...")
    print("=" * 60)
    print("📊 Dashboard URL: http://localhost:5000")
    print("🔧 Configuration: config/services.json")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )
