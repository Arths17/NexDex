#!/usr/bin/env python3
"""
NexDex - Cross-System Business Impact Simulator
Main CLI interface
"""
import argparse
import sys
import json
import webbrowser
from pathlib import Path
from datetime import datetime
from typing import List

try:
    from colorama import init, Fore, Style
    init()
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    # Fallback for when colorama is not installed
    class Fore:
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"
        CYAN = "\033[36m"
        MAGENTA = "\033[35m"
        WHITE = "\033[37m"
        RESET = "\033[0m"
    class Style:
        BRIGHT = "\033[1m"
        DIM = "\033[2m"
        RESET_ALL = "\033[0m"

from tabulate import tabulate

from src.dependency_manager import DependencyManager
from src.simulation_engine import SimulationEngine
from src.report_generator import ReportGenerator
from src.models import Scenario


def print_colored(text: str, color=Fore.WHITE, bright=False):
    """Print colored text if colorama is available"""
    if COLORS_AVAILABLE:
        if bright:
            print(f"{Style.BRIGHT}{color}{text}{Style.RESET_ALL}")
        else:
            print(f"{color}{text}{Style.RESET_ALL}")
    else:
        print(text)


def print_banner():
    """Print NexDex banner"""
    banner = """
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║   ███╗   ██╗███████╗██╗  ██╗██████╗ ███████╗██╗  ██╗ ║
║   ████╗  ██║██╔════╝╚██╗██╔╝██╔══██╗██╔════╝╚██╗██╔╝ ║
║   ██╔██╗ ██║█████╗   ╚███╔╝ ██║  ██║█████╗   ╚███╔╝  ║
║   ██║╚██╗██║██╔══╝   ██╔██╗ ██║  ██║██╔══╝   ██╔██╗  ║
║   ██║ ╚████║███████╗██╔╝ ██╗██████╔╝███████╗██╔╝ ██╗ ║
║   ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝ ║
║                                                       ║
║        Cross-System Business Impact Simulator        ║
╚═══════════════════════════════════════════════════════╝
    """
    print_colored(banner, Fore.CYAN, bright=True)


def list_services(dependency_manager: DependencyManager):
    """List all services with their details"""
    services = dependency_manager.get_all_services()
    
    if not services:
        print_colored("No services configured.", Fore.YELLOW)
        return
    
    # Prepare table data
    table_data = []
    for service in sorted(services, key=lambda s: s.name):
        deps = ", ".join(service.depends_on) if service.depends_on else "None"
        dependents = dependency_manager.get_dependents(service.name)
        dep_count = len(dependents)
        process_importance = (
            dependency_manager.get_process_importance(service.business_process)
            if service.business_process else None
        )
        
        table_data.append([
            service.name,
            service.business_process or "N/A",
            service.importance,
            process_importance if process_importance is not None else "-",
            service.mttr,
            deps,
            dep_count
        ])
    
    headers = ["Service", "Business Process", "Service Importance", "Process Importance", "MTTR (min)", "Depends On", "Dependents"]
    print_colored("\n📋 Configured Services:\n", Fore.CYAN, bright=True)
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # Show statistics
    stats = dependency_manager.get_graph_stats()
    print_colored(f"\n📊 Statistics:", Fore.CYAN, bright=True)
    print(f"  Total Services: {stats['total_services']}")
    print(f"  Total Dependencies: {stats['total_dependencies']}")
    print(f"  Circular Dependencies: {stats['circular_dependencies']}")
    
    if stats['most_critical']:
        print_colored(f"\n🔥 Most Critical Services:", Fore.RED, bright=True)
        for service_name, dependent_count in stats['most_critical']:
            print(f"  - {service_name}: {dependent_count} dependent services")


def run_simulation(
    dependency_manager: DependencyManager,
    failed_services: List[str],
    generate_reports: bool = True,
    save_scenario: str = None,
    show_ascii_graph: bool = False,
    open_report: bool = False,
    peak_hours: bool = False
):
    """Run a failure simulation"""
    peak_label = " (PEAK HOURS 🔴)" if peak_hours else ""
    print_colored(f"\n🚨 Simulating failure of: {', '.join(failed_services)}{peak_label}", Fore.RED, bright=True)
    
    # Validate services
    for service in failed_services:
        if service not in dependency_manager.services:
            print_colored(f"Error: Service '{service}' not found!", Fore.RED)
            print_colored("Use --list to see available services.", Fore.YELLOW)
            return
    
    # Run simulation
    engine = SimulationEngine(dependency_manager)
    result = engine.simulate_failure(failed_services, peak_hours=peak_hours)
    
    # Display results
    print_colored(f"\n✅ Simulation Complete", Fore.GREEN, bright=True)
    print(f"Timestamp: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Summary
    summary = engine.get_impact_summary(result)
    print_colored("📊 Impact Summary:", Fore.CYAN, bright=True)
    print(f"  Total Services Affected: {summary['total_services_affected']}")
    print(f"  Direct Failures: {summary['direct_failures']}")
    print(f"  Cascade Failures: {summary['cascade_failures']}")
    print(f"  Business Processes Affected: {summary['business_processes_affected']}")
    impact_note = f" (1.2x peak multiplier applied)" if result.peak_hours else ""
    print(f"  Total Impact Score: {summary['total_impact_score']:.2f}{impact_note}")
    print(f"  Highest Impact Service: {summary['highest_impact_service']}")
    
    # Business processes
    if result.affected_business_processes:
        print_colored(f"\n💼 Affected Business Processes:", Fore.MAGENTA, bright=True)
        for bp in sorted(result.affected_business_processes):
            print(f"  - {bp}")
    
    # Impact details table
    print_colored(f"\n📋 Detailed Impact Analysis:", Fore.CYAN, bright=True)
    table_data = []
    for impact in sorted(result.impacts, key=lambda x: x.impact_score, reverse=True):
        failure_type = "Direct" if impact.is_direct_failure else f"Cascade ({impact.cascade_depth})"
        bp = impact.affected_business_processes[0] if impact.affected_business_processes else "N/A"
        process_importance = (
            dependency_manager.get_process_importance(bp)
            if bp != "N/A" else None
        )
        effective_importance = process_importance if process_importance is not None else impact.service.importance
        
        table_data.append([
            impact.service.name,
            failure_type,
            bp,
            f"{impact.impact_score:.2f}",
            impact.estimated_downtime,
            f"{effective_importance}/10"
        ])
    
    headers = ["Service", "Type", "Business Process", "Impact Score", "Downtime (min)", "Importance"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

    # Top 5 impacted business processes
    top_processes = engine.get_top_business_processes(result, limit=5)
    if top_processes:
        print_colored(f"\n🎯 Top 5 Impacted Business Processes:", Fore.MAGENTA, bright=True)
        proc_table = []
        for process, impact_score in top_processes:
            proc_table.append([process, f"{impact_score:.2f}"])
        print(tabulate(proc_table, headers=["Process", "Total Impact Score"], tablefmt="grid"))

    if show_ascii_graph:
        print_ascii_graph(dependency_manager, failed_services, result)
    
    reports = None

    # Generate reports
    if generate_reports:
        print_colored(f"\n📄 Generating Reports...", Fore.CYAN)
        report_gen = ReportGenerator()
        reports = report_gen.generate_all_reports(result, dependency_manager)
        
        print_colored("✅ Reports generated:", Fore.GREEN)
        for report_type, filepath in reports.items():
            print(f"  - {report_type.upper()}: {filepath}")

        if open_report and reports.get("html"):
            try:
                webbrowser.open(reports["html"])
                print_colored("🌐 Opened HTML report in your default browser", Fore.GREEN)
            except Exception as e:
                print_colored(f"⚠️  Failed to open browser: {e}", Fore.YELLOW)
    
    # Save scenario
    if save_scenario:
        save_scenario_to_file(failed_services, save_scenario)
        print_colored(f"\n💾 Scenario saved as: {save_scenario}", Fore.GREEN)

    return reports


def save_scenario_to_file(failed_services: List[str], scenario_name: str):
    """Save a scenario to file"""
    scenarios_dir = Path("scenarios")
    scenarios_dir.mkdir(exist_ok=True)
    
    scenario = Scenario(
        name=scenario_name,
        description=f"Failure of: {', '.join(failed_services)}",
        failed_services=failed_services
    )
    
    filepath = scenarios_dir / f"{scenario_name}.json"
    with open(filepath, 'w') as f:
        json.dump(scenario.to_dict(), f, indent=2)


def load_scenario_from_file(scenario_name: str) -> Scenario:
    """Load a scenario from file"""
    scenarios_dir = Path("scenarios")
    filepath = scenarios_dir / f"{scenario_name}.json"
    
    if not filepath.exists():
        raise FileNotFoundError(f"Scenario '{scenario_name}' not found")
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    return Scenario.from_dict(data)


def list_scenarios(filter_tag: str = None):
    """List all saved scenarios, optionally filtered by tag"""
    scenarios_dir = Path("scenarios")
    
    if not scenarios_dir.exists():
        print_colored("No scenarios saved yet.", Fore.YELLOW)
        return
    
    scenario_files = list(scenarios_dir.glob("*.json"))
    
    if not scenario_files:
        print_colored("No scenarios saved yet.", Fore.YELLOW)
        return
    
    print_colored("\n💾 Saved Scenarios:\n", Fore.CYAN, bright=True)
    
    table_data = []
    for filepath in sorted(scenario_files):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            scenario = Scenario.from_dict(data)
            
            # Filter by tag if specified
            if filter_tag and filter_tag.lower() not in [t.lower() for t in scenario.tags]:
                continue
            
            tags_str = ", ".join(scenario.tags) if scenario.tags else "(none)"
            table_data.append([
                scenario.name,
                ", ".join(scenario.failed_services),
                scenario.created_at.strftime("%Y-%m-%d %H:%M"),
                tags_str,
                scenario.description[:40] + ("..." if len(scenario.description) > 40 else "")
            ])
        except Exception as e:
            print_colored(f"Error loading {filepath.name}: {e}", Fore.RED)
    
    if not table_data:
        tag_msg = f" with tag '{filter_tag}'" if filter_tag else ""
        print_colored(f"No scenarios found{tag_msg}.", Fore.YELLOW)
        return
    
    headers = ["Name", "Failed Services", "Created", "Tags", "Description"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def validate_config(dependency_manager: DependencyManager):
    """Validate the configuration"""
    print_colored("\n🔍 Validating configuration...\n", Fore.CYAN, bright=True)
    
    errors = dependency_manager.validate_dependencies()
    
    if errors:
        print_colored("❌ Configuration Errors Found:", Fore.RED, bright=True)
        for error in errors:
            print(f"  - {error}")
    else:
        print_colored("✅ Configuration is valid!", Fore.GREEN, bright=True)
    
    # Check for circular dependencies
    cycles = dependency_manager.detect_circular_dependencies()
    if cycles:
        print_colored("\n⚠️  Circular Dependencies Detected:", Fore.YELLOW, bright=True)
        for cycle in cycles:
            print(f"  - {' -> '.join(cycle + [cycle[0]])}")
    else:
        print_colored("✅ No circular dependencies found.", Fore.GREEN)


def resolve_scenario_paths(patterns: List[str]) -> List[Path]:
    """Resolve scenario file paths from patterns and globs"""
    paths = []
    for pattern in patterns:
        if any(ch in pattern for ch in ["*", "?", "["]):
            for p in Path(".").glob(pattern):
                if p.is_file() and p.suffix.lower() == ".json":
                    paths.append(p)
        else:
            p = Path(pattern)
            if p.is_dir():
                for f in p.glob("*.json"):
                    paths.append(f)
            else:
                paths.append(p)
    
    # De-duplicate while preserving order
    seen = set()
    unique = []
    for p in paths:
        key = str(p.resolve())
        if key not in seen:
            seen.add(key)
            unique.append(p)
    return unique


def run_batch_scenarios(
    dependency_manager: DependencyManager,
    patterns: List[str],
    generate_reports: bool = True,
    open_report: bool = False
):
    """Run multiple scenarios and generate a combined report"""
    scenario_paths = resolve_scenario_paths(patterns)
    if not scenario_paths:
        print_colored("❌ No scenario files found for batch run.", Fore.RED)
        return
    
    scenarios = []
    for path in scenario_paths:
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            scenarios.append(Scenario.from_dict(data))
        except Exception as e:
            print_colored(f"❌ Failed to load {path}: {e}", Fore.RED)
            return
    
    engine = SimulationEngine(dependency_manager)
    results = []
    for scenario in scenarios:
        result = engine.simulate_failure(scenario.failed_services, peak_hours=scenario.peak_hours)
        results.append(result)
    
    print_colored("\n✅ Batch simulation complete", Fore.GREEN, bright=True)
    for scenario, result in zip(scenarios, results):
        print_colored(f"  - {scenario.name}: {result.total_impact_score:.2f} total impact", Fore.CYAN)
    
    if generate_reports:
        report_gen = ReportGenerator()
        batch_report = report_gen.generate_batch_markdown_report(scenarios, results)
        print_colored("\n📄 Batch report generated:", Fore.GREEN)
        print(f"  - MARKDOWN: {batch_report}")


def interactive_shell(dependency_manager: DependencyManager):
    """Interactive CLI shell for demos"""
    engine = SimulationEngine(dependency_manager)
    failed_services = []
    reports_enabled = True
    ascii_graph = True
    last_html_report = None

    print_colored("\n🧭 Interactive Mode", Fore.CYAN, bright=True)
    print("Type 'help' to see available commands. Type 'quit' to exit.\n")

    while True:
        try:
            command = input("nexdex> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n")
            break
        
        if not command:
            continue
        
        if command in ["quit", "exit"]:
            break
        
        if command == "help":
            print("\nCommands:")
            print("  list                         - list services")
            print("  fail <svc1,svc2,...>         - set failed services")
            print("  importance <Process=Score>   - override process importance")
            print("  preview                      - run simulation with ASCII graph, no reports")
            print("  run                          - run simulation (reports on/off)")
            print("  reports on|off               - toggle report generation")
            print("  ascii on|off                 - toggle ASCII graph output")
            print("  scenarios                    - list saved scenarios")
            print("  load <scenario>              - load and run a saved scenario")
            print("  open                         - open last HTML report in browser")
            print("  quit                         - exit interactive mode\n")
            continue
        
        if command == "list":
            list_services(dependency_manager)
            continue
        
        if command.startswith("fail "):
            services_str = command[len("fail "):].strip()
            failed_services = [s.strip() for s in services_str.split(",") if s.strip()]
            print_colored(f"Failed services set to: {', '.join(failed_services)}", Fore.CYAN)
            continue
        
        if command.startswith("importance "):
            overrides_str = command[len("importance "):].strip()
            overrides = overrides_str.split()
            try:
                apply_process_importance_overrides(dependency_manager, overrides)
                print_colored("✅ Process importance updated", Fore.GREEN)
            except ValueError as e:
                print_colored(f"❌ {e}", Fore.RED)
            continue
        
        if command == "preview":
            if not failed_services:
                print_colored("Set failed services first using: fail <svc1,svc2>", Fore.YELLOW)
                continue
            result = engine.simulate_failure(failed_services)
            print_ascii_graph(dependency_manager, failed_services, result)
            continue
        
        if command == "run":
            if not failed_services:
                print_colored("Set failed services first using: fail <svc1,svc2>", Fore.YELLOW)
                continue
            reports = run_simulation(
                dependency_manager,
                failed_services,
                generate_reports=reports_enabled,
                show_ascii_graph=ascii_graph
            )
            if reports and reports.get("html"):
                last_html_report = reports["html"]
            continue
        
        if command.startswith("reports "):
            value = command[len("reports "):].strip().lower()
            reports_enabled = value == "on"
            print_colored(f"Reports {'enabled' if reports_enabled else 'disabled'}", Fore.CYAN)
            continue
        
        if command.startswith("ascii "):
            value = command[len("ascii "):].strip().lower()
            ascii_graph = value == "on"
            print_colored(f"ASCII graph {'enabled' if ascii_graph else 'disabled'}", Fore.CYAN)
            continue
        
        if command == "scenarios":
            list_scenarios()
            continue
        
        if command.startswith("load "):
            name = command[len("load "):].strip()
            try:
                scenario = load_scenario_from_file(name)
                reports = run_simulation(
                    dependency_manager,
                    scenario.failed_services,
                    generate_reports=reports_enabled,
                    show_ascii_graph=ascii_graph
                )
                if reports and reports.get("html"):
                    last_html_report = reports["html"]
            except FileNotFoundError as e:
                print_colored(f"❌ {e}", Fore.RED)
            continue

        if command == "open":
            if last_html_report:
                try:
                    webbrowser.open(last_html_report)
                    print_colored("🌐 Opened HTML report in your default browser", Fore.GREEN)
                except Exception as e:
                    print_colored(f"⚠️  Failed to open browser: {e}", Fore.YELLOW)
            else:
                print_colored("No HTML report available yet. Run a simulation first.", Fore.YELLOW)
            continue
        
        print_colored("Unknown command. Type 'help' for options.", Fore.YELLOW)


def apply_process_importance_overrides(
    dependency_manager: DependencyManager,
    overrides: List[str]
):
    """Apply process importance overrides from CLI"""
    for item in overrides:
        if "=" not in item:
            raise ValueError(f"Invalid format '{item}'. Use Process=Score")
        process_name, score_str = item.split("=", 1)
        process_name = process_name.strip()
        if not process_name:
            raise ValueError(f"Invalid process name in '{item}'")
        try:
            score = int(score_str)
        except ValueError:
            raise ValueError(f"Invalid score '{score_str}' in '{item}'")
        score = max(1, min(10, score))
        dependency_manager.set_process_importance(process_name, score)


def print_ascii_graph(
    dependency_manager: DependencyManager,
    failed_services: List[str],
    result
):
    """Print a simple ASCII dependency view with statuses"""
    try:
        import networkx as nx
    except Exception:
        print_colored("\n⚠️  ASCII graph requires networkx", Fore.YELLOW)
        return

    failed_set = set(failed_services)
    affected_set = {i.service.name for i in result.impacts if not i.is_direct_failure}
    graph = dependency_manager.graph

    try:
        ordered = list(nx.topological_sort(graph))
    except Exception:
        ordered = sorted(graph.nodes())

    print_colored("\n🧭 ASCII Dependency View (Impact Propagation):\n", Fore.CYAN, bright=True)
    for service_name in ordered:
        if service_name in failed_set:
            status = "🔴 FAILED"
            color = Fore.RED
        elif service_name in affected_set:
            status = "🟡 AFFECTED"
            color = Fore.YELLOW
        else:
            status = "🟢 OK"
            color = Fore.GREEN
        deps = dependency_manager.get_dependencies(service_name)
        dep_str = " ← ".join(deps) if deps else "(root)"
        print_colored(f"  {status} {service_name:20} {dep_str}", color)


def compare_scenarios(
    dependency_manager: DependencyManager,
    scenario_name1: str,
    scenario_name2: str,
    open_report: bool = False
):
    """Load and compare two scenarios, generate comparison reports"""
    try:
        scenario1 = load_scenario_from_file(scenario_name1)
        scenario2 = load_scenario_from_file(scenario_name2)
    except FileNotFoundError as e:
        print_colored(f"❌ {e}", Fore.RED)
        return
    
    print_colored(f"\n📊 Comparing: {scenario1.name} vs {scenario2.name}", Fore.CYAN, bright=True)
    print(f"  Scenario 1: {', '.join(scenario1.failed_services)}")
    print(f"  Scenario 2: {', '.join(scenario2.failed_services)}\n")
    
    # Run simulations
    engine = SimulationEngine(dependency_manager)
    
    try:
        result1 = engine.simulate_failure(scenario1.failed_services, peak_hours=scenario1.peak_hours)
        result2 = engine.simulate_failure(scenario2.failed_services, peak_hours=scenario2.peak_hours)
    except Exception as e:
        print_colored(f"❌ Simulation error: {e}", Fore.RED)
        return
    
    # Get comparison data
    comparison = engine.compare_results(result1, result2)
    
    # Display comparison summary
    print_colored("━" * 80, Fore.CYAN)
    print_colored("COMPARISON SUMMARY", Fore.CYAN, bright=True)
    print_colored("━" * 80, Fore.CYAN)
    
    table_data = [
        ["Metric", scenario1.name, scenario2.name, "Difference"],
        ["─" * 20, "─" * 20, "─" * 20, "─" * 20],
        [
            "Total Impact Score",
            f"{comparison['summary1']['total_impact_score']:.2f}",
            f"{comparison['summary2']['total_impact_score']:.2f}",
            f"{comparison['impact_diff']:+.2f} ({comparison['impact_pct_diff']:+.1f}%)"
        ],
        [
            "Services Affected",
            str(comparison['summary1']['total_services_affected']),
            str(comparison['summary2']['total_services_affected']),
            f"{comparison['services_diff']:+d}"
        ],
        [
            "Business Processes",
            str(comparison['summary1']['business_processes_affected']),
            str(comparison['summary2']['business_processes_affected']),
            f"{comparison['summary2']['business_processes_affected'] - comparison['summary1']['business_processes_affected']:+d}"
        ],
        [
            "Cascade Failures",
            str(comparison['summary1']['cascade_failures']),
            str(comparison['summary2']['cascade_failures']),
            f"{comparison['summary2']['cascade_failures'] - comparison['summary1']['cascade_failures']:+d}"
        ],
    ]
    
    print(tabulate(table_data, tablefmt="plain"))
    print()
    
    # Highlight worse scenario
    worse_label = "Scenario 2" if comparison["worse_scenario"] == result2 else "Scenario 1"
    worse_impact = max(result1.total_impact_score, result2.total_impact_score)
    better_impact = min(result1.total_impact_score, result2.total_impact_score)
    
    print_colored(f"\n⚠️  {worse_label} is MORE SEVERE", Fore.RED, bright=True)
    print_colored(
        f"   Impact difference: {abs(comparison['impact_diff']):.2f} points "
        f"({abs(comparison['impact_pct_diff']):.1f}%)",
        Fore.YELLOW
    )
    
    # Unique services
    if comparison["unique_to_first"] or comparison["unique_to_second"]:
        print_colored("\n🔍 Unique Services Affected:", Fore.CYAN, bright=True)
        if comparison["unique_to_first"]:
            print_colored(f"  Only in {scenario1.name}:", Fore.YELLOW)
            for svc in sorted(comparison["unique_to_first"]):
                print(f"    - {svc}")
        if comparison["unique_to_second"]:
            print_colored(f"  Only in {scenario2.name}:", Fore.YELLOW)
            for svc in sorted(comparison["unique_to_second"]):
                print(f"    - {svc}")
    
    # Generate reports
    print_colored("\n📄 Generating comparison reports...", Fore.CYAN)
    report_generator = ReportGenerator()
    
    markdown_report = report_generator.generate_comparison_markdown_report(comparison)
    html_report = report_generator.generate_comparison_html_report(comparison, dependency_manager)
    
    print_colored(f"✅ Markdown report: {markdown_report}", Fore.GREEN)
    print_colored(f"✅ HTML report: {html_report}", Fore.GREEN)
    
    if open_report:
        webbrowser.open(f"file://{Path(html_report).resolve()}")
        print_colored("🌐 Opened HTML report in browser", Fore.CYAN)


def main():
    parser = argparse.ArgumentParser(
        description="NexDex - Cross-System Business Impact Simulator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python nexdex.py --list
  python nexdex.py --fail Database
  python nexdex.py --fail Database WebApp
  python nexdex.py --fail Database --save critical_db_failure
  python nexdex.py --load critical_db_failure
  python nexdex.py --config custom.json --fail API
        """
    )
    
    parser.add_argument(
        "--config",
        default="config/services.json",
        help="Path to services configuration file (default: config/services.json)"
    )
    
    parser.add_argument(
        "--fail",
        nargs="+",
        metavar="SERVICE",
        help="Service(s) to simulate as failed"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all configured services"
    )
    
    parser.add_argument(
        "--scenarios",
        action="store_true",
        help="List all saved scenarios"
    )
    
    parser.add_argument(
        "--save",
        metavar="NAME",
        help="Save simulation as a scenario"
    )
    
    parser.add_argument(
        "--load",
        metavar="NAME",
        help="Load and run a saved scenario"
    )
    
    parser.add_argument(
        "--no-reports",
        action="store_true",
        help="Skip report generation"
    )

    parser.add_argument(
        "--ascii-graph",
        action="store_true",
        help="Show ASCII dependency view in CLI"
    )

    parser.add_argument(
        "--set-process-importance",
        nargs="+",
        metavar="PROCESS=SCORE",
        help="Override business process importance (e.g., Billing=10 Sales=8)"
    )

    parser.add_argument(
        "--batch",
        nargs="+",
        metavar="PATH",
        help="Run multiple scenarios (supports globs like scenarios/*.json)"
    )

    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Start interactive CLI mode"
    )

    parser.add_argument(
        "--open-report",
        action="store_true",
        help="Open HTML report in default web browser"
    )

    parser.add_argument(
        "--filter-tags",
        metavar="TAG",
        help="Filter scenarios by tag (use with --scenarios)"
    )

    parser.add_argument(
        "--compare",
        nargs=2,
        metavar=("SCENARIO1", "SCENARIO2"),
        help="Compare two scenarios side-by-side (e.g., --compare scenario1 scenario2)"
    )
    
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate configuration file"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="NexDex v1.0.0"
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Load configuration
    try:
        dependency_manager = DependencyManager()
        dependency_manager.load_from_json(args.config)
        print_colored(f"✅ Loaded configuration from: {args.config}", Fore.GREEN)
    except FileNotFoundError:
        print_colored(f"❌ Configuration file not found: {args.config}", Fore.RED)
        print_colored("Create a configuration file or use --config to specify a different file.", Fore.YELLOW)
        sys.exit(1)
    except Exception as e:
        print_colored(f"❌ Error loading configuration: {e}", Fore.RED)
        sys.exit(1)
    
    # Apply process importance overrides
    if args.set_process_importance:
        try:
            apply_process_importance_overrides(dependency_manager, args.set_process_importance)
            print_colored("✅ Applied process importance overrides", Fore.GREEN)
        except ValueError as e:
            print_colored(f"❌ {e}", Fore.RED)
            sys.exit(1)

    # Handle commands
    if args.validate:
        validate_config(dependency_manager)
    elif args.interactive:
        interactive_shell(dependency_manager)
    elif args.list:
        list_services(dependency_manager)
    elif args.scenarios:
        list_scenarios(filter_tag=args.filter_tags)
    elif args.batch:
        run_batch_scenarios(
            dependency_manager,
            args.batch,
            generate_reports=not args.no_reports,
            open_report=args.open_report
        )
    elif args.load:
        try:
            scenario = load_scenario_from_file(args.load)
            print_colored(f"\n📁 Loading scenario: {scenario.name}", Fore.CYAN)
            print(f"Description: {scenario.description}")
            run_simulation(
                dependency_manager,
                scenario.failed_services,
                generate_reports=not args.no_reports,
                show_ascii_graph=args.ascii_graph,
                open_report=args.open_report,
                peak_hours=scenario.peak_hours
            )
        except FileNotFoundError as e:
            print_colored(f"❌ {e}", Fore.RED)
            print_colored("Use --scenarios to list available scenarios.", Fore.YELLOW)
            sys.exit(1)
    elif args.compare:
        compare_scenarios(
            dependency_manager,
            args.compare[0],
            args.compare[1],
            open_report=args.open_report
        )
    elif args.fail:
        run_simulation(
            dependency_manager,
            args.fail,
            generate_reports=not args.no_reports,
            save_scenario=args.save,
            show_ascii_graph=args.ascii_graph,
            open_report=args.open_report
        )
    else:
        parser.print_help()
        print_colored("\n💡 Tip: Start with --list to see your configured services", Fore.CYAN)


if __name__ == "__main__":
    main()
