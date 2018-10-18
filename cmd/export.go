package cmd

import (
	"fmt"

	rancher "github.com/rancher/go-rancher/v2"
	log "github.com/sirupsen/logrus"
	"github.com/urfave/cli"
)

const (
	warnMessage = `Some Rancher v1.x organizational concepts have changed in racher v2.x:

- environments -> projects
- stacks -> namespaces 
- services -> workloads

To maintain same organization boundaries on rancher v2.x, is recommended to:

- create a separated project for every rancher v1.x environment.
- create a separated namespace for every rancher v1.x stack.

`
)

func ExportCommand() cli.Command {
	return cli.Command{
		Name:   "export",
		Usage:  "Export compose files for every stack running on cattle environment on a Rancher v1.6 system",
		Action: exportTool,
		Flags: []cli.Flag{
			cli.StringFlag{
				Name:   "url",
				Usage:  "Rancher API endpoint URL",
				EnvVar: "RANCHER_URL",
			},
			cli.StringFlag{
				Name:   "access-key",
				Usage:  "Rancher API access key. Using admin API key will export stacks on all cattle environments",
				EnvVar: "RANCHER_ACCESS_KEY",
			},
			cli.StringFlag{
				Name:   "secret-key",
				Usage:  "Rancher API secret key",
				EnvVar: "RANCHER_SECRET_KEY",
			},
			cli.StringFlag{
				Name:  "export-dir",
				Usage: "Base directory under which compose files will be exported under sub-directories created for every env/stack",
				Value: "export",
			},
			cli.BoolFlag{
				Name:  "all,a",
				Usage: "Export all stacks. Using this flag stacks with inactive, stopped and removing state, will also be exported",
			},
			cli.BoolFlag{
				Name:  "system,s",
				Usage: "Export system and infrastructure stacks",
			},
		},
	}
}

func exportTool(ctx *cli.Context) error {
	log.Info("---Starting migration helper tool export command---")

	opts, err := validateExportFlags(ctx)
	if err != nil {
		return err
	}

	log.Debugf("Connecting to Rancher server %s", opts.Url)
	client, err := rancher.NewRancherClient(opts)
	if err != nil {
		return fmt.Errorf("[ERROR] Connecting to Rancher server %s: %v", opts.Url, err)
	}

	log.Debugf("Getting stacks list")
	col, err := client.Stack.List(defaultListOpts(ctx))
	if err != nil {
		return fmt.Errorf("[ERROR] Getting stacks list: %v", err)
	}

	colData := col.Data

	for {
		col, _ = col.Next()
		if col == nil {
			break
		}
		colData = append(colData, col.Data...)
		if !col.Pagination.Partial {
			break
		}
	}

	projectMap := make(map[string]string)

	count := map[string]int{
		"project": 0,
		"stack":   0,
	}

	log.Debugf("Getting stacks compose files")
	for _, item := range colData {
		if projectMap[item.AccountId] == "" {
			log.Debugf("Getting project ID %s for stack %s", item.AccountId, item.Name)
			project, err := client.Project.ById(item.AccountId)
			if err != nil {
				return fmt.Errorf("[ERROR] Getting project ID %s: %v", item.AccountId, err)
			}

			if project.Orchestration == "cattle" {
				projectMap[item.AccountId] = project.Name
				count["project"]++
			} else {
				projectMap[item.AccountId] = "-"
			}
		}

		// Continue if project orchestrator is nor cattle or docker-compose is empty
		if projectMap[item.AccountId] == "-" || item.DockerCompose == "" {
			continue
		}

		count["stack"]++

		// Get compose config for the stack
		log.Debugf("Getting compose config for stack %s", item.Name)
		composeInput := &rancher.ComposeConfigInput{
			ServiceIds: item.ServiceIds,
		}
		composeConfig, err := client.Stack.ActionExportconfig(&item, composeInput)
		if err != nil {
			return fmt.Errorf("[ERROR] Getting compose config for stack %s: %v", item.Name, err)
		}

		// Create export dir like export-dir/environment/stack
		path := ctx.String("export-dir") + "/" + projectMap[item.AccountId] + "/" + item.Name
		log.Debugf("Creating export dir %s for stack %s", path, item.Name)
		err = CreateDir(path)
		if err != nil {
			return fmt.Errorf("[ERROR] Creating export dir %s: %v", path, err)
		}
		// Saves docker-compose file
		log.Debugf("Saving docker compose file %s/docker-compose.yml for stack %s", path, item.Name)
		err = SaveFile(path+"/docker-compose.yml", []byte(composeConfig.DockerComposeConfig))
		if err != nil {
			return fmt.Errorf("[ERROR] Saving docker compose file %s/docker-compose.yml: %v", path, err)
		}
		//Save rancker-compose file
		log.Debugf("Saving rancher compose file %s/rancher-compose.yml for stack %s", path, item.Name)
		err = SaveFile(path+"/rancher-compose.yml", []byte(composeConfig.RancherComposeConfig))
		if err != nil {
			return fmt.Errorf("[ERROR] Saving rancher compose file %s/rancher-compose.yml: %v", path, err)
		}
		//Save README.md file with advice message
		log.Debugf("Saving readme file %s/README.md for stack %s", path, item.Name)
		message := warnMessage + "Project: " + projectMap[item.AccountId] + "\n"
		message = message + "Namespace: " + item.Name + "\n"
		err = SaveFile(path+"/README.md", []byte(message))
		if err != nil {
			return fmt.Errorf("[ERROR] Saving readme file %s/README.md : %v", path, err)
		}
	}

	log.Infof("---Exported docker compose files for %d stacks from %d environment(s) on %s directory---", count["stack"], count["project"], ctx.String("export-dir"))
	log.Infof("---Please check README.md file for Rancher 1.6 to Rancher 2.x organizational changes---")

	return nil
}

func validateExportFlags(ctx *cli.Context) (*rancher.ClientOpts, error) {
	log.Debugf("Validating flags")

	if ctx.String("url") == "" || ctx.String("access-key") == "" || ctx.String("secret-key") == "" {
		return nil, fmt.Errorf("[ERROR] url, access-key and secret-key must be provided")
	}

	ok, err := IsDirEmpty(ctx.String("export-dir"))
	if err != nil {
		return nil, fmt.Errorf("[ERROR] Accessing output directory %s: %v", ctx.String("export-dir"), err)
	}
	if !ok {
		return nil, fmt.Errorf("[ERROR] Output dir %s is not empty", ctx.String("export-dir"))
	}

	opts := &rancher.ClientOpts{
		Url:       ctx.String("url"),
		AccessKey: ctx.String("access-key"),
		SecretKey: ctx.String("secret-key"),
	}

	return opts, nil
}

func defaultListOpts(ctx *cli.Context) *rancher.ListOpts {
	listOpts := &rancher.ListOpts{
		Filters: map[string]interface{}{
			"limit":  -2,
			"all":    true,
			"system": false,
		},
	}

	if ctx == nil {
		return listOpts
	}

	if !ctx.Bool("all") {
		listOpts.Filters["removed_null"] = "1"
		listOpts.Filters["state_ne"] = []string{
			"inactive",
			"stopped",
			"removing",
		}
		listOpts.Filters["all"] = false
	}

	if ctx.Bool("system") {
		listOpts.Filters["system"] = true
	}

	return listOpts
}
