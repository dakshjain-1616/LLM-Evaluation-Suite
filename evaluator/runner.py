"""Parallel benchmark runner with ProcessPoolExecutor."""

import os
import sys
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict

from .benchmarks.base import BenchmarkResult, BenchmarkConfig
from .cost_tracker import CostTracker


def run_single_benchmark_task(
    model_config: Dict,
    benchmark_name: str,
    config: Dict,
    logs_dir: str,
    dry_run: bool = False
) -> Dict[str, Any]:
    """Run a single benchmark for a single model (module-level function for pickling)."""
    model_id = model_config['id']
    model_name = model_config.get('name', model_id)
    
    # Setup per-job logger
    logger = logging.getLogger(f'{model_id}_{benchmark_name}')
    logger.handlers = []
    logger.setLevel(logging.INFO)
    
    job_handler = logging.FileHandler(
        os.path.join(logs_dir, f'{model_id.replace("/", "_")}_{benchmark_name}.log')
    )
    job_handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s'))
    logger.addHandler(job_handler)
    
    logger.info(f"Starting benchmark {benchmark_name} for model {model_id}")
    
    start_time = datetime.now()
    
    try:
        # Dynamically import benchmark class
        if benchmark_name == 'math500':
            from .benchmarks.math500 import Math500Benchmark
            benchmark = Math500Benchmark()
        elif benchmark_name == 'aime':
            from .benchmarks.aime import AIMEBenchmark
            benchmark = AIMEBenchmark()
        elif benchmark_name == 'frontier_math':
            from .benchmarks.frontier_math import FrontierMathBenchmark
            benchmark = FrontierMathBenchmark()
        elif benchmark_name == 'math_vista':
            from .benchmarks.math_vista import MathVistaBenchmark
            benchmark = MathVistaBenchmark()
        elif benchmark_name == 'bigcodebench':
            from .benchmarks.bigcodebench import BigCodeBenchBenchmark
            benchmark = BigCodeBenchBenchmark()
        elif benchmark_name == 'swe_bench_pro':
            from .benchmarks.swe_bench_pro import SWEBenchProBenchmark
            benchmark = SWEBenchProBenchmark()
        elif benchmark_name == 'livecodebench':
            from .benchmarks.livecodebench import LiveCodeBenchBenchmark
            benchmark = LiveCodeBenchBenchmark()
        elif benchmark_name == 'humaneval_plus':
            from .benchmarks.humaneval_plus import HumanEvalPlusBenchmark
            benchmark = HumanEvalPlusBenchmark()
        elif benchmark_name == 'helmet_ruler':
            from .benchmarks.helmet_ruler import HELMETRulerBenchmark
            benchmark = HELMETRulerBenchmark()
        elif benchmark_name == 'zeroscrolls':
            from .benchmarks.zeroscrolls import ZeroScrollsBenchmark
            benchmark = ZeroScrollsBenchmark()
        elif benchmark_name == 'infinitebench':
            from .benchmarks.infinitebench import InfiniteBenchBenchmark
            benchmark = InfiniteBenchBenchmark()
        elif benchmark_name == 'frames':
            from .benchmarks.frames import FRAMESBenchmark
            benchmark = FRAMESBenchmark()
        elif benchmark_name == 'ifeval':
            from .benchmarks.ifeval import IFEvalBenchmark
            benchmark = IFEvalBenchmark()
        elif benchmark_name == 'wildbench':
            from .benchmarks.wildbench import WildBenchBenchmark
            benchmark = WildBenchBenchmark()
        elif benchmark_name == 'simpleqa':
            from .benchmarks.simpleqa import SimpleQABenchmark
            benchmark = SimpleQABenchmark()
        elif benchmark_name == 'medqa':
            from .benchmarks.medqa import MedQABenchmark
            benchmark = MedQABenchmark()
        elif benchmark_name == 'legalbench':
            from .benchmarks.legalbench import LegalBenchBenchmark
            benchmark = LegalBenchBenchmark()
        elif benchmark_name == 'mirage':
            from .benchmarks.mirage import MIRAGEBenchmark
            benchmark = MIRAGEBenchmark()
        elif benchmark_name == 'strong_reject':
            from .benchmarks.strong_reject import StrongREJECTBenchmark
            benchmark = StrongREJECTBenchmark()
        elif benchmark_name == 'harmbench':
            from .benchmarks.harmbench import HarmBenchBenchmark
            benchmark = HarmBenchBenchmark()
        elif benchmark_name == 'truthfulqa':
            from .benchmarks.truthfulqa import TruthfulQABenchmark
            benchmark = TruthfulQABenchmark()
        elif benchmark_name == 'docvqa':
            from .benchmarks.docvqa import DocVQABenchmark
            benchmark = DocVQABenchmark()
        elif benchmark_name == 'video_mme':
            from .benchmarks.video_mme import VideoMMEBenchmark
            benchmark = VideoMMEBenchmark()
        elif benchmark_name == 'tau_bench':
            from .benchmarks.tau_bench import TauBenchBenchmark
            benchmark = TauBenchBenchmark()
        elif benchmark_name == 'gaia':
            from .benchmarks.gaia import GAIABenchmark
            benchmark = GAIABenchmark()
        elif benchmark_name == 'web_arena':
            from .benchmarks.web_arena import WebArenaBenchmark
            benchmark = WebArenaBenchmark()
        # Legacy benchmarks
        elif benchmark_name == 'swe_bench':
            from .benchmarks.swe_bench import SWEBenchBenchmark
            benchmark = SWEBenchBenchmark()
        elif benchmark_name == 'gpqa':
            from .benchmarks.gpqa import GPQABenchmark
            benchmark = GPQABenchmark()
        elif benchmark_name == 'mmlu_pro':
            from .benchmarks.mmlu_pro import MMLUProBenchmark
            benchmark = MMLUProBenchmark()
        elif benchmark_name == 'terminal_bench':
            from .benchmarks.terminal_bench import TerminalBenchBenchmark
            benchmark = TerminalBenchBenchmark()
        elif benchmark_name == 'osworld':
            from .benchmarks.osworld import OSWorldBenchmark
            benchmark = OSWorldBenchmark()
        elif benchmark_name == 'mmmu_pro':
            from .benchmarks.mmmu_pro import MMMUProBenchmark
            benchmark = MMMUProBenchmark()
        elif benchmark_name == 'agentbench':
            from .benchmarks.agentbench import AgentBenchBenchmark
            benchmark = AgentBenchBenchmark()
        elif benchmark_name == 'mt_bench':
            from .benchmarks.mt_bench import MTBenchBenchmark
            benchmark = MTBenchBenchmark()
        else:
            raise ValueError(f"Unknown benchmark: {benchmark_name}")
        
        prompts = benchmark.get_prompts()
        sample_size = config.get('benchmarks', {}).get('sample_size', 20)
        prompts = prompts[:sample_size]
        
        if dry_run:
            logger.info("DRY RUN - Skipping API calls")
            end_time = datetime.now()
            latency_ms = (end_time - start_time).total_seconds() * 1000
            
            return {
                'benchmark_name': benchmark_name,
                'model_id': model_id,
                'prompt_id': f'{benchmark_name}_aggregate',
                'start_time': start_time,
                'end_time': end_time,
                'latency_ms': latency_ms,
                'prompt': f'DRY RUN - {len(prompts)} prompts',
                'response': 'DRY RUN',
                'expected_answer': None,
                'success': True,
                'score': 0.0,
                'token_count_input': 0,
                'token_count_output': 0,
                'error_message': None,
                'metadata': {
                    'model_name': model_name,
                    'samples_run': len(prompts),
                    'cost_usd': 0.0,
                    'latency_avg_s': 0.0,
                    'dry_run': True
                }
            }
        
        # Real execution
        from openai import OpenAI
        client = OpenAI(
            base_url=config['openrouter']['base_url'],
            api_key=config['openrouter']['api_key']
        )
        
        cost_tracker = CostTracker()
        results = []
        total_cost = 0.0
        total_latency = 0.0
        total_input_tokens = 0
        total_output_tokens = 0
        errors = []
        
        for i, prompt_data in enumerate(prompts):
            try:
                prompt_start = time.time()
                
                messages = [
                    {"role": "user", "content": prompt_data['prompt']}
                ]
                
                system_prompt = benchmark.get_system_prompt()
                if system_prompt:
                    messages.insert(0, {"role": "system", "content": system_prompt})
                
                response = client.chat.completions.create(
                    model=model_id,
                    messages=messages,
                    max_tokens=config.get('evaluation', {}).get('max_tokens', 1024),
                    temperature=config.get('evaluation', {}).get('temperature', 0.7)
                )
                
                latency = time.time() - prompt_start
                total_latency += latency
                
                # Track tokens and cost
                usage = response.usage
                if usage:
                    total_input_tokens += usage.prompt_tokens
                    total_output_tokens += usage.completion_tokens
                    cost = cost_tracker.calculate_cost(
                        model_id, usage.prompt_tokens, usage.completion_tokens
                    )
                    total_cost += cost
                
                # Evaluate response
                eval_result = benchmark.evaluate_response(
                    prompt_data, response.choices[0].message.content
                )
                results.append(eval_result)
                
                logger.info(f"Prompt {i+1}/{len(prompts)}: score={eval_result.get('score', 0):.2f}")
                
            except Exception as e:
                error_msg = f"Error on prompt {i+1}: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                results.append({'success': False, 'score': 0.0, 'error': str(e)})
        
        # Calculate aggregate metrics
        scores = [r.get('score', 0) for r in results if 'score' in r]
        avg_score = sum(scores) / len(scores) if scores else 0.0
        avg_latency = total_latency / len(prompts) if prompts else 0.0
        
        end_time = datetime.now()
        total_latency_ms = (end_time - start_time).total_seconds() * 1000
        
        logger.info(f"Benchmark complete: score={avg_score:.2f}, cost=${total_cost:.4f}")
        
        return {
            'benchmark_name': benchmark_name,
            'model_id': model_id,
            'prompt_id': f'{benchmark_name}_aggregate',
            'start_time': start_time,
            'end_time': end_time,
            'latency_ms': total_latency_ms,
            'prompt': f'Aggregate of {len(prompts)} prompts',
            'response': json.dumps(results),
            'expected_answer': None,
            'success': len(errors) == 0,
            'score': avg_score,
            'token_count_input': total_input_tokens,
            'token_count_output': total_output_tokens,
            'error_message': '; '.join(errors) if errors else None,
            'metadata': {
                'model_name': model_name,
                'samples_run': len(prompts),
                'cost_usd': total_cost,
                'latency_avg_s': avg_latency,
                'details': results
            }
        }
        
    except Exception as e:
        error_msg = f"Benchmark failed: {str(e)}"
        logger.error(error_msg)
        end_time = datetime.now()
        latency_ms = (end_time - start_time).total_seconds() * 1000
        
        return {
            'benchmark_name': benchmark_name,
            'model_id': model_id,
            'prompt_id': f'{benchmark_name}_error',
            'start_time': start_time,
            'end_time': end_time,
            'latency_ms': latency_ms,
            'prompt': 'Error',
            'response': '',
            'expected_answer': None,
            'success': False,
            'score': 0.0,
            'token_count_input': 0,
            'token_count_output': 0,
            'error_message': error_msg,
            'metadata': {
                'model_name': model_name,
                'samples_run': 0,
                'cost_usd': 0.0,
                'latency_avg_s': 0.0
            }
        }


class BenchmarkRunner:
    """Runs benchmarks in parallel using ProcessPoolExecutor."""
    
    def __init__(self, config: Dict[str, Any], run_id: Optional[str] = None):
        self.config = config
        self.run_id = run_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results: List[BenchmarkResult] = []
        self.cost_tracker = CostTracker()
        
        # Setup directories
        self.logs_dir = os.path.join(
            config.get('output', {}).get('logs_dir', 'logs'), self.run_id
        )
        self.reports_dir = os.path.join(
            config.get('output', {}).get('reports_dir', 'reports'), self.run_id
        )
        os.makedirs(self.logs_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # Setup logging
        self._setup_logging()
        
    def _setup_logging(self) -> None:
        """Setup logging configuration."""
        log_format = '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s'
        
        # Master log file
        master_log = os.path.join(self.logs_dir, 'master.log')
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(master_log),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('BenchmarkRunner')
        
    def run(self, models: List[Dict], benchmarks: List[str], dry_run: bool = False) -> List[BenchmarkResult]:
        """Run all benchmarks for all models in parallel."""
        self.logger.info(f"Starting evaluation run: {self.run_id}")
        self.logger.info(f"Models: {[m['id'] for m in models]}")
        self.logger.info(f"Benchmarks: {benchmarks}")
        self.logger.info(f"Dry run: {dry_run}")
        
        max_workers = self.config.get('benchmarks', {}).get('max_workers', 4)
        tasks = [(model, benchmark) for model in models for benchmark in benchmarks]
        
        self.logger.info(f"Total tasks: {len(tasks)}, Max workers: {max_workers}")
        
        results = []
        completed = 0
        
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            future_to_task = {
                executor.submit(
                    run_single_benchmark_task,
                    model,
                    benchmark,
                    self.config,
                    self.logs_dir,
                    dry_run
                ): (model, benchmark)
                for model, benchmark in tasks
            }
            
            for future in as_completed(future_to_task):
                model, benchmark = future_to_task[future]
                try:
                    result_dict = future.result()
                    # Promote cost from metadata to top-level field
                    result_dict['cost_usd'] = result_dict.get('metadata', {}).get('cost_usd', 0.0)
                    result = BenchmarkResult(**result_dict)
                    results.append(result)
                    completed += 1
                    self.logger.info(f"Completed {completed}/{len(tasks)}: {model['id']} - {benchmark}")
                except Exception as e:
                    self.logger.error(f"Task failed for {model['id']} - {benchmark}: {e}")
                    # Create error result
                    error_result = BenchmarkResult(
                        benchmark_name=benchmark,
                        model_id=model['id'],
                        prompt_id=f'{benchmark}_error',
                        start_time=datetime.now(),
                        end_time=datetime.now(),
                        latency_ms=0.0,
                        prompt='Error',
                        response='',
                        success=False,
                        score=0.0,
                        error_message=str(e),
                        metadata={
                            'model_name': model.get('name', model['id']),
                            'samples_run': 0,
                            'cost_usd': 0.0,
                            'latency_avg_s': 0.0
                        }
                    )
                    results.append(error_result)
        
        self.results = results
        self.logger.info(f"Evaluation complete. Results saved to {self.reports_dir}")
        
        return results
    
    def save_results(self) -> str:
        """Save results to JSON file."""
        results_file = os.path.join(self.reports_dir, 'results.json')
        with open(results_file, 'w') as f:
            json.dump([asdict(r) for r in self.results], f, indent=2, default=str)
        return results_file
