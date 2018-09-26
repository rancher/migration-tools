package main

import (
	"os"

	"github.com/sirupsen/logrus"

	"github.com/urfave/cli"
)

var VERSION = "v0.0.0-dev"

func main() {
	app := cli.NewApp()
	app.Name = "Rancher 1.6 to Rancher 2.0 migration-helper"
	app.Version = VERSION
	app.Usage = "Please check the options using --help flag"
	app.Action = func(c *cli.Context) error {
		StartTool(c)
		return nil
	}
	app.Flags = []cli.Flag{
		cli.StringFlag{
			Name:  "docker-file",
			Usage: "An absolute path to an alternate Docker compose file (default: docker-compose.yml)",
			Value: "docker-compose.yml",
		},
		cli.StringFlag{
			Name:  "rancher-file",
			Usage: "An absolute path to an alternate Rancher compose file (default: rancher-compose.yml)",
			Value: "rancher-compose.yml",
		},
	}

	app.Run(os.Args)
}

func StartTool(c *cli.Context) {
	if c.GlobalBool("debug") {
		logrus.SetLevel(logrus.DebugLevel)
	}
	textFormatter := &logrus.TextFormatter{
		FullTimestamp: true,
	}
	logrus.SetFormatter(textFormatter)

	logrus.Info("---Starting migration helper tool---")

	t := &ToolArgs{}

	validateFlags(c, t)

	err := setupConstructsMap(t)
	if err != nil {
		logrus.Fatalf("Failed to parse the constructs input file, error: %v", err)
	}

	err = runParser(t)
	if err != nil {
		logrus.Fatalf("Failed parsing the compose files, error: %v", err)
	}

	runKompose(t)

}

func beforeApp(c *cli.Context) error {
	if c.GlobalBool("verbose") {
		logrus.SetLevel(logrus.DebugLevel)
	}
	return nil
}

func validateFlags(c *cli.Context, t *ToolArgs) {
	t.dockerComposeFile = c.GlobalString("docker-file")
	validateDefaultCompose(t)

	t.rancherComposeFile = c.GlobalString("rancher-file")
	if !isRancherComposePresent(t) {
		t.rancherComposeFile = ""
		logrus.Infof("rancher-compose.yml not found, will parse docker-compose.yml only.")
	}

	if c.IsSet("kompose-tool-path") {
		t.komposeTool = c.GlobalString("kompose-tool-path")
	}
}

func validateDefaultCompose(t *ToolArgs) {
	_, err := os.Stat(t.dockerComposeFile)
	if err != nil {
		logrus.Fatalf("'%s' not found: %v", t.dockerComposeFile, err)
	}
}

func isRancherComposePresent(t *ToolArgs) bool {
	_, err := os.Stat(t.rancherComposeFile)
	if err != nil {
		return false
	}
	return true
}
