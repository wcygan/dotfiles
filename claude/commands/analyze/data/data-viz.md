---
allowed-tools: Read, Write, Task, Bash(fd:*), Bash(rg:*), Bash(jq:*), Bash(gdate:*)
description: Generate interactive data visualizations and dashboards with intelligent chart selection
---

# /data-viz

## Context

- Session ID: !`gdate +%s%N`
- Current directory: !`pwd`
- Data files: !`fd "\.(csv|json|xlsx|parquet|tsv|xml)$" --max-depth 3 | head -10 || echo "No data files found"`
- Database configs: !`fd "(knex|prisma|typeorm|sequelize|deno\.json|package\.json)" --max-depth 2 | head -5 || echo "No database configs found"`
- API endpoints: !`rg "/(api|data|metrics|analytics)/" --type js --type ts --type go --type rust | head -10 || echo "No API endpoints found"`
- Technology stack: !`fd "(deno\.json|package\.json|Cargo\.toml|go\.mod)" --max-depth 2 | head -5 || echo "No framework files detected"`
- Existing dashboards: !`rg "(dashboard|chart|visualization|d3|chartjs)" --type js --type ts | head -5 || echo "No existing dashboards found"`
- Analytics tools: !`fd "(grafana|kibana|metabase|analytics)" --type d | head -5 || echo "No analytics tools found"`

## Your Task

STEP 1: Data Discovery and Analysis

IF $ARGUMENTS provided:

- Analyze specified data source (file, URL, or description)
- Skip discovery phase and proceed to analysis
  ELSE:
- Use parallel sub-agents for comprehensive data discovery:
  - **File Data Agent**: Analyze CSV, JSON, Excel files in project
  - **API Data Agent**: Discover data endpoints and test schemas
  - **Database Agent**: Detect database configs and analyze schemas
  - **Analytics Agent**: Find existing dashboards and analytics tools

STEP 2: Chart Recommendation and Framework Selection

- Think deeply about optimal visualization approaches for discovered data
- Analyze data types: numerical, categorical, temporal, boolean
- Recommend chart types: line, bar, scatter, pie, histogram, heatmap
- Select framework based on project tech stack:
  - Fresh/Deno: D3.js + Custom components
  - React/Next.js: Chart.js + Recharts
  - Vue/Nuxt: Chart.js + Vue-ChartJS
  - Static site: Chart.js + vanilla JavaScript

STEP 3: Dashboard Generation

- Create interactive dashboard layout with responsive grid
- Generate chart components with:
  - Real-time data updates
  - Interactive tooltips and zoom
  - Export functionality
  - Mobile-responsive design
- Implement data transformation pipelines
- Add filtering and time range controls

STEP 4: State Management and Session Tracking

- Create session state file: /tmp/data-viz-$SESSION_ID.json
- Track dashboard configuration and chart definitions
- Save data source mappings and transformation rules
- Implement checkpoint system for complex dashboard builds

STEP 5: Deployment and Integration

- Generate deployment-ready dashboard code
- Create CI/CD configuration for automated updates
- Setup real-time data refresh mechanisms
- Add monitoring and analytics for dashboard usage

TRY:

- Execute comprehensive dashboard generation workflow
- Validate all chart components and data integrations
- Test responsive design and cross-browser compatibility
- Save checkpoint: dashboard_generation_complete

CATCH (missing_data_sources):

- Provide sample data generators and mock APIs
- Create placeholder visualizations with realistic data
- Document data requirements and integration steps
- Save fallback state with alternative data sources

CATCH (framework_compatibility_issues):

- Implement framework-agnostic vanilla JavaScript solution
- Provide multiple framework implementations
- Document compatibility requirements and alternatives
- Use Chart.js as universal fallback option

CATCH (complex_data_analysis_required):

- Use extended thinking for deep data analysis
- Break down complex datasets into manageable visualizations
- Implement progressive data loading and aggregation
- Create summary views with drill-down capabilities

FINALLY:

- Update session state: /tmp/data-viz-$SESSION_ID.json
- Generate comprehensive dashboard documentation
- Clean up temporary analysis files
- Create deployment and maintenance guides
