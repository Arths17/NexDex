"""
Report generation for simulation results
"""
import os
from pathlib import Path
from datetime import datetime
from typing import Optional
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for macOS
import matplotlib.pyplot as plt
import networkx as nx
from jinja2 import Template

from .models import SimulationResult, ImpactResult
from .dependency_manager import DependencyManager


class ReportGenerator:
    """Generates reports in various formats"""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_all_reports(
        self,
        result: SimulationResult,
        dependency_manager: DependencyManager,
        prefix: str = "impact_report"
    ) -> dict:
        """Generate all report formats and return file paths"""
        timestamp = result.timestamp.strftime("%Y%m%d_%H%M%S")
        
        reports = {
            "markdown": self.generate_markdown_report(result, prefix, timestamp),
            "html": self.generate_html_report(result, dependency_manager, prefix, timestamp),
            "graph": self.generate_graph_visualization(result, dependency_manager, prefix, timestamp)
        }
        
        return reports

    def generate_batch_markdown_report(self, scenarios, results) -> str:
        """Generate a combined Markdown report for multiple scenarios"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = self.output_dir / f"batch_report_{timestamp}.md"
        
        content = "# NexDex Batch Scenario Report\n\n"
        content += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        content += "---\n\n"
        content += "## Scenario Comparison\n\n"
        content += "| Scenario | Failed Services | Total Impact | Services Affected | Business Processes | Highest Impact Service |\n"
        content += "|---------|------------------|--------------|-------------------|--------------------|------------------------|\n"
        
        for scenario, result in zip(scenarios, results):
            highest = max(result.impacts, key=lambda x: x.impact_score).service.name if result.impacts else "N/A"
            content += (
                f"| {scenario.name} | {', '.join(result.failed_services)} | "
                f"{result.total_impact_score:.2f} | {result.total_services_affected} | "
                f"{len(result.affected_business_processes)} | {highest} |\n"
            )
        
        content += "\n---\n\n"
        content += "## Totals\n\n"
        total_impact = sum(r.total_impact_score for r in results)
        total_services = sum(r.total_services_affected for r in results)
        content += f"- **Total Impact (sum):** {total_impact:.2f}\n"
        content += f"- **Total Services Affected (sum):** {total_services}\n"
        content += f"- **Scenarios Run:** {len(results)}\n"
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        return str(filepath)
    
    def generate_markdown_report(
        self,
        result: SimulationResult,
        prefix: str = "impact_report",
        timestamp: Optional[str] = None
    ) -> str:
        """Generate a Markdown report"""
        if timestamp is None:
            timestamp = result.timestamp.strftime("%Y%m%d_%H%M%S")
        
        filepath = self.output_dir / f"{prefix}_{timestamp}.md"
        
        # Sort impacts by score
        sorted_impacts = sorted(result.impacts, key=lambda x: x.impact_score, reverse=True)
        
        # Peak hours note
        peak_note = "\n⚠️ **Peak Hours Active:** Impact scores include 1.2x multiplier\n" if result.peak_hours else ""
        
        # Build report content
        content = f"""# NexDex Business Impact Report

**Generated:** {result.timestamp.strftime("%Y-%m-%d %H:%M:%S")}{peak_note}

---

## Executive Summary

- **Failed Services:** {', '.join(result.failed_services)}
- **Total Services Affected:** {result.total_services_affected}
- **Total Impact Score:** {result.total_impact_score:.2f}{"  (1.2x peak hours)" if result.peak_hours else ""}
- **Business Processes Affected:** {len(result.affected_business_processes)}

### Affected Business Processes
{self._format_business_processes(result)}

---

## Impact Analysis

### Impact Score Distribution
"""
        
        # Add impact table
        content += "\n| Service | Type | Business Process | Impact Score | Downtime (min) | Cascade Depth |\n"
        content += "|---------|------|------------------|--------------|----------------|---------------|\n"
        
        for impact in sorted_impacts:
            failure_type = "Direct" if impact.is_direct_failure else "Cascade"
            bp = impact.affected_business_processes[0] if impact.affected_business_processes else "N/A"
            content += f"| {impact.service.name} | {failure_type} | {bp} | "
            content += f"{impact.impact_score:.2f} | {impact.estimated_downtime} | {impact.cascade_depth} |\n"
        
        # Add detailed breakdown
        content += "\n---\n\n## Detailed Impact Breakdown\n\n"
        
        for i, impact in enumerate(sorted_impacts, 1):
            content += f"### {i}. {impact.service.name}\n\n"
            content += f"**Failure Type:** {'Direct Failure' if impact.is_direct_failure else 'Cascading Failure'}\n\n"
            content += f"**Impact Score:** {impact.impact_score:.2f}\n\n"
            content += f"**Business Process:** {impact.affected_business_processes[0] if impact.affected_business_processes else 'None'}\n\n"
            content += f"**Service Importance:** {impact.service.importance}/10\n\n"
            content += f"**Estimated Downtime:** {impact.estimated_downtime} minutes\n\n"
            content += f"**Cascade Depth:** {impact.cascade_depth} hop(s) from original failure\n\n"
            
            if impact.dependent_services:
                content += f"**Services Depending on This:** {', '.join(impact.dependent_services)}\n\n"
            else:
                content += f"**Services Depending on This:** None (leaf service)\n\n"
            
            if impact.service.description:
                content += f"**Description:** {impact.service.description}\n\n"
            
            content += "---\n\n"
        
        # Add recommendations
        content += self._generate_recommendations(result, sorted_impacts)
        
        # Write file
        with open(filepath, 'w') as f:
            f.write(content)
        
        return str(filepath)
    
    def generate_html_report(
        self,
        result: SimulationResult,
        dependency_manager: DependencyManager,
        prefix: str = "impact_report",
        timestamp: Optional[str] = None
    ) -> str:
        """Generate an HTML report with styling"""
        if timestamp is None:
            timestamp = result.timestamp.strftime("%Y%m%d_%H%M%S")
        
        filepath = self.output_dir / f"{prefix}_{timestamp}.html"
        
        sorted_impacts = sorted(result.impacts, key=lambda x: x.impact_score, reverse=True)
        
        # HTML template
        template = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NexDex Impact Report</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { color: #2c3e50; margin-bottom: 10px; }
        h2 { color: #34495e; margin-top: 30px; margin-bottom: 15px; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        h3 { color: #555; margin-top: 20px; margin-bottom: 10px; }
        .timestamp { color: #7f8c8d; font-size: 0.9em; margin-bottom: 30px; }
        .summary {
            background: #ecf0f1;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        .summary-item {
            background: white;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #3498db;
        }
        .summary-item strong { display: block; color: #7f8c8d; font-size: 0.85em; margin-bottom: 5px; }
        .summary-item .value { font-size: 1.5em; color: #2c3e50; font-weight: bold; }
        .alert { background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; border-radius: 5px; }
        .alert-danger { background: #f8d7da; border-left-color: #dc3545; }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background: #3498db;
            color: white;
            font-weight: 600;
        }
        tr:hover { background: #f8f9fa; }
        .badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 3px;
            font-size: 0.85em;
            font-weight: 600;
        }
        .badge-direct { background: #dc3545; color: white; }
        .badge-cascade { background: #ffc107; color: #333; }
        .impact-card {
            background: #f8f9fa;
            padding: 20px;
            margin: 15px 0;
            border-radius: 5px;
            border-left: 4px solid #3498db;
        }
        .impact-high { border-left-color: #dc3545; }
        .impact-medium { border-left-color: #ffc107; }
        .impact-low { border-left-color: #28a745; }
        .score {
            display: inline-block;
            padding: 5px 10px;
            background: #3498db;
            color: white;
            border-radius: 20px;
            font-weight: bold;
        }
        ul { margin: 10px 0 10px 20px; }
        .recommendations { background: #d1ecf1; border-left: 4px solid #17a2b8; padding: 20px; margin: 20px 0; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚨 NexDex Business Impact Report</h1>
        <div class="timestamp">Generated: {{ timestamp }}</div>
        
        <div class="alert alert-danger">
            <strong>⚠️ Simulated Failure:</strong> {{ failed_services }}
        </div>
        
        <div class="summary">
            <h2>Executive Summary</h2>
            <div class="summary-grid">
                <div class="summary-item">
                    <strong>Total Services Affected</strong>
                    <div class="value">{{ total_services }}</div>
                </div>
                <div class="summary-item">
                    <strong>Total Impact Score</strong>
                    <div class="value">{{ total_impact }}</div>
                </div>
                <div class="summary-item">
                    <strong>Business Processes</strong>
                    <div class="value">{{ business_processes_count }}</div>
                </div>
                <div class="summary-item">
                    <strong>Cascade Failures</strong>
                    <div class="value">{{ cascade_count }}</div>
                </div>
            </div>
        </div>
        
        <h2>📊 Impact Analysis</h2>
        <table>
            <thead>
                <tr>
                    <th>Service</th>
                    <th>Type</th>
                    <th>Business Process</th>
                    <th>Impact Score</th>
                    <th>Downtime (min)</th>
                    <th>Cascade Depth</th>
                </tr>
            </thead>
            <tbody>
                {% for impact in impacts %}
                <tr>
                    <td><strong>{{ impact.service.name }}</strong></td>
                    <td>
                        {% if impact.is_direct_failure %}
                        <span class="badge badge-direct">Direct</span>
                        {% else %}
                        <span class="badge badge-cascade">Cascade</span>
                        {% endif %}
                    </td>
                    <td>{{ impact.business_process }}</td>
                    <td><span class="score">{{ "%.2f"|format(impact.impact_score) }}</span></td>
                    <td>{{ impact.estimated_downtime }}</td>
                    <td>{{ impact.cascade_depth }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        
        <h2>📋 Detailed Breakdown</h2>
        {% for impact in impacts %}
        <div class="impact-card {% if impact.impact_score > 500 %}impact-high{% elif impact.impact_score > 200 %}impact-medium{% else %}impact-low{% endif %}">
            <h3>{{ loop.index }}. {{ impact.service.name }}</h3>
            <p><strong>Impact Score:</strong> <span class="score">{{ "%.2f"|format(impact.impact_score) }}</span></p>
            <p><strong>Failure Type:</strong> {% if impact.is_direct_failure %}Direct Failure{% else %}Cascading Failure ({{ impact.cascade_depth }} hop(s)){% endif %}</p>
            <p><strong>Business Process:</strong> {{ impact.business_process }}</p>
            <p><strong>Service Importance:</strong> {{ impact.service.importance }}/10</p>
            <p><strong>Estimated Downtime:</strong> {{ impact.estimated_downtime }} minutes</p>
            {% if impact.dependent_services %}
            <p><strong>Services Depending on This:</strong> {{ impact.dependent_services|join(', ') }}</p>
            {% endif %}
        </div>
        {% endfor %}
        
        <div class="recommendations">
            <h2>💡 Recommendations</h2>
            <ul>
                <li>Consider implementing redundancy for high-impact services</li>
                <li>Review and optimize MTTR for critical services</li>
                <li>Implement circuit breakers to prevent cascade failures</li>
                <li>Regular disaster recovery drills for affected business processes</li>
                <li>Monitor dependencies and set up alerting for critical paths</li>
            </ul>
        </div>
    </div>
</body>
</html>
        """)
        
        # Prepare data for template
        html_content = template.render(
            timestamp=result.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            failed_services=', '.join(result.failed_services),
            total_services=result.total_services_affected,
            total_impact=f"{result.total_impact_score:.2f}",
            business_processes_count=len(result.affected_business_processes),
            cascade_count=len([i for i in result.impacts if not i.is_direct_failure]),
            impacts=[{
                'service': {'name': i.service.name, 'importance': i.service.importance},
                'is_direct_failure': i.is_direct_failure,
                'business_process': i.affected_business_processes[0] if i.affected_business_processes else 'N/A',
                'impact_score': i.impact_score,
                'estimated_downtime': i.estimated_downtime,
                'cascade_depth': i.cascade_depth,
                'dependent_services': i.dependent_services
            } for i in sorted_impacts]
        )
        
        with open(filepath, 'w') as f:
            f.write(html_content)
        
        return str(filepath)
    
    def generate_graph_visualization(
        self,
        result: SimulationResult,
        dependency_manager: DependencyManager,
        prefix: str = "impact_graph",
        timestamp: Optional[str] = None
    ) -> str:
        """Generate a visual dependency graph with failed services highlighted"""
        if timestamp is None:
            timestamp = result.timestamp.strftime("%Y%m%d_%H%M%S")
        
        filepath = self.output_dir / f"{prefix}_{timestamp}.png"
        
        # Create figure
        plt.figure(figsize=(14, 10))
        
        # Get the graph
        G = dependency_manager.graph
        
        # Use hierarchical layout
        try:
            pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
        except:
            pos = nx.circular_layout(G)
        
        # Categorize nodes
        failed_nodes = result.failed_services
        affected_nodes = [i.service.name for i in result.impacts if not i.is_direct_failure]
        normal_nodes = [n for n in G.nodes() if n not in failed_nodes and n not in affected_nodes]
        
        # Draw nodes with different colors
        nx.draw_networkx_nodes(G, pos, nodelist=normal_nodes, node_color='lightblue', 
                               node_size=1500, alpha=0.7, label='Normal')
        nx.draw_networkx_nodes(G, pos, nodelist=affected_nodes, node_color='orange', 
                               node_size=1500, alpha=0.8, label='Affected')
        nx.draw_networkx_nodes(G, pos, nodelist=failed_nodes, node_color='red', 
                               node_size=2000, alpha=0.9, label='Failed')
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, 
                               arrowsize=20, arrowstyle='->', alpha=0.5, width=2)
        
        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold')
        
        plt.title(f"Service Dependency Graph - Impact Simulation\nFailed: {', '.join(failed_nodes)}", 
                  fontsize=14, fontweight='bold', pad=20)
        plt.legend(loc='upper left', fontsize=10)
        plt.axis('off')
        plt.tight_layout()
        
        # Save
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return str(filepath)
    
    def _format_business_processes(self, result: SimulationResult) -> str:
        """Format business processes list"""
        if not result.affected_business_processes:
            return "- None\n"
        return "\n".join([f"- {bp}" for bp in sorted(result.affected_business_processes)])
    
    def _generate_recommendations(self, result: SimulationResult, sorted_impacts) -> str:
        """Generate recommendations based on simulation"""
        content = "## Recommendations\n\n"
        
        # High impact services
        high_impact = [i for i in sorted_impacts if i.impact_score > 300]
        if high_impact:
            content += "### High Priority Actions\n\n"
            content += "The following services have critical impact and require immediate attention:\n\n"
            for impact in high_impact[:3]:
                content += f"- **{impact.service.name}**: Implement redundancy and reduce MTTR (currently {impact.estimated_downtime} min)\n"
            content += "\n"
        
        # Multiple business processes
        if len(result.affected_business_processes) > 3:
            content += "### Business Continuity\n\n"
            content += f"This failure affects {len(result.affected_business_processes)} business processes. Consider:\n"
            content += "- Implementing circuit breakers to prevent cascade failures\n"
            content += "- Creating business continuity plans for critical processes\n"
            content += "- Regular disaster recovery drills\n\n"
        
        # General recommendations
        content += "### General Best Practices\n\n"
        content += "- Monitor critical dependencies and set up alerting\n"
        content += "- Implement health checks and automatic failover\n"
        content += "- Regular dependency audits and updates\n"
        content += "- Document recovery procedures for each service\n"
        
        return content
    def generate_comparison_markdown_report(self, comparison_data: dict) -> str:
        """Generate a comparison Markdown report between two simulation results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = self.output_dir / f"comparison_report_{timestamp}.md"
        
        result1 = comparison_data["result1"]
        result2 = comparison_data["result2"]
        summary1 = comparison_data["summary1"]
        summary2 = comparison_data["summary2"]
        
        content = "# NexDex Scenario Comparison Report\n\n"
        content += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        content += "## Scenario Overview\n\n"
        content += f"**Scenario 1:** {', '.join(result1.failed_services)}\n"
        content += f"**Scenario 2:** {', '.join(result2.failed_services)}\n\n"
        
        # Impact comparison table
        content += "## Impact Comparison\n\n"
        content += "| Metric | Scenario 1 | Scenario 2 | Difference |\n"
        content += "|--------|-----------|-----------|------------|\n"
        
        impact_diff = comparison_data["impact_diff"]
        impact_symbol = "📈" if impact_diff > 0 else "📉" if impact_diff < 0 else "➡️"
        content += (
            f"| Total Impact Score | {summary1['total_impact_score']:.2f} | "
            f"{summary2['total_impact_score']:.2f} | {impact_symbol} "
            f"{abs(impact_diff):.2f} ({comparison_data['impact_pct_diff']:+.1f}%) |\n"
        )
        
        services_diff = comparison_data["services_diff"]
        services_symbol = "📈" if services_diff > 0 else "📉" if services_diff < 0 else "➡️"
        content += (
            f"| Services Affected | {summary1['total_services_affected']} | "
            f"{summary2['total_services_affected']} | {services_symbol} {abs(services_diff)} |\n"
        )
        
        content += (
            f"| Business Processes | {summary1['business_processes_affected']} | "
            f"{summary2['business_processes_affected']} | "
            f"{summary2['business_processes_affected'] - summary1['business_processes_affected']:+d} |\n"
        )
        
        content += (
            f"| Direct Failures | {summary1['direct_failures']} | "
            f"{summary2['direct_failures']} | "
            f"{summary2['direct_failures'] - summary1['direct_failures']:+d} |\n"
        )
        
        content += (
            f"| Cascade Failures | {summary1['cascade_failures']} | "
            f"{summary2['cascade_failures']} | "
            f"{summary2['cascade_failures'] - summary1['cascade_failures']:+d} |\n"
        )
        
        content += "\n"
        
        # Which scenario is worse
        worse = comparison_data["worse_scenario"]
        worse_label = "Scenario 2" if worse == result2 else "Scenario 1"
        content += f"**Conclusion:** {worse_label} has greater business impact.\n\n"
        
        # Affected services analysis
        content += "## Affected Services Analysis\n\n"
        unique_to_first = comparison_data["unique_to_first"]
        unique_to_second = comparison_data["unique_to_second"]
        common = comparison_data["common_services"]
        
        if unique_to_first:
            content += f"### Unique to Scenario 1\n\n"
            content += f"Services only affected in Scenario 1: {', '.join(sorted(unique_to_first))}\n\n"
        
        if unique_to_second:
            content += f"### Unique to Scenario 2\n\n"
            content += f"Services only affected in Scenario 2: {', '.join(sorted(unique_to_second))}\n\n"
        
        if common:
            content += f"### Common to Both Scenarios\n\n"
            content += f"Services affected in both: {', '.join(sorted(common))}\n\n"
        
        # Highest impact services
        content += "## Highest Impact Services\n\n"
        if comparison_data["highest1"]:
            content += f"**Scenario 1:** {comparison_data['highest1'].service.name} "
            content += f"(Impact: {comparison_data['highest1'].impact_score:.2f})\n"
        if comparison_data["highest2"]:
            content += f"**Scenario 2:** {comparison_data['highest2'].service.name} "
            content += f"(Impact: {comparison_data['highest2'].impact_score:.2f})\n"
        
        content += "\n---\n*End of Comparison Report*\n"
        
        with open(filepath, "w") as f:
            f.write(content)
        
        return str(filepath)

    def generate_comparison_html_report(self, comparison_data: dict, dependency_manager) -> str:
        """Generate a comparison HTML report with styling"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = self.output_dir / f"comparison_report_{timestamp}.html"
        
        result1 = comparison_data["result1"]
        result2 = comparison_data["result2"]
        summary1 = comparison_data["summary1"]
        summary2 = comparison_data["summary2"]
        
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NexDex Scenario Comparison</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { font-size: 1.1em; opacity: 0.9; }
        .content { padding: 40px; }
        .comparison-table {
            width: 100%;
            border-collapse: collapse;
            margin: 30px 0;
            font-size: 1em;
        }
        .comparison-table th {
            background: #f5f5f5;
            padding: 15px;
            text-align: left;
            border-bottom: 2px solid #667eea;
            font-weight: 600;
            color: #667eea;
        }
        .comparison-table td {
            padding: 12px 15px;
            border-bottom: 1px solid #e0e0e0;
        }
        .comparison-table tr:hover { background: #f9f9f9; }
        .metric-label { font-weight: 600; color: #667eea; }
        .value-positive { color: #28a745; font-weight: 600; }
        .value-negative { color: #dc3545; font-weight: 600; }
        .value-neutral { color: #666; }
        .scenario-row {
            background: #f0f4ff;
            font-weight: 600;
        }
        .comparison-card {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin: 30px 0;
        }
        .card {
            padding: 20px;
            background: #f9f9f9;
            border-left: 4px solid #667eea;
            border-radius: 4px;
        }
        .card h3 { color: #667eea; margin-bottom: 15px; }
        .card-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #e0e0e0;
        }
        .card-item:last-child { border-bottom: none; }
        .card-label { font-weight: 500; color: #666; }
        .card-value { font-weight: 700; color: #333; }
        .section { margin: 30px 0; }
        .section h2 {
            color: #667eea;
            font-size: 1.5em;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }
        .worse-scenario {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 20px;
            border-radius: 4px;
            margin: 20px 0;
        }
        .unique-services {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 20px 0;
        }
        .service-list {
            padding: 15px;
            background: #f5f5f5;
            border-radius: 4px;
            border-left: 4px solid #667eea;
        }
        .service-list h4 { color: #667eea; margin-bottom: 10px; }
        .service-list ul { list-style: none; }
        .service-list li {
            padding: 5px 0;
            color: #666;
        }
        .service-list li:before {
            content: "▸ ";
            color: #667eea;
            font-weight: bold;
            margin-right: 5px;
        }
        .footer {
            background: #f5f5f5;
            padding: 20px 40px;
            text-align: center;
            color: #999;
            font-size: 0.9em;
            border-top: 1px solid #e0e0e0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Scenario Comparison Report</h1>
            <p>NexDex Business Impact Analysis</p>
        </div>
        <div class="content">
            <div class="section">
                <h2>Scenarios Being Compared</h2>
                <div class="comparison-card">
                    <div class="card">
                        <h3>Scenario 1</h3>
                        <div class="card-item">
                            <span class="card-label">Failed Services:</span>
                            <span class="card-value">{{ failed_services_1|join(', ') }}</span>
                        </div>
                    </div>
                    <div class="card">
                        <h3>Scenario 2</h3>
                        <div class="card-item">
                            <span class="card-label">Failed Services:</span>
                            <span class="card-value">{{ failed_services_2|join(', ') }}</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>Impact Metrics Comparison</h2>
                <table class="comparison-table">
                    <thead>
                        <tr class="scenario-row">
                            <th>Metric</th>
                            <th>Scenario 1</th>
                            <th>Scenario 2</th>
                            <th>Difference</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td class="metric-label">Total Impact Score</td>
                            <td>{{ summary1['total_impact_score']|round(2) }}</td>
                            <td>{{ summary2['total_impact_score']|round(2) }}</td>
                            <td class="{% if impact_diff > 0 %}value-negative{% elif impact_diff < 0 %}value-positive{% else %}value-neutral{% endif %}">
                                {{ impact_diff|round(2) }} ({{ impact_pct_diff|round(1) }}%)
                            </td>
                        </tr>
                        <tr>
                            <td class="metric-label">Services Affected</td>
                            <td>{{ summary1['total_services_affected'] }}</td>
                            <td>{{ summary2['total_services_affected'] }}</td>
                            <td class="{% if services_diff > 0 %}value-negative{% elif services_diff < 0 %}value-positive{% else %}value-neutral{% endif %}">
                                {{ services_diff_formatted }}
                            </td>
                        </tr>
                        <tr>
                            <td class="metric-label">Business Processes</td>
                            <td>{{ summary1['business_processes_affected'] }}</td>
                            <td>{{ summary2['business_processes_affected'] }}</td>
                            <td class="{% if proc_diff > 0 %}value-negative{% else %}value-positive{% endif %}">
                                {{ proc_diff_formatted }}
                            </td>
                        </tr>
                        <tr>
                            <td class="metric-label">Direct Failures</td>
                            <td>{{ summary1['direct_failures'] }}</td>
                            <td>{{ summary2['direct_failures'] }}</td>
                            <td class="value-neutral">
                                {{ direct_diff_formatted }}
                            </td>
                        </tr>
                        <tr>
                            <td class="metric-label">Cascade Failures</td>
                            <td>{{ summary1['cascade_failures'] }}</td>
                            <td>{{ summary2['cascade_failures'] }}</td>
                            <td class="{% if cascade_diff > 0 %}value-negative{% else %}value-positive{% endif %}">
                                {{ cascade_diff_formatted }}
                            </td>
                        </tr>
                        <tr>
                            <td class="metric-label">Avg Impact/Service</td>
                            <td>{{ summary1['average_impact_per_service']|round(2) }}</td>
                            <td>{{ summary2['average_impact_per_service']|round(2) }}</td>
                            <td class="value-neutral">
                                {{ avg_diff_formatted }}
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div class="section">
                <div class="worse-scenario">
                    <h3>⚠️ Key Insight</h3>
                    <p><strong>{{ worse_scenario_label }}</strong> has {{ "GREATER" if is_worse_scenario_2 else "LOWER" }} business impact 
                    {{ (impact_diff|abs)|round(2) }} impact points ({{ (impact_pct_diff|abs)|round(1) }}%) 
                    {{ "MORE severe" if is_worse_scenario_2 else "LESS severe" }}.</p>
                </div>
            </div>
            
            <div class="section">
                <h2>Affected Services Analysis</h2>
                <div class="unique-services">
                    {% if unique_to_first %}
                    <div class="service-list">
                        <h4>🔴 Unique to Scenario 1</h4>
                        <ul>
                            {% for service in unique_to_first|sort %}
                            <li>{{ service }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                    {% endif %}
                    {% if unique_to_second %}
                    <div class="service-list">
                        <h4>🔴 Unique to Scenario 2</h4>
                        <ul>
                            {% for service in unique_to_second|sort %}
                            <li>{{ service }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                    {% endif %}
                </div>
                {% if common_services %}
                <div class="service-list" style="grid-column: 1 / -1;">
                    <h4>🟡 Affected in Both Scenarios</h4>
                    <ul>
                        {% for service in common_services|sort %}
                        <li>{{ service }}</li>
                        {% endfor %}
                    </ul>
                </div>
                {% endif %}
            </div>
            
            <div class="section">
                <h2>Highest Impact Services</h2>
                <div class="comparison-card">
                    {% if highest1 %}
                    <div class="card">
                        <h3>Scenario 1</h3>
                        <div class="card-item">
                            <span class="card-label">Service:</span>
                            <span class="card-value">{{ highest1['service_name'] }}</span>
                        </div>
                        <div class="card-item">
                            <span class="card-label">Impact Score:</span>
                            <span class="card-value">{{ highest1['impact_score']|round(2) }}</span>
                        </div>
                    </div>
                    {% endif %}
                    {% if highest2 %}
                    <div class="card">
                        <h3>Scenario 2</h3>
                        <div class="card-item">
                            <span class="card-label">Service:</span>
                            <span class="card-value">{{ highest2['service_name'] }}</span>
                        </div>
                        <div class="card-item">
                            <span class="card-label">Impact Score:</span>
                            <span class="card-value">{{ highest2['impact_score']|round(2) }}</span>
                        </div>
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>
        <div class="footer">
            <p>Generated on {{ generated_at }} | NexDex v1.0.0</p>
        </div>
    </div>
</body>
</html>
        """
        
        # Prepare template data
        # Helper function to format numbers with + sign
        def format_diff(value):
            if value > 0:
                return f"+{int(value)}"
            else:
                return str(int(value))
        
        # Calculate differences
        proc_diff = summary2['business_processes_affected'] - summary1['business_processes_affected']
        direct_diff = summary2['direct_failures'] - summary1['direct_failures']
        cascade_diff = summary2['cascade_failures'] - summary1['cascade_failures']
        avg_diff = summary2['average_impact_per_service'] - summary1['average_impact_per_service']
        
        template_data = {
            "failed_services_1": result1.failed_services,
            "failed_services_2": result2.failed_services,
            "summary1": summary1,
            "summary2": summary2,
            "impact_diff": comparison_data["impact_diff"],
            "impact_pct_diff": comparison_data["impact_pct_diff"],
            "services_diff": comparison_data["services_diff"],
            "services_diff_formatted": format_diff(comparison_data["services_diff"]),
            "proc_diff": proc_diff,
            "proc_diff_formatted": format_diff(proc_diff),
            "direct_diff": direct_diff,
            "direct_diff_formatted": format_diff(direct_diff),
            "cascade_diff": cascade_diff,
            "cascade_diff_formatted": format_diff(cascade_diff),
            "avg_diff_formatted": f"{avg_diff:+.2f}",
            "unique_to_first": list(comparison_data["unique_to_first"]),
            "unique_to_second": list(comparison_data["unique_to_second"]),
            "common_services": list(comparison_data["common_services"]),
            "highest1": {
                "service_name": comparison_data["highest1"].service.name,
                "impact_score": comparison_data["highest1"].impact_score
            } if comparison_data["highest1"] else None,
            "highest2": {
                "service_name": comparison_data["highest2"].service.name,
                "impact_score": comparison_data["highest2"].impact_score
            } if comparison_data["highest2"] else None,
            "worse_scenario_label": "Scenario 2" if comparison_data["worse_scenario"] == result2 else "Scenario 1",
            "is_worse_scenario_2": comparison_data["worse_scenario"] == result2,
            "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        template = Template(html_template)
        html_content = template.render(**template_data)
        
        with open(filepath, "w") as f:
            f.write(html_content)
        
        return str(filepath)