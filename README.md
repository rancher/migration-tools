migration-tools
========

This tool is to help migration efforts of apps running on Rancher 1.6 to Rancher 2.0.
This tool will:
- Accept the Rancher 1.6 Docker Compose config files [docker-compose.yml and rancher-compose.yml]
- Output a list of constructs present in the config file that cannot be supported onto Rancher 2.0 without special handling or that cannot be converted to Kubernetes YAML using tools like Kompose.

This should help users to run a quick check to see if their application running on Rancher 1.6 can be migrated to 2.0 and what is lacking to do the migration.

**Usage**:

```migration-tools --docker-file <path to docker-compose.yml> --rancher-file <path to rancher-compose.yml if available>```

**Options**:

-   `--docker-file value`   An absolute path to an alternate Docker compose file (default: "docker-compose.yml")
-   `--rancher-file value`  An absolute path to an alternate Rancher compose file (default: "rancher-compose.yml")
-   `--help, -h`           show help
-   `--version, -v`        print the version

**Output**

- output.txt
		This tool will generate `output.txt` file to list all constructs for each service in your docker-compose.yml file that will need to be handled specially to sucessfully migrate them to Rancher 2.0.
- Kubernetes YAML specs
		This tool also invokes the [Kompose tool](https://github.com/kubernetes/kompose) that generates some Kubernetes YAML specs for the services to get started with migration.


## Building

`make`


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
