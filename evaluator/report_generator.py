"""Report generator for creating markdown reports and visualization graphs."""

import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

from .benchmarks.base import BenchmarkResult


class ReportGenerator:
    """Generates markdown reports and visualization graphs."""
    
    def __init__(self, config: Dict[str, Any], run_id: str):
        self.config = config
        self.run_id = run_id
        self.reports_dir = config.get('output', {}).get('reports_dir', 'reports')
        self.generate_graphs = config.get('output', {}).get('generate_graphs', True)
        
        # Create output directories
        self.run_dir = os.path.join(self.reports_dir, run_id)
        self.graphs_dir = os.path.join(self.run_dir, 'graphs')
        os.makedirs(self.run_dir, exist_ok=True)
        os.makedirs(self.graphs_dir, exist_ok=True)
    
    def generate(self, results: List[BenchmarkResult]) -> str:
        """Generate full report with markdown and graphs."""
        if not results:
            return "No results to report"
        
        # Generate markdown report
        report_path = self._generate_markdown(results)
        
        # Generate graphs
        if self.generate_graphs:
            self._generate_graphs(results)
        
        return report_path
    
    def _generate_markdown(self, results: List[BenchmarkResult]) -> str:
        """Generate markdown report."""
        report_path = os.path.join(self.run_dir, 'report.md')
        
        # Organize results by model
        results_by_model = defaultdict(list)
        for result in results:
            results_by_model[result.model_id].append(result)
        
        # Organize results by benchmark
        results_by_benchmark = defaultdict(list)
        for result in results:
            results_by_benchmark[result.benchmark_name].append(result)
        
        # Calculate summary statistics
        total_cost = sum(r.cost_usd for r in results)
        avg_score = sum(r.score for r in results) / len(results) if results else 0
        
        # Build markdown content
        lines = []
        lines.append("# LLM Evaluation Report")
        lines.append(f"\n**Run ID:** {self.run_id}")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"\n---\n")
        
        # Executive Summary
        lines.append("## Executive Summary\n")
        lines.append(f"- **Models Evaluated:** {len(results_by_model)}")
        lines.append(f"- **Benchmarks Run:** {len(results_by_benchmark)}")
        lines.append(f"- **Total Evaluations:** {len(results)}")
        lines.append(f"- **Total Cost:** ${total_cost:.4f}")
        lines.append(f"- **Average Score:** {avg_score:.3f}")
        lines.append("")
        
        # Model Rankings
        lines.append("## Model Rankings\n")
        lines.append("Ranked by average score across all benchmarks:\n")
        
        model_scores = []
        for model_id, model_results in results_by_model.items():
            avg = sum(r.score for r in model_results) / len(model_results)
            total_cost = sum(r.cost_usd for r in model_results)
            model_scores.append((model_id, avg, total_cost))
        
        model_scores.sort(key=lambda x: x[1], reverse=True)
        
        lines.append("| Rank | Model | Avg Score | Total Cost |")
        lines.append("|------|-------|-----------|------------|")
        for i, (model_id, score, cost) in enumerate(model_scores, 1):
            lines.append(f"| {i} | `{model_id}` | {score:.3f} | ${cost:.4f} |")
        lines.append("")
        
        # Cost Efficiency
        lines.append("## Cost Efficiency\n")
        lines.append("Score per dollar spent (higher is better):\n")
        
        efficiency = []
        for model_id, model_results in results_by_model.items():
            avg_score = sum(r.score for r in model_results) / len(model_results)
            total_cost = sum(r.cost_usd for r in model_results)
            if total_cost > 0:
                eff = avg_score / total_cost
                efficiency.append((model_id, eff, avg_score, total_cost))
        
        efficiency.sort(key=lambda x: x[1], reverse=True)
        
        lines.append("| Model | Score/$ | Avg Score | Total Cost |")
        lines.append("|-------|---------|-----------|------------|")
        for model_id, eff, score, cost in efficiency:
            lines.append(f"| `{model_id}` | {eff:.2f} | {score:.3f} | ${cost:.4f} |")
        lines.append("")
        
        # Per-Model Results
        lines.append("## Per-Model Results\n")
        
        for model_id, model_results in results_by_model.items():
            lines.append(f"### {model_id}\n")
            
            # Summary table
            lines.append("| Benchmark | Score | Cost ($) | Latency (ms) | Tokens |")
            lines.append("|-----------|-------|----------|--------------|--------|")
            
            for result in model_results:
                lines.append(
                    f"| {result.benchmark_name} | {result.score:.3f} | "
                    f"${result.cost_usd:.4f} | {result.latency_ms:.0f} | {result.total_tokens} |"
                )
            
            # Model summary
            model_avg = sum(r.score for r in model_results) / len(model_results)
            model_cost = sum(r.cost_usd for r in model_results)
            model_latency = sum(r.latency_ms for r in model_results) / len(model_results)
            
            lines.append("")
            lines.append(f"**Summary:** Avg Score: {model_avg:.3f}, Total Cost: ${model_cost:.4f}, Avg Latency: {model_latency:.0f}ms")
            lines.append("")
        
        # Benchmark Analysis
        lines.append("## Benchmark Analysis\n")
        
        for benchmark_name, benchmark_results in results_by_benchmark.items():
            lines.append(f"### {benchmark_name}\n")
            
            lines.append("| Model | Score | Cost ($) | Latency (ms) |")
            lines.append("|-------|-------|----------|--------------|")
            
            for result in benchmark_results:
                lines.append(
                    f"| `{result.model_id}` | {result.score:.3f} | "
                    f"${result.cost_usd:.4f} | {result.latency_ms:.0f} |"
                )
            
            benchmark_avg = sum(r.score for r in benchmark_results) / len(benchmark_results)
            lines.append("")
            lines.append(f"**Average Score:** {benchmark_avg:.3f}")
            lines.append("")
        
        # Graphs Section
        if self.generate_graphs:
            lines.append("## Visualizations\n")
            lines.append("Generated graphs:\n")
            lines.append("- `scores_comparison.png` - Score comparison across models and benchmarks")
            lines.append("- `cost_vs_score.png` - Cost vs Score scatter plot")
            lines.append("- `latency_heatmap.png` - Latency heatmap by model and benchmark")
            lines.append("- `radar_chart.png` - Capability radar chart per model")
            lines.append("")
        
        # Write report
        with open(report_path, 'w') as f:
            f.write('\n'.join(lines))
        
        return report_path
    
    def _generate_graphs(self, results: List[BenchmarkResult]) -> None:
        """Generate all visualization graphs."""
        self._generate_scores_comparison(results)
        self._generate_cost_vs_score(results)
        self._generate_latency_heatmap(results)
        self._generate_radar_chart(results)
    
    def _generate_scores_comparison(self, results: List[BenchmarkResult]) -> None:
        """Generate grouped bar chart of scores."""
        # Organize data
        results_by_model = defaultdict(lambda: defaultdict(float))
        for result in results:
            results_by_model[result.model_id][result.benchmark_name] = result.score
        
        models = list(results_by_model.keys())
        benchmarks = sorted(set(r.benchmark_name for r in results))
        
        # Create figure
        fig, ax = plt.subplots(figsize=(14, 6))
        
        x = np.arange(len(benchmarks))
        width = 0.15
        
        for i, model in enumerate(models):
            scores = [results_by_model[model].get(b, 0) for b in benchmarks]
            ax.bar(x + i * width, scores, width, label=model.split('/')[-1])
        
        ax.set_xlabel('Benchmark')
        ax.set_ylabel('Score')
        ax.set_title('Score Comparison Across Models and Benchmarks')
        ax.set_xticks(x + width * (len(models) - 1) / 2)
        ax.set_xticklabels(benchmarks, rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.graphs_dir, 'scores_comparison.png'), dpi=150)
        plt.close()
    
    def _generate_cost_vs_score(self, results: List[BenchmarkResult]) -> None:
        """Generate scatter plot of cost vs score."""
        # Aggregate by model
        model_data = defaultdict(lambda: {'scores': [], 'costs': []})
        for result in results:
            model_data[result.model_id]['scores'].append(result.score)
            model_data[result.model_id]['costs'].append(result.cost_usd)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for model_id, data in model_data.items():
            avg_score = sum(data['scores']) / len(data['scores'])
            total_cost = sum(data['costs'])
            ax.scatter(total_cost, avg_score, s=100, label=model_id.split('/')[-1])
        
        ax.set_xlabel('Total Cost ($)')
        ax.set_ylabel('Average Score')
        ax.set_title('Cost vs Performance Trade-off')
        ax.legend()
        ax.grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.graphs_dir, 'cost_vs_score.png'), dpi=150)
        plt.close()
    
    def _generate_latency_heatmap(self, results: List[BenchmarkResult]) -> None:
        """Generate latency heatmap."""
        # Create pivot data
        models = sorted(set(r.model_id for r in results))
        benchmarks = sorted(set(r.benchmark_name for r in results))
        
        data = np.zeros((len(models), len(benchmarks)))
        for result in results:
            i = models.index(result.model_id)
            j = benchmarks.index(result.benchmark_name)
            data[i, j] = result.latency_ms / 1000  # Convert to seconds
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        im = ax.imshow(data, cmap='YlOrRd', aspect='auto')
        
        ax.set_xticks(np.arange(len(benchmarks)))
        ax.set_yticks(np.arange(len(models)))
        ax.set_xticklabels(benchmarks, rotation=45, ha='right')
        ax.set_yticklabels([m.split('/')[-1] for m in models])
        
        ax.set_xlabel('Benchmark')
        ax.set_ylabel('Model')
        ax.set_title('Latency Heatmap (seconds)')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Latency (s)')
        
        # Add text annotations
        for i in range(len(models)):
            for j in range(len(benchmarks)):
                text = ax.text(j, i, f'{data[i, j]:.1f}',
                             ha="center", va="center", color="black", fontsize=8)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.graphs_dir, 'latency_heatmap.png'), dpi=150)
        plt.close()
    
    def _generate_radar_chart(self, results: List[BenchmarkResult]) -> None:
        """Generate radar chart for model capabilities."""
        # Organize data by model
        model_scores = defaultdict(dict)
        for result in results:
            model_scores[result.model_id][result.benchmark_name] = result.score
        
        benchmarks = sorted(set(r.benchmark_name for r in results))
        
        # Number of variables
        N = len(benchmarks)
        
        # Compute angle for each axis
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Complete the circle
        
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        colors = plt.cm.tab10(np.linspace(0, 1, len(model_scores)))
        
        for idx, (model_id, scores) in enumerate(model_scores.items()):
            values = [scores.get(b, 0) for b in benchmarks]
            values += values[:1]  # Complete the circle
            
            ax.plot(angles, values, 'o-', linewidth=2, label=model_id.split('/')[-1], color=colors[idx])
            ax.fill(angles, values, alpha=0.15, color=colors[idx])
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(benchmarks)
        ax.set_ylim(0, 1)
        ax.set_title('Model Capability Radar Chart', size=16, y=1.08)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        ax.grid(True)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.graphs_dir, 'radar_chart.png'), dpi=150)
        plt.close()
