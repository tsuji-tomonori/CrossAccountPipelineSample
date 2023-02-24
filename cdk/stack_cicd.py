from __future__ import annotations

from typing import Any

import aws_cdk as cdk
from aws_cdk import Stack, aws_codecommit, pipelines
from constructs import Construct

from cdk.stage_app import AppStage


class CICD(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs: Any) -> None:
        super().__init__(scope, construct_id, **kwargs)

        repository = aws_codecommit.Repository(
            self,
            "repository",
            repository_name=construct_id,
        )

        pipeline = pipelines.CodePipeline(
            self,
            "pipeline",
            pipeline_name=construct_id,
            synth=pipelines.ShellStep(
                "synth",
                input=pipelines.CodePipelineSource.code_commit(
                    repository, branch="main"),
                install_commands=[
                    "pip install --upgrade pip",
                    "pip install -r requirements-deploy.txt",
                    "npm install -g aws-cdk",
                ],
                commands=[
                    "cdk synth",
                ]
            ),
            cross_account_keys=True,
        )

        stg = AppStage(self, "stg", env=cdk.Environment(
            account="167545301745",
            region="ap-northeast-1",
        ))
        pipeline.add_stage(stg)

        pro = AppStage(self, "pro", env=cdk.Environment(
            account="560779131333",
            region="ap-northeast-1",
        ))
        pipeline.add_stage(pro)
