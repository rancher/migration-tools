package cmd

import (
	"fmt"
	"os"

	log "github.com/sirupsen/logrus"
	"github.com/urfave/cli"
)

func ParseCommand() cli.Command {
	return cli.Command{
		Name:   "parse",
		Usage:  "Parse docker-compose and rancher-compose files to get k8s manifests",
		Action: ParseTool,
		Flags: []cli.Flag{
			cli.StringFlag{
				Name:  "docker-file",
				Usage: "Docker compose file to parse to get k8s manifest",
				Value: "docker-compose.yml",
			},
			cli.StringFlag{
				Name:  "output-file",
				Usage: "Output file where to write checks and advices for conversion",
				Value: "output.txt",
			},
			cli.StringFlag{
				Name:  "rancher-file",
				Usage: "Rancher compose file to parse to get k8s manifest",
				Value: "rancher-compose.yml",
			},
		},
	}
}

func ParseTool(c *cli.Context) error {
	log.Info("---Starting migration helper tool parse command---")

	t, err := validateParseFlags(c)
	if err != nil {
		return err
	}

	err = runParser(t)
	if err != nil {
		return fmt.Errorf("[ERROR] Parsing docker compose files: %v", err)
	}

	runKompose(t)

	return nil
}

func validateParseFlags(c *cli.Context) (*ToolArgs, error) {
	log.Debugf("Validating flags")

	t := &ToolArgs{
		dockerComposeFile:  c.String("docker-file"),
		outputFile:         c.String("output-file"),
		rancherComposeFile: c.String("rancher-file"),
	}

	err := validateDockerCompose(t)
	if err != nil {
		return nil, err
	}

	err = validateRancherCompose(t)
	if err != nil {
		return nil, err
	}

	err = setupConstructsMap(t)
	if err != nil {
		return nil, err
	}

	return t, nil
}

func validateDockerCompose(t *ToolArgs) error {
	log.Debugf("Validating docker compose file")

	_, err := os.Stat(t.dockerComposeFile)
	if err != nil {
		return fmt.Errorf("[ERROR] Validating docker compose file '%s': %v", t.dockerComposeFile, err)
	}

	return nil
}

func validateRancherCompose(t *ToolArgs) error {
	log.Debugf("Validating rancher compose file")

	_, err := os.Stat(t.rancherComposeFile)
	if err != nil {
		if os.IsNotExist(err) {
			t.rancherComposeFile = ""
			log.Debugf("Rancher compose file doesn't exist, just docker compose file will be parsed.")
			return nil
		}
		return fmt.Errorf("[ERROR] Validating rancher compose file '%s': %v", t.rancherComposeFile, err)
	}

	return nil
}
