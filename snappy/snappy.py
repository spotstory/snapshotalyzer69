import boto3
import click

session = boto3.Session(profile_name='snappy')
ec2 = session.resource('ec2')

def find_key(instance, tag_name):
    for i in instance.tags:
        if i['Key'] == 'Project':
            return i['Key'] + "=" + i['Value']

@click.command()
def list_snapshots():
    "List EC2 instances"
    for i in ec2.instances.all():
        project_name = find_key(i, "Project")
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            project_name)))

    return

if __name__ == '__main__':
    list_snapshots()
