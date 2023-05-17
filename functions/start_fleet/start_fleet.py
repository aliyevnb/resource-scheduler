import boto3

def lambda_handler(event, context):
    myFleet=[
        {
            "Name": "tag:fleet",
            "Values": ["workhorse"]
        },
        {
            "Name": "instance-state-name",
            "Values": ["stopped"]
        }
    ]
    
    ec2=boto3.resource("ec2")

    instances=ec2.instances.filter(Filters=myFleet)

    stoppedInstances=[instance.id for instance in instances]

    if stoppedInstances:
        ec2.instance.filter(InstanceId=stoppedInstances).start()
    else:
        print("Nothing to do here...")