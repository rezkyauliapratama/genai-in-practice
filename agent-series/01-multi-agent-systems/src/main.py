"""CLI entrypoint: pilih demo multi-agent yang mau dijalankan.

Usage:
    python -m src.main --demo langgraph   # Task 2: supervisor (LangGraph)
    python -m src.main --demo adk         # Task 3: ADK hierarchy
    python -m src.main --demo pipeline    # Task 4: 2-agent pipeline
    python -m src.main --demo all         # semua berurutan
"""
import argparse
import sys


def main() -> None:
    parser = argparse.ArgumentParser(description="Multi-Agent Systems demo runner")
    parser.add_argument(
        "--demo",
        choices=["langgraph", "adk", "pipeline", "all"],
        default="all",
        help="demo mana yang dijalankan (default: all)",
    )
    args = parser.parse_args()

    demos = {
        "langgraph": ("Task 2 — LangGraph Supervisor", run_langgraph),
        "adk": ("Task 3 — Google ADK", run_adk),
        "pipeline": ("Task 4 — 2-Agent Pipeline", run_pipeline),
    }

    selected = demos.keys() if args.demo == "all" else [args.demo]
    for key in selected:
        title, fn = demos[key]
        print(f"\n{'#'*60}\n# {title}\n{'#'*60}")
        try:
            fn()
        except Exception as e:  # noqa: BLE001 - demo runner menampilkan error per demo
            print(f"[ERROR] {key}: {e}", file=sys.stderr)


def run_langgraph():
    from .langgraph_supervisor import run_supervisor

    summary, iters = run_supervisor()
    print("=" * 50)
    print("FINAL SUMMARY:")
    print("=" * 50)
    print(summary)
    print(f"\n[debug] iterations dipakai: {iters}")


def run_adk():
    from .google_adk_agents import run_adk as _run

    _run()


def run_pipeline():
    from .research_summarize import run_pipeline as _run

    _run()


if __name__ == "__main__":
    main()
