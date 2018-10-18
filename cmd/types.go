package cmd

type ToolArgs struct {
	dockerComposeFile  string
	rancherComposeFile string
	komposeTool        string
	outputFile         string
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
	Volumes             []string               `yaml:"volumes,omitempty"`
	VolumesFrom         []string               `yaml:"volumes_from,omitempty"`
	VolumeDriver        string                 `yaml:"volume_driver,omitempty"`
	Networks            []string               `yaml:"networks,omitempty"`
	NetworkMode         string                 `yaml:"network_mode,omitempty"`
	Labels              map[string]string      `yaml:"labels,omitempty"`
	Isolation           string                 `yaml:"isolation,omitempty"`
	Sysctls             map[string]string      `yaml:"sysctls,omitempty"`
	Secrets             []string               `yaml:"secrets,omitempty"`
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
	RetainIP        string                 `yaml:"retain_ip,omitempty"`
	StartOnCreate   string                 `yaml:"start_on_create,omitempty"`
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
