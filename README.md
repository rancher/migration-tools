migration-tools
========

This tool is to help migration efforts of apps running on Rancher 1.6 to Rancher 2.0.

This tool will:
- Export docker compose config files [docker-compose.yml and rancher-compose.yml] for every stack running on cattle environments on existing Rancher v1.6 system.
- Parse docker compose config files and output a list of constructs present in the config file that cannot be supported onto Rancher 2.0 without special handling or that cannot be converted to Kubernetes YAML using [Kompose tool](https://github.com/kubernetes/kompose) tool.

This should help users to export all docker compose config files, parse them and run a quick check to see if their application running on Rancher 1.6 can be migrated to 2.0 and what is lacking to do the migration.

**Usage**

```
# migration-tools -h
NAME:
   Rancher 1.6 to Rancher 2.0 migration-helper - Please check the options using --help flag

USAGE:
   migration-tools [global options] command [command options] [arguments...]

VERSION:
   git

AUTHOR:
   Rancher Labs, Inc.

COMMANDS:
     export   Export compose files for every stack running on cattle environment on a Rancher v1.6 system
     parse    Parse docker-compose and rancher-compose files to get k8s manifests
     help, h  Shows a list of commands or help for one command

GLOBAL OPTIONS:
   --debug        debug logging
   --log value    path to log to
   --help, -h     show help
   --version, -v  print the version
```

```
# migration-tools export -h
NAME:
   migration-tools export - Export compose files for every stack running on cattle environment on a Rancher v1.6 system

USAGE:
   migration-tools export [command options] [arguments...]

OPTIONS:
   --url value         Rancher API endpoint URL [$RANCHER_URL]
   --access-key value  Rancher API access key. Using admin API key will export stacks on all cattle environments [$RANCHER_ACCESS_KEY]
   --secret-key value  Rancher API secret key [$RANCHER_SECRET_KEY]
   --export-dir value  Base directory under which compose files will be exported under sub-directories created for every env/stack (default: "export")
   --all, -a           Export all stacks. Using this flag stacks with inactive, stopped and removing state, will also be exported
   --system, -s        Export system and infrastructure stacks
```

```
# migration-tools parse -h
NAME:
   migration-tools parse - Parse docker-compose and rancher-compose files to get k8s manifests

USAGE:
   migration-tools parse [command options] [arguments...]

OPTIONS:
   --docker-file value   Docker compose file to parse to get k8s manifest (default: "docker-compose.yml")
   --output-file value   Output file where to write checks and advices for conversion (default: "output.txt")
   --rancher-file value  Rancher compose file to parse to get k8s manifest (default: "rancher-compose.yml")
```

**Output**

* export
    - compose files
        This command will connect to Rancher 1.6 system and generate docker-compose and rancher-compose files for every stack running on cattle environment. For every stack, files are exported in `<export-dir>/<env_name>/<stack_name>` folder.
* parse
    - output.txt
		This command will generate `output.txt` file to list all constructs for each service in your docker-compose.yml file that will need to be handled specially to sucessfully migrate them to Rancher 2.0.
    - Kubernetes YAML specs
		This command also invokes the [Kompose tool](https://github.com/kubernetes/kompose) that generates some Kubernetes YAML specs for the services to get started with migration.


## Building

`scripts/build`

* Linux: Binary generated under `bin/`
  `make`

* Linux, darwin and windows: Binaries generated under `build/bin/`
  `CROSS=1 make build`.

## Running

`./bin/migration-tools`

## License
Copyright (c) 2018 [Rancher Labs, Inc.](http://rancher.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
