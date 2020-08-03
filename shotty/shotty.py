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
def cli():
    """Shotty manages snapshot and volumes"""

### volumes functions
@cli.group('volumes')
def volumes():
    """Commands for volumes"""

@volumes.command('list')
@click.option('--project', default=None,
    help="Only instances for project (tag project:<name>)")

def list_volumes(project):
    "List EC2 volumes"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
             print(",".join((
             v.id,
             i.id,
             v.state,
             str(v.size)+"GB",
             v.encrypted and "Encrypted" or "Not Encrypted"
             )))
    return

### snapshots functions
@cli.group('snapshots')
def snapshots():
    """Commands for snapshots"""

@snapshots.command('list')
@click.option('--project', default=None,
    help="Only instances for project (tag project:<name>)")

def list_snapshots(project):
    "List EC2 snapshots"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                 print(",".join((
                 s.id,
                 v.id,
                 i.id,
                 s.state,
                 s.progress,
                 s.start_time.strftime("%c")
                 )))
    return

### insatnces functions
@cli.group('instances')
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
    return

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
    return

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

@instances.command('snapshot')
@click.option('--project', default=None,
    help="Only instances for project (tag project:<name>)")

def create_snapshots(project):
    "Create snapshot for volumes of a gourp of instancs"

    instances = filter_instances(project)

    for i in instances:
        print ("stopping {0} for volume snapshots".format(i.id))
        i.stop()
        i.wait_until_stopped()

        for v in i.volumes.all():
            print ("Creating snapshot of {0} of {1}".format(v.id, i.id))
            v.create_snapshot(Description="Created by Snapshotalyzer")
        print ("starting {0} after volume snapshots".format(i.id))
        i.start()
        i.wait_until_running()
    return

if __name__ == '__main__':
    cli()
