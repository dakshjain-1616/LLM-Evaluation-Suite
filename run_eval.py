#!/usr/bin/env python3
"""LLM Evaluation Suite — CLI entrypoint.

Usage:
  python run_eval.py                                         # use config.yaml
  python run_eval.py --config my.yaml                       # custom config
  python run_eval.py --models anthropic/claude-opus-4       # override models
  python run_eval.py --benchmarks gpqa mmlu_pro             # subset
  python run_eval.py --dry-run                              # simulate, no API
  python run_eval.py --sample-size 5                        # prompts per bench
"""

import argparse
import os
import sys
import yaml
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

ALL_BENCHMARK_NAMES = [
    # Math & Formal Reasoning
    "math500", "aime", "frontier_math", "math_vista",
    # Code Generation & Debugging
    "bigcodebench", "swe_bench_pro", "livecodebench", "humaneval_plus",
    # Long-Context Understanding
    "helmet_ruler", "zeroscrolls", "infinitebench", "frames",
    # Instruction Following
    "ifeval", "wildbench",
    # Knowledge & QA
    "simpleqa", "medqa", "legalbench",
    # RAG & Grounded Generation
    "mirage",
    # Safety & Alignment
    "strong_reject", "harmbench", "truthfulqa",
    # Multimodal
    "docvqa", "video_mme",
    # Agent & Tool Use
    "tau_bench", "gaia", "web_arena",
]


def load_config(path: str) -> dict:
    raw = open(path).read()
    # Expand ${ENV_VAR} references
    import re
    for match in re.finditer(r'\$\{(\w+)\}', raw):
        val = os.environ.get(match.group(1), "")
        raw = raw.replace(match.group(0), val)
    return yaml.safe_load(raw)


def build_model_list(config: dict, override: list) -> list:
    if override:
        return [{"id": m, "name": m.split("/")[-1]} for m in override]
    return config.get("models", [])


def print_summary(results, run_id: str, report_path: str):
    from collections import defaultdict
    model_data = defaultdict(lambda: {"scores": [], "costs": [], "latencies": []})
    for r in results:
        mid = r.model_id
        model_data[mid]["scores"].append(r.score)
        model_data[mid]["costs"].append(r.cost_usd)
        model_data[mid]["latencies"].append(r.latency_ms)

    table = Table(title=f"Evaluation Results — Run {run_id}", header_style="bold cyan")
    table.add_column("Model", style="bold")
    table.add_column("Avg Score", justify="right")
    table.add_column("Total Cost", justify="right")
    table.add_column("Avg Latency", justify="right")
    table.add_column("Score/$", justify="right")

    rows = []
    for model_id, data in model_data.items():
        avg_score = sum(data["scores"]) / len(data["scores"])
        total_cost = sum(data["costs"])
        avg_lat = sum(data["latencies"]) / len(data["latencies"])
        efficiency = avg_score / total_cost if total_cost > 0 else float("inf")
        rows.append((model_id, avg_score, total_cost, avg_lat, efficiency))

    rows.sort(key=lambda x: x[1], reverse=True)
    for model_id, avg_score, total_cost, avg_lat, efficiency in rows:
        eff_str = f"{efficiency:.1f}" if efficiency != float("inf") else "∞"
        table.add_row(
            model_id.split("/")[-1],
            f"{avg_score:.3f}",
            f"${total_cost:.4f}",
            f"{avg_lat:.0f}ms",
            eff_str,
        )

    console.print(table)
    console.print(f"\n[green]Report:[/green]  {report_path}")


def main():
    parser = argparse.ArgumentParser(description="LLM Evaluation Suite via OpenRouter")
    parser.add_argument("--config",       default="config.yaml")
    parser.add_argument("--models",       nargs="+", help="OpenRouter model IDs")
    parser.add_argument("--benchmarks",   nargs="+", choices=ALL_BENCHMARK_NAMES + ["gpqa_diamond"])
    parser.add_argument("--sample-size",  type=int)
    parser.add_argument("--output-dir",   help="Override reports output dir")
    parser.add_argument("--dry-run",      action="store_true")
    parser.add_argument("--workers",      type=int)
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        console.print(f"[red]Config not found: {config_path}[/red]"); sys.exit(1)

    config = load_config(str(config_path))

    if args.output_dir:
        config.setdefault("output", {})["reports_dir"] = args.output_dir
    if args.workers:
        config.setdefault("benchmarks", {})["max_workers"] = args.workers
    if args.sample_size:
        config.setdefault("benchmarks", {})["sample_size"] = args.sample_size
    config.setdefault("output", {}).setdefault("generate_graphs", True)

    if not args.dry_run:
        api_key = config.get("openrouter", {}).get("api_key", "")
        if not api_key:
            console.print("[red]OPENROUTER_API_KEY not set.[/red]"); sys.exit(1)

    models = build_model_list(config, args.models or [])
    if not models:
        console.print("[red]No models configured.[/red]"); sys.exit(1)

    # Determine benchmark names to run
    if args.benchmarks:
        bench_names = ["gpqa" if b == "gpqa_diamond" else b for b in args.benchmarks]
    else:
        bench_names = config.get("benchmarks", {}).get("enabled", ALL_BENCHMARK_NAMES)

    mode = "[yellow]DRY RUN[/yellow]" if args.dry_run else "[green]LIVE[/green]"
    console.print(Panel(
        f"Mode: {mode}\n"
        f"Models ({len(models)}): {', '.join(m['id'] for m in models)}\n"
        f"Benchmarks ({len(bench_names)}): {', '.join(bench_names)}\n"
        f"Workers: {config.get('benchmarks', {}).get('max_workers', 8)}",
        title="LLM Evaluation Suite", border_style="cyan",
    ))

    from evaluator.runner import BenchmarkRunner
    from evaluator.report_generator import ReportGenerator

    runner = BenchmarkRunner(config)

    with console.status("[bold green]Running benchmarks...[/bold green]"):
        results = runner.run(models, bench_names, dry_run=args.dry_run)

    if not results:
        console.print("[red]No results collected.[/red]"); sys.exit(1)

    results_path = runner.save_results()

    report_gen = ReportGenerator(config, runner.run_id)
    report_path = report_gen.generate(results)

    print_summary(results, runner.run_id, report_path)

    graphs_dir = os.path.join(
        config.get("output", {}).get("reports_dir", "reports"),
        runner.run_id, "graphs"
    )
    logs_dir = os.path.join(
        config.get("output", {}).get("logs_dir", "logs"),
        runner.run_id
    )
    console.print(f"[green]Graphs:[/green]  {graphs_dir}/")
    console.print(f"[green]Logs:[/green]    {logs_dir}/")
    console.print(f"[green]Raw JSON:[/green] {results_path}")


if __name__ == "__main__":
    main()
