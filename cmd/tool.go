package cmd

import (
	"html/template"
	"io/ioutil"
	"os"
	"reflect"
	"strings"

	"fmt"

	"github.com/kubernetes/kompose/pkg/app"
	"github.com/kubernetes/kompose/pkg/kobject"
	"github.com/sirupsen/logrus"
	"gopkg.in/yaml.v2"
)

func runParser(t *ToolArgs) error {
	composeConfig, err := readDockerCompose(t)
	if err != nil {
		return err
	}

	rancherComposeConfig, err := readRancherCompose(t)
	if err != nil {
		return err
	}
	//iterate over all services in dockerConfig and check in rancherConfig for this service
	var serviceConstructs = make(map[string]map[string][]DocConstruct)

	for service, config := range composeConfig.ServicesMap {
		constructsOut := make(map[string][]DocConstruct)

		reflectedConfig := reflect.ValueOf(config)
		lookForDocumentedConstructs(reflectedConfig, t.constructsMap, constructsOut)

		//load the corresponding rancher_compose service
		if rancherComposeConfig != nil {
			rancherConfig := rancherComposeConfig.ServicesMap[service]
			reflectedConfig = reflect.ValueOf(rancherConfig)
			lookForDocumentedConstructs(reflectedConfig, t.constructsMap, constructsOut)
		}

		if len(constructsOut) != 0 {
			serviceConstructs[service] = constructsOut
		}
	}

	//check for other top-level constructs
	var usesNetworks, usesVolumes bool
	if composeConfig.Volumes != nil && len(composeConfig.Volumes) != 0 {
		usesVolumes = true
	}
	if composeConfig.Networks != nil && len(composeConfig.Networks) != 0 {
		usesNetworks = true
	}

	//create the output file
	output, err := os.Create(t.outputFile)
	if err != nil {
		return fmt.Errorf("Error creating the output file, quit")
	}
	defer output.Close()

	data := map[string]interface{}{
		"serviceConstructs": serviceConstructs,
		"usesNetworks":      usesNetworks,
		"usesVolumes":       usesVolumes,
	}
	outputTemplate := template.Must(template.New("output_template").Parse(outputTemplate))
	if err := outputTemplate.Execute(output, data); err != nil {
		return fmt.Errorf("Error writing the output template to file: %v", err)
	}

	logrus.Infof("---Please check the output.txt file for list of Docker/Rancher 1.6 constructs needing special handling---")

	return nil
}

func lookForDocumentedConstructs(reflectedConfig reflect.Value, inputConstructsMap map[string]DocConstruct, constructsOut map[string][]DocConstruct) {
	for key, doc := range inputConstructsMap {
		f := reflectedConfig.FieldByName(key)
		if f.IsValid() && !isEmpty(f) {
			if doc.Special {
				outDoc := handleSpecialConstruct(key, f)
				constructsOut[doc.Name] = append(constructsOut[doc.Name], outDoc...)
			} else {
				constructsOut[doc.Name] = append(constructsOut[doc.Name], doc)
			}
		}
	}
}

func isEmpty(reflectedField reflect.Value) bool {
	fieldType := reflectedField.Type()
	switch fieldType.Name() {
	case "string":
		return reflectedField.Interface().(string) == ""
	case "bool":
		return false
	default:
		return reflectedField.IsNil()
	}

}

func handleSpecialConstruct(key string, reflectedField reflect.Value) []DocConstruct {

	var outDoc []DocConstruct

	switch key {
	case "Labels":
		labels, ok := reflectedField.Interface().(map[string]string)
		if !ok {
			logrus.Infof("\n--- Error reading labels from compose config file")
			return outDoc
		}
		if labels != nil && len(labels) != 0 {
			for labelKey := range labels {
				if strings.HasPrefix(labelKey, "io.rancher.scheduler") {
					doc := DocConstruct{
						Name:     labelKey,
						DocLink:  "https://rancher.com/blog/2018/2018-08-29-scheduling-options-in-2-dot-0/",
						HelpText: "Please refer to the scheduling options in Rancher 2.0 to migrate this functionality",
					}
					outDoc = append(outDoc, doc)
				} else {
					doc := DocConstruct{
						Name: labelKey,
					}
					outDoc = append(outDoc, doc)
				}
			}
		}
	}

	return outDoc
}

func readDockerCompose(t *ToolArgs) (*ComposeConfig, error) {
	dcBytes, err := ioutil.ReadFile(t.dockerComposeFile)
	if err != nil {
		return nil, fmt.Errorf("Failed to read file %v, error: %v ", t.dockerComposeFile, err)
	}

	dockerConfig := &ComposeConfig{}

	err = yaml.Unmarshal(dcBytes, &dockerConfig)
	if err != nil {
		return nil, fmt.Errorf("Failed to parse the docker-compose yaml file, error: %v", err)
	}

	return dockerConfig, nil
}

func readRancherCompose(t *ToolArgs) (*RancherComposeConfig, error) {
	if t.rancherComposeFile == "" {
		return nil, nil
	}
	dcBytes, err := ioutil.ReadFile(t.rancherComposeFile)
	if err != nil {
		return nil, fmt.Errorf("Failed to read file %v, error: %v ", t.rancherComposeFile, err)
	}

	rancherConfig := &RancherComposeConfig{}

	err = yaml.Unmarshal(dcBytes, &rancherConfig)
	if err != nil {
		return nil, fmt.Errorf("Failed to parse the rancher-compose yaml file, error: %v", err)
	}
	return rancherConfig, nil
}

func runKompose(t *ToolArgs) {
	logrus.Infof("---Running Kompose tool on the docker-compose.yml---")
	ConvertOpt := kobject.ConvertOptions{
		ToStdout:     false,
		Provider:     "kubernetes",
		GenerateYaml: true,
		InputFiles:   []string{t.dockerComposeFile},
	}

	app.Convert(ConvertOpt)
	logrus.Infof("---Kompose has created the Kubernetes YAML files for your 1.6 services---")
}

func setupConstructsMap(t *ToolArgs) error {
	logrus.Debugf("Setting construct map")

	t.constructsMap = make(map[string]DocConstruct)
	err := yaml.Unmarshal([]byte(documentedConstructs), &t.constructsMap)
	if err != nil {
		return fmt.Errorf("Failed to parse the constructs input file, error: %v", err)
	}
	return nil
}
