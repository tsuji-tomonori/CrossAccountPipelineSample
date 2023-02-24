from __future__ import annotations

from pathlib import Path

import aws_cdk as cdk
import tomli
from aws_cdk import Tags

from cdk.stack_cicd import CICD

pyproject_path = Path.cwd() / "pyproject.toml"
with pyproject_path.open("rb") as f:
    pyproject = tomli.load(f)

project_name = pyproject["project"]["name"].replace("_", "-")

app = cdk.App()
stack = CICD(app, project_name, env=cdk.Environment(
    account="167545301745",
    region="ap-northeast-1",
))
Tags.of(stack).add("Project", project_name)
Tags.of(stack).add("Type", "dev")
Tags.of(stack).add("Creator", "cdk")
app.synth()
