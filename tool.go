package main

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

type ToolArgs struct {
	dockerComposeFile  string
	rancherComposeFile string
	komposeTool        string
	constructsMap      map[string]DocConstruct
}

type DocConstruct struct {
	Name     string `yaml:"name,omitempty"`
	DocLink  string `yaml:"doclink,omitempty"`
	HelpText string `yaml:"helptext,omitempty"`
	Special  bool   `yaml:"special,omitempty"`
}

type ComposeConfig struct {
	Version     string                   `yaml:"version,omitempty"`
	ServicesMap map[string]ServiceConfig `yaml:"services,omitempty"`
	Volumes     map[string]interface{}   `yaml:"volumes,omitempty"`
	Networks    map[string]interface{}   `yaml:"networks,omitempty"`
}

//ServiceConfig - defines only those keys in docker-compose.yml explicitly that we know that cannot be migrated
type ServiceConfig struct {
	Image               string                 `yaml:"image,omitempty"`
	CgroupParent        string                 `yaml:"cgroup_parent,omitempty"`
	Links               []string               `yaml:"links,omitempty"`
	ExternalLinks       []string               `yaml:"external_links,omitempty"`
	Ports               []string               `yaml:"ports,omitempty"`
	Expose              []string               `yaml:"expose,omitempty"`
	DeviceReadBps       []string               `yaml:"device_read_bps,omitempty"`
	DeviceReadIOps      []string               `yaml:"device_read_iops,omitempty"`
	Devices             []string               `yaml:"devices,omitempty"`
	DeviceWriteBps      []string               `yaml:"device_write_bps,omitempty"`
	DeviceWriteIOps     []string               `yaml:"device_write_iops,omitempty"`
	DependsOn           []string               `yaml:"depends_on,omitempty"`
	DNS                 []string               `yaml:"dns,omitempty"`
	DNSOpt              []string               `yaml:"dns_opt,omitempty"`
	DNSSearch           []string               `yaml:"dns_search,omitempty"`
	DrainTimeoutMs      string                 `yaml:"drain_timeout_ms,omitempty"`
	Volumes             map[string]interface{} `yaml:"volumes,omitempty"`
	VolumesFrom         []string               `yaml:"volumes_from,omitempty"`
	VolumeDriver        string                 `yaml:"volume_driver,omitempty"`
	Networks            map[string]interface{} `yaml:"networks,omitempty"`
	NetworkMode         string                 `yaml:"network_mode,omitempty"`
	Labels              map[string]string      `yaml:"labels,omitempty"`
	Isolation           string                 `yaml:"isolation,omitempty"`
	Sysctls             map[string]string      `yaml:"sysctls,omitempty"`
	Secrets             map[string]interface{} `yaml:"secrets,omitempty"`
	SecurityOpt         []string               `yaml:"security_opt,omitempty"`
	StopSignal          string                 `yaml:"stop_signal,omitempty"`
	Ulimits             map[string]interface{} `yaml:"ulimits,omitempty"`
	MemLimit            string                 `yaml:"mem_limit,omitempty"`
	MemReservation      string                 `yaml:"mem_reservation,omitempty"`
	MemSwapLimit        string                 `yaml:"memswap_limit,omitempty"`
	MemSwappiness       string                 `yaml:"mem_swappiness,omitempty"`
	MilliCPUReservation string                 `yaml:"milli_cpu_reservation,omitempty"`
}

type RancherComposeConfig struct {
	Version     string                   `yaml:"version,omitempty"`
	ServicesMap map[string]RancherConfig `yaml:"services,omitempty"`
}

//RancherConfig define only those keys in rancher-compose.yml that we know that cannot be migrated
type RancherConfig struct {
	LbConfig        map[string]interface{} `yaml:"lb_config"`
	DefaultCert     string                 `yaml:"default_cert,omitempty"`
	Certs           []string               `yaml:"certs,omitempty"`
	Type            string                 `yaml:"type,omitempty"`
	Scale           string                 `yaml:"scale,omitempty"`
	RetainIP        bool                   `yaml:"retain_ip,omitempty"`
	StartOnCreate   bool                   `yaml:"start_on_create,omitempty"`
	DrainTimeoutMs  string                 `yaml:"drain_timeout_ms,omitempty"`
	ExternalIps     []string               `yaml:"external_ips,omitempty"`
	HealthCheck     map[string]interface{} `yaml:"health_check,omitempty"`
	Metadata        map[string]interface{} `yaml:"metadata,omitempty"`
	ScalePolicy     map[string]interface{} `yaml:"scale_policy,omitempty"`
	ServiceSchemas  map[string]interface{} `yaml:"service_schemas,omitempty"`
	UpgradeStrategy map[string]interface{} `yaml:"upgrade_strategy,omitempty"`
	StorageDriver   map[string]interface{} `yaml:"storage_driver,omitempty"`
	NetworkDriver   map[string]interface{} `yaml:"network_driver,omitempty"`
}

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
	output, err := os.Create("output.txt")
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
