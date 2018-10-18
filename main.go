package main

import (
	"os"

	cmd "github.com/rancher/migration-tools/cmd"
	log "github.com/sirupsen/logrus"
	"github.com/urfave/cli"
)

var VERSION string

func main() {
	app := cli.NewApp()
	app.Name = "Rancher 1.6 to Rancher 2.0 migration-helper"
	app.Author = "Rancher Labs, Inc."
	app.Usage = "Please check the options using --help flag"

	if VERSION == "" {
		app.Version = "git"
	} else {
		app.Version = VERSION
	}

	app.Flags = []cli.Flag{
		cli.BoolFlag{
			Name:  "debug",
			Usage: "debug logging",
		},
		cli.StringFlag{
			Name:  "log",
			Usage: "path to log to",
			Value: "",
		},
	}

	app.Before = beforeApp
	app.Commands = []cli.Command{
		cmd.ExportCommand(),
		cmd.ParseCommand(),
	}

	app.Run(os.Args)
}

func beforeApp(c *cli.Context) error {
	timeFormat := new(log.TextFormatter)
	timeFormat.TimestampFormat = "2006-01-02 15:04:05"
	timeFormat.FullTimestamp = true
	log.SetFormatter(timeFormat)

	if c.Bool("debug") {
		log.SetLevel(log.DebugLevel)
	}

	return nil
}
