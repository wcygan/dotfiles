# /data-viz

Generate interactive data visualizations and dashboards for $ARGUMENT with intelligent chart selection, real-time updates, and deployment-ready interfaces.

## Usage

```
/data-viz [data-source]
/data-viz [csv-file]
/data-viz [api-endpoint]
/data-viz
```

## Context Detection

**When no argument provided:**

- Scans project for data sources (CSV, JSON, databases)
- Detects API endpoints returning data
- Analyzes existing monitoring/metrics systems
- Provides interactive data source selection

**When data source provided:**

- Analyzes data structure and types
- Suggests appropriate visualization types
- Creates responsive dashboard layouts
- Configures real-time data updates

**When file provided:**

- Parses CSV, JSON, or Excel files
- Infers data relationships and patterns
- Generates static and interactive visualizations
- Creates data exploration interfaces

## Data Source Detection

**File-based Data Sources:**

```bash
# Detect data files
fd "\.(csv|json|xlsx|parquet|tsv)$" --max-depth 3

# Analyze database connections
rg "(DATABASE_URL|POSTGRES|MYSQL|MONGODB)" --type env
fd "(knex|prisma|typeorm|sequelize).(js|ts|config)" --max-depth 2

# Check for existing analytics
rg "(analytics|metrics|dashboard)" --type js --type ts --type py
fd "(grafana|kibana|metabase)" --type d
```

**API Data Sources:**

```bash
# Detect API endpoints with data
rg "/(api|data|metrics|analytics)/" --type js --type ts --type go --type rust -A 2

# Check for time-series data
rg "(timestamp|created_at|time|date)" --type js --type ts --type sql

# Identify metrics endpoints
rg "/(metrics|stats|analytics|dashboard)" --type js --type ts -A 3
```

## Visualization Generation Strategies

### 1. Data Analysis and Chart Recommendation

**Automatic Chart Type Selection:**

```typescript
// Intelligent chart type recommendation engine
interface DataColumn {
  name: string;
  type: "categorical" | "numerical" | "temporal" | "boolean";
  unique_values: number;
  sample_values: any[];
  null_percentage: number;
}

interface ChartRecommendation {
  type: string;
  priority: number;
  columns: string[];
  description: string;
  use_case: string;
}

class ChartRecommendationEngine {
  analyzeData(data: any[]): DataColumn[] {
    if (!data.length) return [];

    const columns: DataColumn[] = [];
    const keys = Object.keys(data[0]);

    for (const key of keys) {
      const values = data.map((row) => row[key]).filter((v) => v != null);
      const unique_values = new Set(values).size;
      const sample_values = values.slice(0, 5);

      let type: DataColumn["type"] = "categorical";

      // Type inference
      if (values.every((v) => typeof v === "number")) {
        type = "numerical";
      } else if (values.every((v) => !isNaN(Date.parse(v)))) {
        type = "temporal";
      } else if (values.every((v) => typeof v === "boolean")) {
        type = "boolean";
      }

      columns.push({
        name: key,
        type,
        unique_values,
        sample_values,
        null_percentage: (data.length - values.length) / data.length,
      });
    }

    return columns;
  }

  recommendCharts(columns: DataColumn[]): ChartRecommendation[] {
    const recommendations: ChartRecommendation[] = [];

    const numerical = columns.filter((c) => c.type === "numerical");
    const categorical = columns.filter((c) => c.type === "categorical");
    const temporal = columns.filter((c) => c.type === "temporal");

    // Time series recommendations
    if (temporal.length > 0 && numerical.length > 0) {
      recommendations.push({
        type: "line",
        priority: 10,
        columns: [temporal[0].name, numerical[0].name],
        description: "Line chart showing trends over time",
        use_case: "Time series analysis, trend visualization",
      });
    }

    // Distribution recommendations
    if (numerical.length >= 1) {
      recommendations.push({
        type: "histogram",
        priority: 8,
        columns: [numerical[0].name],
        description: "Histogram showing data distribution",
        use_case: "Understanding data distribution and outliers",
      });
    }

    // Comparison recommendations
    if (categorical.length > 0 && numerical.length > 0) {
      if (categorical[0].unique_values <= 10) {
        recommendations.push({
          type: "bar",
          priority: 9,
          columns: [categorical[0].name, numerical[0].name],
          description: "Bar chart comparing categories",
          use_case: "Comparing values across categories",
        });
      }
    }

    // Correlation recommendations
    if (numerical.length >= 2) {
      recommendations.push({
        type: "scatter",
        priority: 7,
        columns: [numerical[0].name, numerical[1].name],
        description: "Scatter plot showing correlation",
        use_case: "Exploring relationships between variables",
      });
    }

    // Composition recommendations
    if (categorical.length > 0 && numerical.length > 0) {
      if (categorical[0].unique_values <= 8) {
        recommendations.push({
          type: "pie",
          priority: 6,
          columns: [categorical[0].name, numerical[0].name],
          description: "Pie chart showing composition",
          use_case: "Understanding proportional relationships",
        });
      }
    }

    return recommendations.sort((a, b) => b.priority - a.priority);
  }
}
```

### 2. D3.js Interactive Visualizations

**Responsive Line Chart with Real-time Updates:**

```typescript
// Generated D3.js visualization component
import * as d3 from "d3";

interface DataPoint {
  timestamp: Date;
  value: number;
  category?: string;
}

class InteractiveLineChart {
  private svg: d3.Selection<SVGGElement, unknown, HTMLElement, any>;
  private width: number;
  private height: number;
  private margin = { top: 20, right: 80, bottom: 30, left: 50 };
  private xScale: d3.ScaleTime<number, number>;
  private yScale: d3.ScaleLinear<number, number>;
  private line: d3.Line<DataPoint>;
  private data: DataPoint[] = [];

  constructor(container: string, width: number = 800, height: number = 400) {
    this.width = width - this.margin.left - this.margin.right;
    this.height = height - this.margin.top - this.margin.bottom;

    this.svg = d3.select(container)
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .attr("transform", `translate(${this.margin.left},${this.margin.top})`);

    this.initializeScales();
    this.initializeAxes();
    this.initializeInteractions();
  }

  private initializeScales(): void {
    this.xScale = d3.scaleTime()
      .range([0, this.width]);

    this.yScale = d3.scaleLinear()
      .range([this.height, 0]);

    this.line = d3.line<DataPoint>()
      .x((d) => this.xScale(d.timestamp))
      .y((d) => this.yScale(d.value))
      .curve(d3.curveMonotoneX);
  }

  private initializeAxes(): void {
    // X-axis
    this.svg.append("g")
      .attr("class", "x-axis")
      .attr("transform", `translate(0,${this.height})`);

    // Y-axis
    this.svg.append("g")
      .attr("class", "y-axis");

    // Grid lines
    this.svg.append("g")
      .attr("class", "grid")
      .attr("transform", `translate(0,${this.height})`)
      .style("stroke-dasharray", "3,3")
      .style("opacity", 0.3);

    this.svg.append("g")
      .attr("class", "grid")
      .style("stroke-dasharray", "3,3")
      .style("opacity", 0.3);
  }

  private initializeInteractions(): void {
    // Tooltip
    const tooltip = d3.select("body")
      .append("div")
      .attr("class", "tooltip")
      .style("opacity", 0)
      .style("position", "absolute")
      .style("background", "rgba(0, 0, 0, 0.8)")
      .style("color", "white")
      .style("padding", "8px")
      .style("border-radius", "4px")
      .style("font-size", "12px");

    // Zoom behavior
    const zoom = d3.zoom<SVGGElement, unknown>()
      .scaleExtent([1, 10])
      .on("zoom", (event) => {
        const newXScale = event.transform.rescaleX(this.xScale);
        this.updateChart(this.data, newXScale);
      });

    this.svg.call(zoom);

    // Brush for selection
    const brush = d3.brushX()
      .extent([[0, 0], [this.width, this.height]])
      .on("end", (event) => {
        if (event.selection) {
          const [x0, x1] = event.selection.map(this.xScale.invert);
          this.filterData(x0, x1);
        }
      });

    this.svg.append("g")
      .attr("class", "brush")
      .call(brush);
  }

  updateData(newData: DataPoint[]): void {
    this.data = newData;

    // Update scales
    this.xScale.domain(d3.extent(newData, (d) => d.timestamp) as [Date, Date]);
    this.yScale.domain(d3.extent(newData, (d) => d.value) as [number, number]);

    this.updateChart(newData);
  }

  private updateChart(data: DataPoint[], customXScale?: d3.ScaleTime<number, number>): void {
    const xScale = customXScale || this.xScale;

    // Update axes
    this.svg.select(".x-axis")
      .transition()
      .duration(750)
      .call(d3.axisBottom(xScale).tickFormat(d3.timeFormat("%H:%M")));

    this.svg.select(".y-axis")
      .transition()
      .duration(750)
      .call(d3.axisLeft(this.yScale));

    // Update grid
    this.svg.select(".grid")
      .selectAll("line")
      .data(xScale.ticks())
      .join("line")
      .attr("x1", (d) => xScale(d))
      .attr("x2", (d) => xScale(d))
      .attr("y1", 0)
      .attr("y2", -this.height);

    // Update line
    const path = this.svg.selectAll(".line")
      .data([data]);

    path.enter()
      .append("path")
      .attr("class", "line")
      .style("fill", "none")
      .style("stroke", "#007bff")
      .style("stroke-width", 2)
      .merge(path)
      .transition()
      .duration(750)
      .attr("d", this.line);

    // Update data points
    const circles = this.svg.selectAll(".dot")
      .data(data);

    circles.enter()
      .append("circle")
      .attr("class", "dot")
      .style("fill", "#007bff")
      .merge(circles)
      .transition()
      .duration(750)
      .attr("cx", (d) => xScale(d.timestamp))
      .attr("cy", (d) => this.yScale(d.value))
      .attr("r", 3);

    circles.exit().remove();
  }

  private filterData(startDate: Date, endDate: Date): void {
    const filteredData = this.data.filter(
      (d) => d.timestamp >= startDate && d.timestamp <= endDate,
    );
    this.updateChart(filteredData);
  }

  // Real-time data updates
  startRealTimeUpdates(endpoint: string, interval: number = 5000): void {
    setInterval(async () => {
      try {
        const response = await fetch(endpoint);
        const newData = await response.json();
        this.updateData(newData);
      } catch (error) {
        console.error("Failed to fetch real-time data:", error);
      }
    }, interval);
  }
}

// Usage example
const chart = new InteractiveLineChart("#chart-container");
chart.updateData(initialData);
chart.startRealTimeUpdates("/api/metrics/realtime");
```

### 3. Chart.js Dashboard Components

**Multi-Chart Dashboard:**

```typescript
// Generated Chart.js dashboard
import {
  ArcElement,
  BarController,
  BarElement,
  CategoryScale,
  Chart,
  ChartConfiguration,
  DoughnutController,
  Legend,
  LinearScale,
  LineController,
  LineElement,
  PointElement,
  TimeScale,
  Title,
  Tooltip,
} from "chart.js";
import "chartjs-adapter-date-fns";

Chart.register(
  LineController,
  BarController,
  DoughnutController,
  LineElement,
  BarElement,
  ArcElement,
  CategoryScale,
  LinearScale,
  TimeScale,
  PointElement,
  Tooltip,
  Legend,
  Title,
);

interface DashboardConfig {
  container: string;
  title: string;
  refreshInterval?: number;
  charts: ChartConfig[];
}

interface ChartConfig {
  id: string;
  type: "line" | "bar" | "doughnut" | "scatter";
  title: string;
  dataSource: string;
  width?: string;
  height?: string;
  options?: any;
}

class DataVisualizationDashboard {
  private charts: Map<string, Chart> = new Map();
  private config: DashboardConfig;
  private refreshTimer?: number;

  constructor(config: DashboardConfig) {
    this.config = config;
    this.initializeDashboard();

    if (config.refreshInterval) {
      this.startAutoRefresh();
    }
  }

  private initializeDashboard(): void {
    const container = document.querySelector(this.config.container);
    if (!container) return;

    // Create dashboard layout
    container.innerHTML = `
      <div class="dashboard-header">
        <h1>${this.config.title}</h1>
        <div class="dashboard-controls">
          <button id="refresh-btn">Refresh</button>
          <button id="export-btn">Export</button>
          <select id="time-range">
            <option value="1h">Last Hour</option>
            <option value="24h">Last 24 Hours</option>
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
          </select>
        </div>
      </div>
      <div class="dashboard-grid">
        ${
      this.config.charts.map((chart) => `
          <div class="chart-container" style="width: ${chart.width || "50%"}; height: ${
        chart.height || "400px"
      }">
            <h3>${chart.title}</h3>
            <canvas id="${chart.id}"></canvas>
          </div>
        `).join("")
    }
      </div>
    `;

    // Initialize charts
    this.config.charts.forEach((chartConfig) => {
      this.createChart(chartConfig);
    });

    // Add event listeners
    this.addEventListeners();
  }

  private createChart(config: ChartConfig): void {
    const canvas = document.getElementById(config.id) as HTMLCanvasElement;
    if (!canvas) return;

    const chartConfig: ChartConfiguration = {
      type: config.type,
      data: {
        labels: [],
        datasets: [],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: config.title,
          },
          legend: {
            display: true,
            position: "top",
          },
          tooltip: {
            mode: "index",
            intersect: false,
            callbacks: {
              title: (context) => {
                return context[0].label;
              },
              label: (context) => {
                return `${context.dataset.label}: ${context.formattedValue}`;
              },
            },
          },
        },
        scales: this.getScaleConfig(config.type),
        ...config.options,
      },
    };

    const chart = new Chart(canvas, chartConfig);
    this.charts.set(config.id, chart);

    // Load initial data
    this.loadChartData(config.id, config.dataSource);
  }

  private getScaleConfig(type: string): any {
    switch (type) {
      case "line":
        return {
          x: {
            type: "time",
            time: {
              displayFormats: {
                minute: "HH:mm",
                hour: "HH:mm",
                day: "MMM dd",
              },
            },
          },
          y: {
            beginAtZero: true,
          },
        };
      case "bar":
        return {
          y: {
            beginAtZero: true,
          },
        };
      default:
        return {};
    }
  }

  private async loadChartData(chartId: string, dataSource: string): Promise<void> {
    try {
      const response = await fetch(dataSource);
      const data = await response.json();

      const chart = this.charts.get(chartId);
      if (!chart) return;

      // Transform data based on chart type
      const transformedData = this.transformDataForChart(data, chart.config.type);

      chart.data = transformedData;
      chart.update();
    } catch (error) {
      console.error(`Failed to load data for chart ${chartId}:`, error);
    }
  }

  private transformDataForChart(data: any[], chartType: string): any {
    switch (chartType) {
      case "line":
        return {
          labels: data.map((d) => new Date(d.timestamp)),
          datasets: [{
            label: "Value",
            data: data.map((d) => ({ x: new Date(d.timestamp), y: d.value })),
            borderColor: "rgb(75, 192, 192)",
            backgroundColor: "rgba(75, 192, 192, 0.1)",
            tension: 0.1,
          }],
        };

      case "bar":
        return {
          labels: data.map((d) => d.category),
          datasets: [{
            label: "Count",
            data: data.map((d) => d.count),
            backgroundColor: [
              "rgba(255, 99, 132, 0.8)",
              "rgba(54, 162, 235, 0.8)",
              "rgba(255, 205, 86, 0.8)",
              "rgba(75, 192, 192, 0.8)",
              "rgba(153, 102, 255, 0.8)",
            ],
          }],
        };

      case "doughnut":
        return {
          labels: data.map((d) => d.label),
          datasets: [{
            data: data.map((d) => d.value),
            backgroundColor: [
              "#FF6384",
              "#36A2EB",
              "#FFCE56",
              "#4BC0C0",
              "#9966FF",
              "#FF9F40",
            ],
          }],
        };

      default:
        return { labels: [], datasets: [] };
    }
  }

  private addEventListeners(): void {
    // Refresh button
    document.getElementById("refresh-btn")?.addEventListener("click", () => {
      this.refreshAllCharts();
    });

    // Export button
    document.getElementById("export-btn")?.addEventListener("click", () => {
      this.exportDashboard();
    });

    // Time range selector
    document.getElementById("time-range")?.addEventListener("change", (e) => {
      const target = e.target as HTMLSelectElement;
      this.updateTimeRange(target.value);
    });
  }

  private refreshAllCharts(): void {
    this.config.charts.forEach((chartConfig) => {
      this.loadChartData(chartConfig.id, chartConfig.dataSource);
    });
  }

  private updateTimeRange(range: string): void {
    // Update data sources with time range parameter
    this.config.charts.forEach((chartConfig) => {
      const dataSource = `${chartConfig.dataSource}?range=${range}`;
      this.loadChartData(chartConfig.id, dataSource);
    });
  }

  private exportDashboard(): void {
    const dashboardElement = document.querySelector(this.config.container);
    if (!dashboardElement) return;

    // Generate export data
    const exportData = {
      title: this.config.title,
      timestamp: new Date().toISOString(),
      charts: Array.from(this.charts.entries()).map(([id, chart]) => ({
        id,
        type: chart.config.type,
        data: chart.data,
      })),
    };

    // Download as JSON
    const blob = new Blob([JSON.stringify(exportData, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `dashboard-export-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }

  private startAutoRefresh(): void {
    this.refreshTimer = window.setInterval(() => {
      this.refreshAllCharts();
    }, this.config.refreshInterval);
  }

  destroy(): void {
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer);
    }

    this.charts.forEach((chart) => chart.destroy());
    this.charts.clear();
  }
}

// Example usage
const dashboard = new DataVisualizationDashboard({
  container: "#dashboard",
  title: "Application Metrics Dashboard",
  refreshInterval: 30000, // 30 seconds
  charts: [
    {
      id: "response-times",
      type: "line",
      title: "Response Times",
      dataSource: "/api/metrics/response-times",
      width: "50%",
      height: "300px",
    },
    {
      id: "error-rates",
      type: "bar",
      title: "Error Rates by Endpoint",
      dataSource: "/api/metrics/errors",
      width: "50%",
      height: "300px",
    },
    {
      id: "user-activity",
      type: "doughnut",
      title: "User Activity Distribution",
      dataSource: "/api/metrics/user-activity",
      width: "100%",
      height: "400px",
    },
  ],
});
```

### 4. Static Site Generation

**Generated Static Dashboard:**

```html
<!-- Generated static dashboard HTML -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Visualization Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
    <style>
      body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        margin: 0;
        padding: 20px;
        background: #f5f5f5;
      }

      .dashboard-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
        padding: 20px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      }

      .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
        gap: 20px;
      }

      .chart-container {
        background: white;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      }

      .chart-container h3 {
        margin: 0 0 20px 0;
        color: #333;
        font-size: 18px;
      }

      .controls {
        display: flex;
        gap: 10px;
        align-items: center;
      }

      button {
        padding: 8px 16px;
        border: none;
        border-radius: 4px;
        background: #007bff;
        color: white;
        cursor: pointer;
        font-size: 14px;
      }

      button:hover {
        background: #0056b3;
      }

      select {
        padding: 8px 12px;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-size: 14px;
      }

      .tooltip {
        position: absolute;
        background: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 8px 12px;
        border-radius: 4px;
        font-size: 12px;
        pointer-events: none;
        z-index: 1000;
      }

      .loading {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
        color: #666;
      }

      @media (max-width: 768px) {
        .dashboard-header {
          flex-direction: column;
          gap: 20px;
        }

        .dashboard-grid {
          grid-template-columns: 1fr;
        }
      }
    </style>
  </head>
  <body>
    <div id="dashboard">
      <div class="dashboard-header">
        <h1>Data Visualization Dashboard</h1>
        <div class="controls">
          <button id="refresh-btn">Refresh</button>
          <button id="export-btn">Export</button>
          <select id="time-range">
            <option value="1h">Last Hour</option>
            <option value="24h">Last 24 Hours</option>
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
          </select>
        </div>
      </div>

      <div class="dashboard-grid">
        <!-- Charts will be dynamically generated here -->
      </div>
    </div>

    <script>
      // Dashboard initialization and management code
      // (Generated TypeScript/JavaScript code goes here)
    </script>
  </body>
</html>
```

## Framework Integration

**Deno Fresh Dashboard Route:**

```typescript
// Generated Fresh route for dashboard
import { Handlers, PageProps } from "$fresh/server.ts";
import DashboardComponent from "../components/Dashboard.tsx";

interface DashboardData {
  metrics: any[];
  config: DashboardConfig;
}

export const handler: Handlers<DashboardData> = {
  async GET(req, ctx) {
    // Load dashboard configuration
    const config = await loadDashboardConfig();

    // Fetch initial metrics data
    const metrics = await Promise.all(
      config.charts.map((chart) => fetchChartData(chart.dataSource)),
    );

    return ctx.render({ metrics, config });
  },
};

export default function DashboardPage({ data }: PageProps<DashboardData>) {
  return (
    <div class="min-h-screen bg-gray-100">
      <DashboardComponent
        config={data.config}
        initialData={data.metrics}
      />
    </div>
  );
}
```

## CI/CD Integration

**Automated Dashboard Deployment:**

```yaml
# GitHub Actions for dashboard deployment
name: Deploy Data Visualization Dashboard

on:
  push:
    branches: [main]
    paths: ["data/**", "dashboards/**"]

jobs:
  build-dashboard:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Deno
        uses: denoland/setup-deno@v1
        with:
          deno-version: v1.x

      - name: Process data sources
        run: |
          deno run --allow-all scripts/process-data.ts

      - name: Generate visualizations
        run: |
          deno run --allow-all scripts/generate-charts.ts

      - name: Build static dashboard
        run: |
          deno run --allow-all scripts/build-dashboard.ts

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist

      - name: Update dashboard URL in README
        run: |
          echo "Dashboard: https://${{ github.repository_owner }}.github.io/${{ github.event.repository.name }}/" >> README.md
```

## Output

The command generates:

1. **Interactive Dashboards**: Responsive web interfaces with real-time updates
2. **Chart Components**: Reusable visualization components for various data types
3. **Data Processing**: Scripts for data analysis and transformation
4. **Static Sites**: Deployment-ready dashboard websites
5. **API Integration**: Real-time data fetching and updates
6. **Export Functionality**: Data and visualization export capabilities

## Integration with Other Commands

- Use with `/api-docs` for API endpoint visualization
- Combine with `/monitor` for system metrics dashboards
- Integrate with `/ci-gen` for automated dashboard deployment
- Follow with `/deploy` for production dashboard hosting
- Use with `/load-test` for performance metrics visualization

The data visualization system automatically detects data sources, recommends appropriate chart types, and generates production-ready dashboards with real-time updates and responsive design.
