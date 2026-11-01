import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from src.agents.config import ChartSpec


class Executor:
    def run(self, df: pd.DataFrame, spec: ChartSpec, output_path: str) -> str:
        fig, ax = plt.subplots()

        if spec.chart_type == "bar":
            df.groupby(spec.x)[spec.y].mean().plot.bar(ax=ax)
        elif spec.chart_type == "line":
            data = df.sort_values(spec.x)
            ax.plot(data[spec.x], data[spec.y])
        elif spec.chart_type == "scatter":
            ax.scatter(df[spec.x], df[spec.y])
        elif spec.chart_type == "histogram":
            ax.hist(df[spec.x].dropna())

        ax.set_xlabel(spec.x)
        ax.set_ylabel(spec.y if spec.y is not None else "count")
        ax.set_title(spec.title)

        fig.tight_layout()
        fig.savefig(output_path)
        plt.close(fig)

        return output_path
