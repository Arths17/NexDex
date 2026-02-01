# NexDex - Cross-System Business Impact Simulator

A local MVP tool for simulating failures of services and analyzing their business impact.

## Overview

NexDex helps you understand the business impact of service failures by:
- Mapping service dependencies
- Simulating failure scenarios
- Calculating impact scores
- Generating detailed reports

## Installation

1. Ensure you have Python 3.10+ installed
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Define Your Services

Edit `config/services.json` to define your services, dependencies, and business processes:

```json
{
  "business_processes": {
    "Core Data Platform": 10,
    "Customer Experience": 9
  },
  "services": [
    {
      "name": "Database",
      "depends_on": [],
      "business_process": "Core Data Platform",
      "importance": 10,
      "mttr": 20
    },
    {
      "name": "WebApp",
      "depends_on": ["Database"],
      "business_process": "Customer Experience",
      "importance": 9,
      "mttr": 15
    }
  ]
}
```

### 2. Run a Simulation

Simulate a single service failure:
```bash
python nexdex.py --fail Database
```

Simulate multiple failures:
```bash
python nexdex.py --fail Database WebApp
```

### 3. View Results

Reports are automatically generated in the `reports/` directory:
- Markdown report: `reports/impact_report_<timestamp>.md`
- HTML report: `reports/impact_report_<timestamp>.html`
- Visualization: `reports/impact_report_<timestamp>.png`

## CLI Commands

### Simulate Failures
```bash
python nexdex.py --fail <service_name> [<service_name> ...]
```

### List Services
```bash
python nexdex.py --list
```

### Save Scenario
```bash
python nexdex.py --fail Database --save my_scenario
```

### Load and Run Scenario
```bash
python nexdex.py --load my_scenario
```

### Skip Reports
```bash
python nexdex.py --fail Database --no-reports
```

### Show ASCII Dependency View (Colored Status)
```bash
python nexdex.py --fail Database --ascii-graph
```

Shows colored ASCII graph with:
- 🔴 **FAILED** (red) - Directly failed services
- 🟡 **AFFECTED** (yellow) - Cascade-impacted services  
- 🟢 **OK** (green) - Unaffected services

### List Scenarios
```bash
python nexdex.py --scenarios
```

### Filter Scenarios by Tags
```bash
python nexdex.py --scenarios --filter-tags peak-hours
```

Scenarios can have tags like: `peak-hours`, `database`, `critical`, `revenue-impact`

### Open HTML Report in Browser
```bash
python nexdex.py --fail Database --open-report
```

### Override Business Process Importance
```bash
python nexdex.py --fail Database --set-process-importance "Core Data Platform=10" "Customer Experience=9"
```

### Interactive Mode
```bash
python nexdex.py --interactive
```

### Batch Simulation
```bash
python nexdex.py --batch scenarios/*.json
```

### Demo: Peak Hours Database Outage
```bash
python nexdex.py --load peak_hours_db_outage
```


### Custom Config
```bash
python nexdex.py --config custom_config.json --fail Database
```

## Configuration Format

### Service Definition

- **name**: Unique service identifier
- **depends_on**: List of services this service depends on
- **business_process**: Business process impacted by this service
- **importance**: Business importance score (1-10, default: 5)
- **mttr**: Mean Time To Repair in minutes (default: 30)

### Scenario Format with Tags

```json
{
  "name": "peak_hours_db_outage",
  "description": "Database outage during peak hours",
  "failed_services": ["Database"],
  "tags": ["peak-hours", "database", "critical", "revenue-impact"],
  "created_at": "2026-02-01T13:45:00"
}
```

**Tags** help organize and filter scenarios. Use `--filter-tags` to quickly find related scenarios.

### Business Process Importance

You can define shared business process importance scores in the config, and override them at runtime:

```json
"business_processes": {
  "Core Data Platform": 10,
  "Customer Experience": 9
}
```

### Example Configuration

```json
{
  "services": [
    {
      "name": "PostgresDB",
      "depends_on": [],
      "business_process": "Data Storage",
      "importance": 10,
      "mttr": 15
    },
    {
      "name": "Redis",
      "depends_on": [],
      "business_process": "Caching",
      "importance": 6,
      "mttr": 5
    },
    {
      "name": "API_Gateway",
      "depends_on": ["PostgresDB", "Redis"],
      "business_process": "API Services",
      "importance": 9,
      "mttr": 10
    },
    {
      "name": "WebFrontend",
      "depends_on": ["API_Gateway"],
      "business_process": "Customer Interface",
      "importance": 8,
      "mttr": 20
    }
  ]
}
```

## Impact Score Calculation

Impact Score = MTTR × Importance × Cascade Factor

Where:
- **MTTR**: Mean Time To Repair (minutes)
- **Importance**: Business process importance (if defined) or service importance
- **Cascade Factor**: Multiplier based on number of dependent services

## Project Structure

```
NexDex/
├── nexdex.py              # Main CLI entry point
├── config/
│   └── services.json      # Service definitions
├── src/
│   ├── models.py          # Data models
│   ├── dependency_manager.py  # Dependency graph logic
│   ├── simulation_engine.py   # Simulation logic
│   └── report_generator.py    # Report generation
├── reports/               # Generated reports
├── scenarios/             # Saved scenarios
├── requirements.txt       # Dependencies
└── README.md             # This file
```

## Future Enhancements

- Real-time monitoring integration
- SaaS dashboard
- Slack/Teams notifications
- Historical failure data analysis
- Machine learning-based impact predictions
- Multi-cloud support

## Potential Next Local Enhancements

- Color-coded ASCII graphs for easier visualization
- Batch simulation of multiple scenarios in one run
- Summary table in reports with top 5 impacted business processes
- Optional: save impact reports to a timestamped folder per scenario

## License

MIT License - Free for personal and commercial use
