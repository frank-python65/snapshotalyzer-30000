#import sys
import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

def filter_instances(project):
    instance = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    return instances

@click.group()
def instances():
    """Commands for instances"""

@instances.command('list')
@click.option('--project', default=None,
    help="Only instances for project (tag project:<name>)")

def list_insatnces(project):
    "List EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        tags = {t['Key'] : t['Value'] for t in (i.tags or []) }
        print(','.join((
        i.id,
        tags.get('Project', '<no project>'),
        i.instance_type,
        i.placement['AvailabilityZone'],
        i.state['Name'],
        i.public_dns_name
        )))

@instances.command('stop')
@click.option('--project', default=None,
    help="Only instances for project (tag project:<name>)")

def stop_insatnces(project):
    "Stop EC2 instances"

    instances = filter_instances(project)

    for i in instances:
#        tags = {t['Key'] : t['Value'] for t in (i.tags or []) }
#        project = tags.get('Project', '<no project>')
        print ("stopping {0} - {1}...".format(project,i.id))
        i.stop()


@instances.command('start')
@click.option('--project', default=None,
    help="Only instances for project (tag project:<name>)")

def start_insatnces(project):
    "Start EC2 instances"

    instances = filter_instances(project)

    for i in instances:
#        tags = {t['Key'] : t['Value'] for t in (i.tags or []) }
#        project = tags.get('Project', '<no project>')
        print ("starting {0} - {1}...".format(project,i.id))
        i.start()

    return

if __name__ == '__main__':
    instances()
