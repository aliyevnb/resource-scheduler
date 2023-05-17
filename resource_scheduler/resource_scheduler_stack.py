from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_ec2 as _ec2,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_iam as _iam
)
import timeUtil
import awsenv
from constructs import Construct

class ResourceSchedulerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        resourceSchedulerRole=_iam.Role(self,
            "rs-lambda-execution-role",
            role_name=awsenv.setRole(),
            assumed_by=_iam.ServicePrincipal("lambda.amazonaws.com")
        )

        resourceSchedulerRole.add_to_policy(
            _iam.PolicyStatement(
                effect=_iam.Effect.ALLOW,
                resources=[
                    "*"
                ],
                actions=[
                    "ec2:Describe*",
                    "ec2:StartInstances",
                    "ec2:StopInstances",
                    "ec2:AttachNetworkInterface",
                    "ec2:CreateNetworkInterface",
                    "ec2:DeleteNetworkInterface",
                    "ec2:DetachNetworkInterface",
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ]
            )
        )
        
        functionVpc=_ec2.Vpc.from_lookup(self, 
            "rs-lambda-vpc", 
            vpc_name=awsenv.setVpc())

        
        functionSubnet=_ec2.SubnetSelection(
            subnet_type=_ec2.SubnetType.PRIVATE_WITH_EGRESS
        )

        functionSg=_ec2.SecurityGroup.from_lookup_by_name(self,
            "rs-lambda-sg", 
            security_group_name=awsenv.setSg(), 
            vpc=functionVpc)
        
        stopEc2Fleet=_lambda.Function(
            self,
            "stop-fleet",
            code=_lambda.Code.from_asset("./functions/stop_fleet"),
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="stop_fleet.lambda_handler",
            architecture=_lambda.Architecture.ARM_64,
            function_name="stop_fleet",
            role=resourceSchedulerRole,
            vpc=functionVpc,
            vpc_subnets=functionSubnet,
            security_groups=[functionSg]
        )

        startEc2Fleet=_lambda.Function(
            self,
            "start-fleet",
            code=_lambda.Code.from_asset("./functions/start_fleet"),
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="start_fleet.lambda_handler",
            architecture=_lambda.Architecture.ARM_64,
            function_name="start_fleet",
            role=resourceSchedulerRole,
            vpc=functionVpc,
            vpc_subnets=functionSubnet,
            security_groups=[functionSg]           
        )

        startH, startM = timeUtil.startTime()
        stopH, stopM = timeUtil.stopTime()

        startFleet=_events.Rule(
            self,
            "start-ec2-instance-fleet-schedule",
            schedule=_events.Schedule.cron(
                minute=startM,
                hour=startH,
                week_day="1-5",
            )
        )

        startFleet.add_target(_targets.LambdaFunction(startEc2Fleet))
        
        stopFleet=_events.Rule(
            self,
            "stop-ec2-instance-fleet-schedule",
            schedule=_events.Schedule.cron(
                minute=stopM,
                hour=stopH,
                week_day="1-5",
            )
        )