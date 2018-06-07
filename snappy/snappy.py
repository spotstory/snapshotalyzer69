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
def cli():
    """Snappy manages snapshots"""

### SNAPSHOTS ###
@cli.group('snapshots')
def snapshots():
    """Commands for Snapshots"""

## SNAPSHOTS LIST
@snapshots.command('list')
@click.option('--project', default=None,
    help="Only snapshots for project (tag Project:<name>)")
def list_snapshots(project):
    "List snapshots"

    instances = filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ".join((
                    s.id,
                    v.id,
                    i.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime("%c")
                )))

    return

### VOLUMES ###
@cli.group('volumes')
def volumes():
    """Commands for Volumes"""

## VOLUMES LIST
@volumes.command('list')
@click.option('--project', default=None,
    help="Only volumes for project (tag Project:<name>)")
def list_volumes(project):
    "List instance volumes"

    instances = filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
            print(", ".join((
                v.volume_id,
                v.state,
                str(v.size)+"GiB",
                v.encrypted and "Encrypted" or "Not Encrypted",
                str(v.tags)
            )))

    return

### INSTANCES ###
@cli.group('instances')
def instances():
    """Commands for instances"""

## INSTANCES SNAPSHOT
@instances.command('snapshot')
@click.option('--project', default=None,
    help="Create snapshots for all volumes")
def create_snapshots(project):
    "Snapshot EC2 instances"

    instances = filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
            print("Creating snapshot of {0}".format(v.id))
            v.create_snapshot(
                Description = "Created by snappy",
                DryRun = False
            )
    return

## INSTANCES LIST
@instances.command('list')
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def list_instances(project):
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
            tags.get('Project', '<no project>')
        )))

    return

## INSTANCES STOP
@instances.command('stop')
@click.option('--project', default=None,
    help="Only instances for project")
def stop_snapshots(project):
    "Stop EC2 instances"
    instances = filter_instances(project)

    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()

    return

## INSTANCES START
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
    cli()
