import boto3

def lambda_handler(event, context):
    myFleet = [
        {
            "Name": "tag:fleet",
            "Values": ["workhorse"]
        },
        {
            "Name": "instance-state-name",
            "Values": ["running"]
        }
    ]

    ec2=boto3.resource("ec2")

    instances=ec2.instances.filter(Filters=myFleet)

    runningInstances=[instance.id for instance in instances]

    if runningInstances:
        ec2.instances.filter(InstanceIds=runningInstances).stop()
    else:
        print("Nothing to do here")