from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import aws_cdk as cdk
from aws_cdk import Stack, Stage
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_logs as logs
from constructs import Construct


class AppStage(Stage):

    def __init__(self, scope: Construct, construct_id: str, env: cdk.Environment) -> None:
        super().__init__(scope, construct_id, env=env)

        settings_path = Path.cwd() / "settings" / \
            f"{env.account}_{env.region.replace('-', '_')}.json"  # type: ignore

        with settings_path.open(encoding="utf-8") as f:
            settings_json = json.load(f)

        AppStack(self, construct_id.split("_")[0], settings_json=settings_json)


class AppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, settings_json: dict[str, Any], **kwargs: Any) -> None:
        super().__init__(scope, construct_id, **kwargs)

        fn = _lambda.Function(
            self, f"{construct_id}_lambda",
            function_name=f"{construct_id}_lmd_cross_account_cicd_cdk",
            code=_lambda.Code.from_asset("src"),
            handler="lambda_function.lambda_handler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            timeout=cdk.Duration.seconds(3),
            environment=settings_json["env"],
            memory_size=256,
        )

        loggroup_name = f"/aws/lambda/{fn.function_name}"
        logs.LogGroup(
            self, f"{construct_id}-loggroup",
            log_group_name=loggroup_name,
            retention=logs.RetentionDays.ONE_DAY,
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )
