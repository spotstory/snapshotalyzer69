import boto3
import click

session = boto3.Session(profile_name='snappy')
ec2 = session.resource('ec2')

def tags_dict(instance):
    return { t['Key']: t['Value'] for t in instance.tags or []}

def filter_instances(project):
    if project:
        filters = [{'Name':'tag:Project','Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances

@click.group()
def instances():
    """Commands for instances"""

@instances.command('list')
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def list_snapshots(project):
    "List EC2 instances"
    instances = filter_instances(project)

    for i in instances:
        tags = tags_dict(i)

        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project', '<no project>'))))

    return

@instances.command('stop')
@click.option('--project', default=None,
    help="Only instances for project")
def stop_snapshots(project):
    "Stop EC2 instances"
    instances = filtered_instances(project)

    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()

    return

@instances.command('start')
@click.option('--project', default=None,
    help="Only instances for project")
def start_snapshots(project):
    "Start EC2 instances"
    instances = filter_instances(project)

    for i in instances:
        print("Starting {0}...".format(i.id))
        i.start()

    return

if __name__ == '__main__':
    instances()
