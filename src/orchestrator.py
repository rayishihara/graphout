import os
import re
import json
import mlflow
import pandas as pd

from src.agent_factory import AgentFactory
from src.agents.config import ChartSpec
from src.agents.executor.executor import Executor
from src.preprocess import extract_csv_metadata

class Orchestrator:
    def __init__(self) -> None:
        factory = AgentFactory()
        self.analyst = factory.create_analyst()
        self.big_guy = factory.create_big_guy()
        self.executor = Executor()

    def _parse_spec(self, text: str, metadata: dict) -> ChartSpec:
        match = re.search(r"\{.*?\}", text, re.DOTALL)
        if match is None:
            raise ValueError("No JSON object found in the response")
        spec = ChartSpec.model_validate_json(match.group())

        schema = metadata["schema"]
        for col in (spec.x, spec.y):
            if col is not None and col not in schema:
                raise ValueError(f"Column '{col}' does not exist; use one of {list(schema)}")

        numeric_col = spec.x if spec.chart_type == "histogram" else spec.y
        if schema[numeric_col]["inferred_type"] != "numerical":
            raise ValueError(f"A {spec.chart_type} chart needs '{numeric_col}' to be numerical")

        return spec

    def run(self, csv_path: str, output_path: str = "chart.png") -> str:
        df = pd.read_csv(csv_path)
        metadata = extract_csv_metadata(csv_path)

        with mlflow.start_run(run_name="pipeline"):
            mlflow.log_param("csv_name", os.path.basename(csv_path))

            summary = self.analyst.run(
                f"Metadata:\n{json.dumps(metadata)}\n\nFirst rows:\n{df.head(5).to_csv(index=False)}"
            )

            columns = "\n".join(f"- {name}: {info['inferred_type']}" for name, info in metadata["schema"].items())
            message = f"Summary:\n{summary}\n\nColumns:\n{columns}"

            # Retry Big Guy once with the validation error
            for attempt in (1, 2):
                response = self.big_guy.run(message)
                try:
                    spec = self._parse_spec(response, metadata)
                    break
                except ValueError as e:
                    if attempt == 2:
                        raise ValueError(f"Big Guy gave an invalid chart spec twice: {e}\nLast response:\n{response}") from e
                    message = f"{message}\n\nYour previous response was:\n{response}\n\nIt was invalid: {e}\nTry again."

            mlflow.log_param("big_guy_attempts", attempt)
            mlflow.log_dict(spec.model_dump(), "spec.json")

            self.executor.run(df, spec, output_path)
            mlflow.log_artifact(output_path)

        return output_path
