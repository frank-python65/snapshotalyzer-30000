# snapshotalyzer-30000

Demo project to manage AWS ECS snapshots

## About

This is a demo project to manage AWS ECS snapshots

## Configuring

shotty uses the configiuration created via AWS cli etc.

'aws configure --profile shotty'

## running

'pipenv run "python shotty\shotty.py <command> <subcommand> <--project=PROJECT>"'


<command> <subcommand> is one of
  - instances [list | start | stopping]
  - volumes [list]
  - snapshots [list\]
<Project> is optional

### --help
  - Top command has help for all Commands
  - Each command has its help
