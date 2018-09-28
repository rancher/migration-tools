%if 0%{?fedora} || 0%{?rhel} == 6
# Not all devel deps exist in Fedora so you can't
# install the devel rpm so we need to build without
# devel or unit_test for now
# Generate devel rpm
%global with_devel 0
# Build project from bundled dependencies
%global with_bundled 1
# Build with debug info rpm
%global with_debug 1
# Run tests in check section
%global with_check 1
# Generate unit-test rpm
%global with_unit_test 0
%else
%global with_devel 0
%global with_bundled 1
%global with_debug 0
%global with_check 0
%global with_unit_test 0
%endif

# https://fedoraproject.org/wiki/PackagingDrafts/Go#Debuginfo
# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

# https://fedoraproject.org/wiki/PackagingDrafts/Go#Debuginfo
%if ! 0%{?gobuild:1}
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%endif

%global provider        github
%global provider_tld    com
%global project         kubernetes-incubator
%global repo            kompose
# https://github.com/kubernetes-incubator/kompose
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          135165b39c55d29a5426479ded81eddd56bfbaf4
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

# define ldflags, buildflags, testflags here. The ldflags/buildflags
# were taken from script/.build and the testflags were taken from
# script/test-unit. We will need to periodically check these for
# consistency.
%global ldflags "-w -X github.com/kubernetes-incubator/kompose/version.GITCOMMIT=%{shortcommit}"
%global buildflags %nil
%global testflags -race -cover -v

Name:           kompose
Version:        0.3.0
Release:        0.1.git%{shortcommit}%{?dist}
Summary:        Tool to move from `docker-compose` to Kubernetes
License:        ASL 2.0
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 aarch64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

# Main package BuildRequires
%if ! 0%{?with_bundled}
# Remaining dependencies not included in main packages
BuildRequires: golang(github.com/spf13/cobra)
BuildRequires: golang(k8s.io/kubernetes/pkg/runtime)
BuildRequires: golang(github.com/openshift/origin/pkg/build/api)
BuildRequires: golang(github.com/ghodss/yaml)
BuildRequires: golang(github.com/openshift/origin/pkg/deploy/cmd)
BuildRequires: golang(github.com/Sirupsen/logrus)
BuildRequires: golang(github.com/openshift/origin/pkg/route/api/install)
BuildRequires: golang(github.com/openshift/origin/pkg/deploy/api)
BuildRequires: golang(github.com/openshift/origin/pkg/image/api)
BuildRequires: golang(k8s.io/kubernetes/pkg/api/resource)
BuildRequires: golang(github.com/openshift/origin/pkg/client)
BuildRequires: golang(k8s.io/kubernetes/pkg/client/unversioned/clientcmd)
BuildRequires: golang(github.com/openshift/origin/pkg/deploy/api/install)
BuildRequires: golang(github.com/spf13/viper)
BuildRequires: golang(github.com/openshift/origin/pkg/route/api)
BuildRequires: golang(github.com/docker/libcompose/lookup)
BuildRequires: golang(github.com/docker/libcompose/yaml)
BuildRequires: golang(k8s.io/kubernetes/pkg/kubectl/cmd/util)
BuildRequires: golang(github.com/docker/libcompose/project)
BuildRequires: golang(github.com/fatih/structs)
BuildRequires: golang(k8s.io/kubernetes/pkg/apis/extensions/install)
BuildRequires: golang(k8s.io/kubernetes/pkg/api/install)
BuildRequires: golang(k8s.io/kubernetes/pkg/kubectl)
BuildRequires: golang(k8s.io/kubernetes/pkg/apis/extensions)
BuildRequires: golang(k8s.io/kubernetes/pkg/client/unversioned)
BuildRequires: golang(github.com/openshift/origin/pkg/image/api/install)
BuildRequires: golang(github.com/openshift/origin/pkg/build/api/install)
BuildRequires: golang(k8s.io/kubernetes/pkg/util/intstr)
BuildRequires: golang(k8s.io/kubernetes/pkg/api)
BuildRequires: golang(k8s.io/kubernetes/pkg/api/unversioned)
BuildRequires: golang(github.com/docker/libcompose/config)
BuildRequires: golang(github.com/openshift/origin/pkg/cmd/cli/config)
%endif

# Adding dependecy as `git`
Requires: git

# Main package Provides
%if 0%{?with_bundled}
Provides: bundled(golang(cloud.google.com/go/compute/metadata)) = %{version}-3b1ae45394a234c385be014e9a488f2bb6eef821
Provides: bundled(golang(cloud.google.com/go/internal)) = %{version}-3b1ae45394a234c385be014e9a488f2bb6eef821
Provides: bundled(golang(cloud.google.com/go/storage)) = %{version}-3b1ae45394a234c385be014e9a488f2bb6eef821
Provides: bundled(golang(github.com/beorn7/perks/quantile)) = %{version}-3ac7bf7a47d159a033b107610db8a1b6575507a4
Provides: bundled(golang(github.com/coreos/etcd/alarm)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/auth)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/auth/authpb)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/client)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/clientv3)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/compactor)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/discovery)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/embed)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/error)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/etcdserver)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/etcdserver/api)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/etcdserver/api/v2http)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/etcdserver/api/v2http/httptypes)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/etcdserver/api/v3rpc)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/etcdserver/api/v3rpc/rpctypes)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/etcdserver/auth)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/etcdserver/etcdserverpb)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/etcdserver/membership)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/etcdserver/stats)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/integration)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/lease)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/lease/leasehttp)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/lease/leasepb)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/mvcc)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/mvcc/backend)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/mvcc/mvccpb)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/pkg/adt)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/pkg/contention)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/pkg/cors)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/pkg/crc)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/pkg/fileutil)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/pkg/httputil)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/pkg/idutil)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/pkg/ioutil)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/pkg/logutil)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/pkg/netutil)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/pkg/osutil)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/pkg/pathutil)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/pkg/pbutil)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/pkg/runtime)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/pkg/schedule)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/pkg/testutil)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/pkg/tlsutil)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/pkg/transport)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/pkg/types)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/pkg/wait)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/proxy/grpcproxy)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/proxy/grpcproxy/cache)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/raft)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/raft/raftpb)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/rafthttp)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/snap)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/snap/snappb)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/store)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/version)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/wal)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/etcd/wal/walpb)) = %{version}-83347907774bf36cbb261c594a32fd7b0f5dd9f6
Provides: bundled(golang(github.com/coreos/go-oidc/http)) = %{version}-5cf2aa52da8c574d3aa4458f471ad6ae2240fe6b
Provides: bundled(golang(github.com/coreos/go-oidc/jose)) = %{version}-5cf2aa52da8c574d3aa4458f471ad6ae2240fe6b
Provides: bundled(golang(github.com/coreos/go-oidc/key)) = %{version}-5cf2aa52da8c574d3aa4458f471ad6ae2240fe6b
Provides: bundled(golang(github.com/coreos/go-oidc/oauth2)) = %{version}-5cf2aa52da8c574d3aa4458f471ad6ae2240fe6b
Provides: bundled(golang(github.com/coreos/go-oidc/oidc)) = %{version}-5cf2aa52da8c574d3aa4458f471ad6ae2240fe6b
Provides: bundled(golang(github.com/coreos/go-systemd/daemon)) = %{version}-4484981625c1a6a2ecb40a390fcb6a9bcfee76e3
Provides: bundled(golang(github.com/coreos/go-systemd/dbus)) = %{version}-4484981625c1a6a2ecb40a390fcb6a9bcfee76e3
Provides: bundled(golang(github.com/coreos/go-systemd/journal)) = %{version}-4484981625c1a6a2ecb40a390fcb6a9bcfee76e3
Provides: bundled(golang(github.com/coreos/go-systemd/unit)) = %{version}-4484981625c1a6a2ecb40a390fcb6a9bcfee76e3
Provides: bundled(golang(github.com/coreos/go-systemd/util)) = %{version}-4484981625c1a6a2ecb40a390fcb6a9bcfee76e3
Provides: bundled(golang(github.com/coreos/pkg/capnslog)) = %{version}-fa29b1d70f0beaddd4c7021607cc3c3be8ce94b8
Provides: bundled(golang(github.com/coreos/pkg/dlopen)) = %{version}-fa29b1d70f0beaddd4c7021607cc3c3be8ce94b8
Provides: bundled(golang(github.com/coreos/pkg/health)) = %{version}-fa29b1d70f0beaddd4c7021607cc3c3be8ce94b8
Provides: bundled(golang(github.com/coreos/pkg/httputil)) = %{version}-fa29b1d70f0beaddd4c7021607cc3c3be8ce94b8
Provides: bundled(golang(github.com/coreos/pkg/timeutil)) = %{version}-fa29b1d70f0beaddd4c7021607cc3c3be8ce94b8
Provides: bundled(golang(github.com/davecgh/go-spew/spew)) = %{version}-5215b55f46b2b919f50a1df0eaa5886afe4e3b3d
Provides: bundled(golang(github.com/docker/distribution/configuration)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/context)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/digest)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/health)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/health/checks)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/manifest)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/manifest/manifestlist)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/manifest/schema1)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/manifest/schema2)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/notifications)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/reference)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/api/errcode)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/api/v2)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/auth)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/auth/htpasswd)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/auth/token)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/client)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/client/auth)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/client/transport)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/handlers)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/middleware/registry)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/middleware/repository)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/proxy)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/proxy/scheduler)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/storage)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/storage/cache)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/storage/cache/memory)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/storage/cache/redis)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/storage/driver)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/storage/driver/azure)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/storage/driver/base)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/storage/driver/factory)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/storage/driver/filesystem)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/storage/driver/gcs)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/storage/driver/inmemory)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/storage/driver/middleware)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/storage/driver/middleware/cloudfront)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/storage/driver/s3-aws)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/registry/storage/driver/swift)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/uuid)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/distribution/version)) = %{version}-12acdf0a6c1e56d965ac6eb395d2bce687bf22fc
Provides: bundled(golang(github.com/docker/docker/api/types)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/api/types/blkiodev)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/api/types/container)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/api/types/filters)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/api/types/mount)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/api/types/network)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/api/types/registry)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/api/types/strslice)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/api/types/swarm)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/api/types/versions)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/opts)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/pkg/mount)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/pkg/signal)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/pkg/urlutil)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/docker/runconfig/opts)) = %{version}-601004e1a714d77d3a43e957b8ae8adbc867b280
Provides: bundled(golang(github.com/docker/engine-api/client)) = %{version}-dea108d3aa0c67d7162a3fd8aa65f38a430019fd
Provides: bundled(golang(github.com/docker/engine-api/client/transport)) = %{version}-dea108d3aa0c67d7162a3fd8aa65f38a430019fd
Provides: bundled(golang(github.com/docker/engine-api/client/transport/cancellable)) = %{version}-dea108d3aa0c67d7162a3fd8aa65f38a430019fd
Provides: bundled(golang(github.com/docker/engine-api/types)) = %{version}-dea108d3aa0c67d7162a3fd8aa65f38a430019fd
Provides: bundled(golang(github.com/docker/engine-api/types/blkiodev)) = %{version}-dea108d3aa0c67d7162a3fd8aa65f38a430019fd
Provides: bundled(golang(github.com/docker/engine-api/types/container)) = %{version}-dea108d3aa0c67d7162a3fd8aa65f38a430019fd
Provides: bundled(golang(github.com/docker/engine-api/types/filters)) = %{version}-dea108d3aa0c67d7162a3fd8aa65f38a430019fd
Provides: bundled(golang(github.com/docker/engine-api/types/network)) = %{version}-dea108d3aa0c67d7162a3fd8aa65f38a430019fd
Provides: bundled(golang(github.com/docker/engine-api/types/reference)) = %{version}-dea108d3aa0c67d7162a3fd8aa65f38a430019fd
Provides: bundled(golang(github.com/docker/engine-api/types/registry)) = %{version}-dea108d3aa0c67d7162a3fd8aa65f38a430019fd
Provides: bundled(golang(github.com/docker/engine-api/types/strslice)) = %{version}-dea108d3aa0c67d7162a3fd8aa65f38a430019fd
Provides: bundled(golang(github.com/docker/engine-api/types/time)) = %{version}-dea108d3aa0c67d7162a3fd8aa65f38a430019fd
Provides: bundled(golang(github.com/docker/engine-api/types/versions)) = %{version}-dea108d3aa0c67d7162a3fd8aa65f38a430019fd
Provides: bundled(golang(github.com/docker/go-connections/nat)) = %{version}-f549a9393d05688dff0992ef3efd8bbe6c628aeb
Provides: bundled(golang(github.com/docker/go-connections/sockets)) = %{version}-f549a9393d05688dff0992ef3efd8bbe6c628aeb
Provides: bundled(golang(github.com/docker/go-connections/tlsconfig)) = %{version}-f549a9393d05688dff0992ef3efd8bbe6c628aeb
Provides: bundled(golang(github.com/docker/libcompose/config)) = %{version}-1c4bd4542afb20db0b51afd71d9ebceaf206e2dd
Provides: bundled(golang(github.com/docker/libcompose/logger)) = %{version}-1c4bd4542afb20db0b51afd71d9ebceaf206e2dd
Provides: bundled(golang(github.com/docker/libcompose/lookup)) = %{version}-1c4bd4542afb20db0b51afd71d9ebceaf206e2dd
Provides: bundled(golang(github.com/docker/libcompose/project)) = %{version}-1c4bd4542afb20db0b51afd71d9ebceaf206e2dd
Provides: bundled(golang(github.com/docker/libcompose/project/events)) = %{version}-1c4bd4542afb20db0b51afd71d9ebceaf206e2dd
Provides: bundled(golang(github.com/docker/libcompose/project/options)) = %{version}-1c4bd4542afb20db0b51afd71d9ebceaf206e2dd
Provides: bundled(golang(github.com/docker/libcompose/utils)) = %{version}-1c4bd4542afb20db0b51afd71d9ebceaf206e2dd
Provides: bundled(golang(github.com/docker/libcompose/yaml)) = %{version}-1c4bd4542afb20db0b51afd71d9ebceaf206e2dd
Provides: bundled(golang(github.com/emicklei/go-restful/log)) = %{version}-89ef8af493ab468a45a42bb0d89a06fccdd2fb22
Provides: bundled(golang(github.com/emicklei/go-restful/swagger)) = %{version}-89ef8af493ab468a45a42bb0d89a06fccdd2fb22
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/Sirupsen/logrus)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/docker/docker/opts)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/docker/docker/pkg/archive)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/docker/docker/pkg/fileutils)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/docker/docker/pkg/homedir)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/docker/docker/pkg/idtools)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/docker/docker/pkg/ioutils)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/docker/docker/pkg/longpath)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/docker/docker/pkg/pools)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/docker/docker/pkg/promise)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/docker/docker/pkg/stdcopy)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/docker/docker/pkg/system)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/docker/go-units)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/hashicorp/go-cleanhttp)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/github.com/opencontainers/runc/libcontainer/user)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/golang.org/x/net/context)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/fsouza/go-dockerclient/external/golang.org/x/sys/unix)) = %{version}-bf97c77db7c945cbcdbf09d56c6f87a66f54537b
Provides: bundled(golang(github.com/gogo/protobuf/gogoproto)) = %{version}-e18d7aa8f8c624c915db340349aad4c49b10d173
Provides: bundled(golang(github.com/gogo/protobuf/plugin/compare)) = %{version}-e18d7aa8f8c624c915db340349aad4c49b10d173
Provides: bundled(golang(github.com/gogo/protobuf/plugin/defaultcheck)) = %{version}-e18d7aa8f8c624c915db340349aad4c49b10d173
Provides: bundled(golang(github.com/gogo/protobuf/plugin/description)) = %{version}-e18d7aa8f8c624c915db340349aad4c49b10d173
Provides: bundled(golang(github.com/gogo/protobuf/plugin/embedcheck)) = %{version}-e18d7aa8f8c624c915db340349aad4c49b10d173
Provides: bundled(golang(github.com/gogo/protobuf/plugin/enumstringer)) = %{version}-e18d7aa8f8c624c915db340349aad4c49b10d173
Provides: bundled(golang(github.com/gogo/protobuf/plugin/equal)) = %{version}-e18d7aa8f8c624c915db340349aad4c49b10d173
Provides: bundled(golang(github.com/gogo/protobuf/plugin/face)) = %{version}-e18d7aa8f8c624c915db340349aad4c49b10d173
Provides: bundled(golang(github.com/gogo/protobuf/plugin/gostring)) = %{version}-e18d7aa8f8c624c915db340349aad4c49b10d173
Provides: bundled(golang(github.com/gogo/protobuf/plugin/marshalto)) = %{version}-e18d7aa8f8c624c915db340349aad4c49b10d173
Provides: bundled(golang(github.com/gogo/protobuf/plugin/oneofcheck)) = %{version}-e18d7aa8f8c624c915db340349aad4c49b10d173
Provides: bundled(golang(github.com/gogo/protobuf/plugin/populate)) = %{version}-e18d7aa8f8c624c915db340349aad4c49b10d173
Provides: bundled(golang(github.com/gogo/protobuf/plugin/size)) = %{version}-e18d7aa8f8c624c915db340349aad4c49b10d173
Provides: bundled(golang(github.com/gogo/protobuf/plugin/stringer)) = %{version}-e18d7aa8f8c624c915db340349aad4c49b10d173
Provides: bundled(golang(github.com/gogo/protobuf/plugin/testgen)) = %{version}-e18d7aa8f8c624c915db340349aad4c49b10d173
Provides: bundled(golang(github.com/gogo/protobuf/plugin/union)) = %{version}-e18d7aa8f8c624c915db340349aad4c49b10d173
Provides: bundled(golang(github.com/gogo/protobuf/plugin/unmarshal)) = %{version}-e18d7aa8f8c624c915db340349aad4c49b10d173
Provides: bundled(golang(github.com/gogo/protobuf/proto)) = %{version}-e18d7aa8f8c624c915db340349aad4c49b10d173
Provides: bundled(golang(github.com/gogo/protobuf/protoc-gen-gogo/descriptor)) = %{version}-e18d7aa8f8c624c915db340349aad4c49b10d173
Provides: bundled(golang(github.com/gogo/protobuf/protoc-gen-gogo/generator)) = %{version}-e18d7aa8f8c624c915db340349aad4c49b10d173
Provides: bundled(golang(github.com/gogo/protobuf/protoc-gen-gogo/grpc)) = %{version}-e18d7aa8f8c624c915db340349aad4c49b10d173
Provides: bundled(golang(github.com/gogo/protobuf/protoc-gen-gogo/plugin)) = %{version}-e18d7aa8f8c624c915db340349aad4c49b10d173
Provides: bundled(golang(github.com/gogo/protobuf/sortkeys)) = %{version}-e18d7aa8f8c624c915db340349aad4c49b10d173
Provides: bundled(golang(github.com/gogo/protobuf/vanity)) = %{version}-e18d7aa8f8c624c915db340349aad4c49b10d173
Provides: bundled(golang(github.com/gogo/protobuf/vanity/command)) = %{version}-e18d7aa8f8c624c915db340349aad4c49b10d173
Provides: bundled(golang(github.com/golang/groupcache/lru)) = %{version}-604ed5785183e59ae2789449d89e73f3a2a77987
Provides: bundled(golang(github.com/golang/protobuf/jsonpb)) = %{version}-8616e8ee5e20a1704615e6c8d7afcdac06087a67
Provides: bundled(golang(github.com/golang/protobuf/proto)) = %{version}-8616e8ee5e20a1704615e6c8d7afcdac06087a67
Provides: bundled(golang(github.com/google/cadvisor/api)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/cache/memory)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/collector)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/container)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/container/common)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/container/docker)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/container/libcontainer)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/container/raw)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/container/rkt)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/container/systemd)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/devicemapper)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/events)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/fs)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/healthz)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/http)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/http/mux)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/info/v1)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/info/v2)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/machine)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/manager)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/manager/watcher)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/manager/watcher/raw)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/manager/watcher/rkt)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/metrics)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/pages)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/pages/static)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/storage)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/summary)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/utils)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/utils/cloudinfo)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/utils/cpuload)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/utils/cpuload/netlink)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/utils/docker)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/utils/oomparser)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/utils/sysfs)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/utils/sysinfo)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/utils/tail)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/validate)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/google/cadvisor/version)) = %{version}-ef63d70156d509efbbacfc3e86ed120228fab914
Provides: bundled(golang(github.com/grpc-ecosystem/grpc-gateway/runtime)) = %{version}-f52d055dc48aec25854ed7d31862f78913cf17d1
Provides: bundled(golang(github.com/grpc-ecosystem/grpc-gateway/runtime/internal)) = %{version}-f52d055dc48aec25854ed7d31862f78913cf17d1
Provides: bundled(golang(github.com/grpc-ecosystem/grpc-gateway/utilities)) = %{version}-f52d055dc48aec25854ed7d31862f78913cf17d1
Provides: bundled(golang(github.com/hashicorp/hcl/hcl/ast)) = %{version}-372e8ddaa16fd67e371e9323807d056b799360af
Provides: bundled(golang(github.com/hashicorp/hcl/hcl/parser)) = %{version}-372e8ddaa16fd67e371e9323807d056b799360af
Provides: bundled(golang(github.com/hashicorp/hcl/hcl/scanner)) = %{version}-372e8ddaa16fd67e371e9323807d056b799360af
Provides: bundled(golang(github.com/hashicorp/hcl/hcl/strconv)) = %{version}-372e8ddaa16fd67e371e9323807d056b799360af
Provides: bundled(golang(github.com/hashicorp/hcl/hcl/token)) = %{version}-372e8ddaa16fd67e371e9323807d056b799360af
Provides: bundled(golang(github.com/hashicorp/hcl/json/parser)) = %{version}-372e8ddaa16fd67e371e9323807d056b799360af
Provides: bundled(golang(github.com/hashicorp/hcl/json/scanner)) = %{version}-372e8ddaa16fd67e371e9323807d056b799360af
Provides: bundled(golang(github.com/hashicorp/hcl/json/token)) = %{version}-372e8ddaa16fd67e371e9323807d056b799360af
Provides: bundled(golang(github.com/matttproud/golang_protobuf_extensions/pbutil)) = %{version}-fc2b8d3a73c4867e51861bbdd5ae3c1f0869dd6a
Provides: bundled(golang(github.com/openshift/origin/pkg/api)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/api/extension)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/api/latest)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/auth/api)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/auth/authenticator)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/auth/authenticator/request/x509request)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/authorization/api)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/build/api)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/build/api/install)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/build/api/v1)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/build/client)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/build/util)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/client)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/cmd/cli/config)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/cmd/util)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/deploy/api)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/deploy/api/install)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/deploy/api/v1)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/deploy/cmd)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/deploy/util)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/image/api)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/image/api/docker10)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/image/api/dockerpre012)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/image/api/install)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/image/api/v1)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/image/reference)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/oauth/api)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/project/api)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/quota/api)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/quota/util)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/route/api)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/route/api/install)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/route/api/v1)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/sdn/api)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/security/api)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/template/api)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/user/api)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/util/namer)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/openshift/origin/pkg/version)) = %{version}-b4e0954faa4a0d11d9c1a536b76ad4a8c0206b7c
Provides: bundled(golang(github.com/prometheus/client_golang/prometheus)) = %{version}-e51041b3fa41cece0dca035740ba6411905be473
Provides: bundled(golang(github.com/prometheus/client_model/go)) = %{version}-fa8ad6fec33561be4280a8f0514318c79d7f6cb6
Provides: bundled(golang(github.com/prometheus/common/expfmt)) = %{version}-a6ab08426bb262e2d190097751f5cfd1cfdfd17d
Provides: bundled(golang(github.com/prometheus/common/internal/bitbucket.org/ww/goautoneg)) = %{version}-a6ab08426bb262e2d190097751f5cfd1cfdfd17d
Provides: bundled(golang(github.com/prometheus/common/model)) = %{version}-a6ab08426bb262e2d190097751f5cfd1cfdfd17d
Provides: bundled(golang(github.com/spf13/afero/mem)) = %{version}-72b31426848c6ef12a7a8e216708cb0d1530f074
Provides: bundled(golang(github.com/ugorji/go/codec)) = %{version}-f4485b318aadd133842532f841dc205a8e339d74
Provides: bundled(golang(golang.org/x/net/context)) = %{version}-e90d6d0afc4c315a0d87a568ae68577cc15149a0
Provides: bundled(golang(golang.org/x/net/context/ctxhttp)) = %{version}-e90d6d0afc4c315a0d87a568ae68577cc15149a0
Provides: bundled(golang(golang.org/x/net/html)) = %{version}-e90d6d0afc4c315a0d87a568ae68577cc15149a0
Provides: bundled(golang(golang.org/x/net/html/atom)) = %{version}-e90d6d0afc4c315a0d87a568ae68577cc15149a0
Provides: bundled(golang(golang.org/x/net/http2)) = %{version}-e90d6d0afc4c315a0d87a568ae68577cc15149a0
Provides: bundled(golang(golang.org/x/net/http2/hpack)) = %{version}-e90d6d0afc4c315a0d87a568ae68577cc15149a0
Provides: bundled(golang(golang.org/x/net/idna)) = %{version}-e90d6d0afc4c315a0d87a568ae68577cc15149a0
Provides: bundled(golang(golang.org/x/net/internal/timeseries)) = %{version}-e90d6d0afc4c315a0d87a568ae68577cc15149a0
Provides: bundled(golang(golang.org/x/net/lex/httplex)) = %{version}-e90d6d0afc4c315a0d87a568ae68577cc15149a0
Provides: bundled(golang(golang.org/x/net/proxy)) = %{version}-e90d6d0afc4c315a0d87a568ae68577cc15149a0
Provides: bundled(golang(golang.org/x/net/trace)) = %{version}-e90d6d0afc4c315a0d87a568ae68577cc15149a0
Provides: bundled(golang(golang.org/x/net/websocket)) = %{version}-e90d6d0afc4c315a0d87a568ae68577cc15149a0
Provides: bundled(golang(golang.org/x/oauth2/google)) = %{version}-3c3a985cb79f52a3190fbc056984415ca6763d01
Provides: bundled(golang(golang.org/x/oauth2/internal)) = %{version}-3c3a985cb79f52a3190fbc056984415ca6763d01
Provides: bundled(golang(golang.org/x/oauth2/jws)) = %{version}-3c3a985cb79f52a3190fbc056984415ca6763d01
Provides: bundled(golang(golang.org/x/oauth2/jwt)) = %{version}-3c3a985cb79f52a3190fbc056984415ca6763d01
Provides: bundled(golang(golang.org/x/sys/unix)) = %{version}-aaabbdc969c3935a2a7f61efac801e7163c73a2a
Provides: bundled(golang(golang.org/x/text/cases)) = %{version}-ceefd2213ed29504fff30155163c8f59827734f3
Provides: bundled(golang(golang.org/x/text/internal/tag)) = %{version}-ceefd2213ed29504fff30155163c8f59827734f3
Provides: bundled(golang(golang.org/x/text/language)) = %{version}-ceefd2213ed29504fff30155163c8f59827734f3
Provides: bundled(golang(golang.org/x/text/runes)) = %{version}-ceefd2213ed29504fff30155163c8f59827734f3
Provides: bundled(golang(golang.org/x/text/secure/bidirule)) = %{version}-ceefd2213ed29504fff30155163c8f59827734f3
Provides: bundled(golang(golang.org/x/text/secure/precis)) = %{version}-ceefd2213ed29504fff30155163c8f59827734f3
Provides: bundled(golang(golang.org/x/text/transform)) = %{version}-ceefd2213ed29504fff30155163c8f59827734f3
Provides: bundled(golang(golang.org/x/text/unicode/bidi)) = %{version}-ceefd2213ed29504fff30155163c8f59827734f3
Provides: bundled(golang(golang.org/x/text/unicode/norm)) = %{version}-ceefd2213ed29504fff30155163c8f59827734f3
Provides: bundled(golang(golang.org/x/text/width)) = %{version}-ceefd2213ed29504fff30155163c8f59827734f3
Provides: bundled(golang(google.golang.org/appengine/internal)) = %{version}-12d5545dc1cfa6047a286d5e853841b6471f4c19
Provides: bundled(golang(google.golang.org/appengine/internal/app_identity)) = %{version}-12d5545dc1cfa6047a286d5e853841b6471f4c19
Provides: bundled(golang(google.golang.org/appengine/internal/base)) = %{version}-12d5545dc1cfa6047a286d5e853841b6471f4c19
Provides: bundled(golang(google.golang.org/appengine/internal/datastore)) = %{version}-12d5545dc1cfa6047a286d5e853841b6471f4c19
Provides: bundled(golang(google.golang.org/appengine/internal/log)) = %{version}-12d5545dc1cfa6047a286d5e853841b6471f4c19
Provides: bundled(golang(google.golang.org/appengine/internal/modules)) = %{version}-12d5545dc1cfa6047a286d5e853841b6471f4c19
Provides: bundled(golang(google.golang.org/appengine/internal/remote_api)) = %{version}-12d5545dc1cfa6047a286d5e853841b6471f4c19
Provides: bundled(golang(google.golang.org/appengine/internal/urlfetch)) = %{version}-12d5545dc1cfa6047a286d5e853841b6471f4c19
Provides: bundled(golang(google.golang.org/appengine/urlfetch)) = %{version}-12d5545dc1cfa6047a286d5e853841b6471f4c19
Provides: bundled(golang(google.golang.org/grpc/codes)) = %{version}-b1a2821ca5a4fd6b6e48ddfbb7d6d7584d839d21
Provides: bundled(golang(google.golang.org/grpc/credentials)) = %{version}-b1a2821ca5a4fd6b6e48ddfbb7d6d7584d839d21
Provides: bundled(golang(google.golang.org/grpc/grpclog)) = %{version}-b1a2821ca5a4fd6b6e48ddfbb7d6d7584d839d21
Provides: bundled(golang(google.golang.org/grpc/internal)) = %{version}-b1a2821ca5a4fd6b6e48ddfbb7d6d7584d839d21
Provides: bundled(golang(google.golang.org/grpc/metadata)) = %{version}-b1a2821ca5a4fd6b6e48ddfbb7d6d7584d839d21
Provides: bundled(golang(google.golang.org/grpc/naming)) = %{version}-b1a2821ca5a4fd6b6e48ddfbb7d6d7584d839d21
Provides: bundled(golang(google.golang.org/grpc/peer)) = %{version}-b1a2821ca5a4fd6b6e48ddfbb7d6d7584d839d21
Provides: bundled(golang(google.golang.org/grpc/transport)) = %{version}-b1a2821ca5a4fd6b6e48ddfbb7d6d7584d839d21
Provides: bundled(golang(k8s.io/client-go/1.4/discovery)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/dynamic)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/kubernetes)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/kubernetes/typed/apps/v1alpha1)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/kubernetes/typed/authentication/v1beta1)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/kubernetes/typed/authorization/v1beta1)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/kubernetes/typed/autoscaling/v1)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/kubernetes/typed/batch/v1)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/kubernetes/typed/certificates/v1alpha1)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/kubernetes/typed/core/v1)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/kubernetes/typed/extensions/v1beta1)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/kubernetes/typed/policy/v1alpha1)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/kubernetes/typed/rbac/v1alpha1)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/kubernetes/typed/storage/v1beta1)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/api)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/api/endpoints)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/api/errors)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/api/install)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/api/meta)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/api/meta/metatypes)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/api/pod)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/api/resource)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/api/service)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/api/unversioned)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/api/unversioned/validation)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/api/util)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/api/v1)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/api/validation)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apimachinery)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apimachinery/registered)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/apps)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/apps/install)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/apps/v1alpha1)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/authentication)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/authentication/install)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/authentication/v1beta1)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/authorization)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/authorization/install)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/authorization/v1beta1)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/autoscaling)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/autoscaling/install)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/autoscaling/v1)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/batch)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/batch/install)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/batch/v1)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/batch/v2alpha1)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/certificates)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/certificates/install)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/certificates/v1alpha1)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/componentconfig)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/componentconfig/install)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/componentconfig/v1alpha1)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/extensions)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/extensions/install)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/extensions/v1beta1)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/imagepolicy)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/imagepolicy/install)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/imagepolicy/v1alpha1)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/policy)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/policy/install)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/policy/v1alpha1)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/rbac)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/rbac/install)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/rbac/v1alpha1)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/storage)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/storage/install)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/apis/storage/v1beta1)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/auth/user)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/capabilities)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/conversion)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/conversion/queryparams)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/fields)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/kubelet/qos)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/kubelet/server/portforward)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/kubelet/types)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/labels)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/master/ports)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/runtime)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/runtime/serializer)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/runtime/serializer/json)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/runtime/serializer/protobuf)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/runtime/serializer/recognizer)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/runtime/serializer/streaming)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/runtime/serializer/versioning)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/security/apparmor)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/selection)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/third_party/forked/golang/json)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/third_party/forked/golang/reflect)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/types)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/clock)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/config)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/crypto)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/diff)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/errors)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/flowcontrol)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/framer)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/hash)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/homedir)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/httpstream)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/integer)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/intstr)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/json)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/labels)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/net)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/net/sets)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/parsers)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/rand)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/runtime)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/sets)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/strategicpatch)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/uuid)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/validation)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/validation/field)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/wait)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/util/yaml)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/version)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/watch)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/pkg/watch/versioned)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/rest)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/tools/clientcmd/api)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/tools/metrics)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/client-go/1.4/transport)) = %{version}-d72c0e162789e1bbb33c33cfa26858a1375efe01
Provides: bundled(golang(k8s.io/kubernetes/federation/apis/federation)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/federation/apis/federation/install)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/federation/apis/federation/v1beta1)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/federation/client/clientset_generated/federation_internalclientset)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/federation/client/clientset_generated/federation_internalclientset/typed/core/unversioned)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/federation/client/clientset_generated/federation_internalclientset/typed/extensions/unversioned)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/federation/client/clientset_generated/federation_internalclientset/typed/federation/unversioned)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/api)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/annotations)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/endpoints)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/errors)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/install)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/meta)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/meta/metatypes)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/pod)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/resource)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/rest)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/service)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/unversioned)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/unversioned/validation)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/util)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/v1)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/api/validation)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apimachinery)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apimachinery/registered)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/apps)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/apps/install)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/apps/v1alpha1)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/authentication)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/authentication/install)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/authentication/v1beta1)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/authorization)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/authorization/install)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/authorization/v1beta1)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/autoscaling)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/autoscaling/install)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/autoscaling/v1)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/batch)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/batch/install)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/batch/v1)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/batch/v2alpha1)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/certificates)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/certificates/install)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/certificates/v1alpha1)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/componentconfig)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/componentconfig/install)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/componentconfig/v1alpha1)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/extensions)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/extensions/install)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/extensions/v1beta1)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/extensions/validation)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/policy)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/policy/install)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/policy/v1alpha1)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/rbac)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/rbac/install)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/rbac/v1alpha1)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/storage)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/storage/install)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/storage/util)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/apis/storage/v1beta1)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/auth/authenticator)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/auth/user)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/capabilities)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/cache)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/typed/authentication/unversioned)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/typed/authorization/unversioned)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/typed/autoscaling/unversioned)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/typed/batch/unversioned)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/typed/certificates/unversioned)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/typed/core/unversioned)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/typed/extensions/unversioned)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/typed/rbac/unversioned)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/clientset_generated/internalclientset/typed/storage/unversioned)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/metrics)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/record)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/restclient)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/transport)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/typed/discovery)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/typed/dynamic)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/unversioned)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/unversioned/adapters/internalclientset)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/unversioned/auth)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/unversioned/clientcmd)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/unversioned/clientcmd/api)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/unversioned/clientcmd/api/latest)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/client/unversioned/clientcmd/api/v1)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/controller)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/controller/deployment/util)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/controller/framework)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/conversion)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/conversion/queryparams)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/credentialprovider)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/fieldpath)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/fields)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/kubectl)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/kubectl/cmd/util)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/kubectl/resource)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/kubelet/qos)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/kubelet/types)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/labels)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/master/ports)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/registry/generic)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/registry/thirdpartyresourcedata)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/runtime)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/runtime/serializer)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/runtime/serializer/json)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/runtime/serializer/protobuf)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/runtime/serializer/recognizer)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/runtime/serializer/streaming)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/runtime/serializer/versioning)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/security/apparmor)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/security/podsecuritypolicy/util)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/securitycontextconstraints/util)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/selection)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/serviceaccount)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/storage)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/storage/etcd)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/storage/etcd/metrics)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/storage/etcd/util)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/storage/etcd3)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/storage/storagebackend)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/storage/storagebackend/factory)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/types)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/cache)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/certificates)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/clock)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/config)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/crypto)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/diff)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/errors)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/exec)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/flag)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/flowcontrol)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/framer)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/hash)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/homedir)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/integer)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/intstr)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/json)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/jsonpath)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/labels)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/net)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/net/sets)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/parsers)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/pod)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/rand)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/replicaset)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/runtime)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/sets)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/slice)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/strategicpatch)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/uuid)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/validation)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/validation/field)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/wait)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/util/yaml)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/version)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/watch)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/pkg/watch/versioned)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/plugin/pkg/client/auth)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/plugin/pkg/client/auth/gcp)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/plugin/pkg/client/auth/oidc)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/third_party/forked/golang/json)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/third_party/forked/golang/netutil)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/third_party/forked/golang/reflect)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
Provides: bundled(golang(k8s.io/kubernetes/third_party/forked/golang/template)) = %{version}-a9e9cf3b407c1d315686c452bdb918c719c3ea6e
%endif

%description
%{summary}

%if 0%{?with_devel}
%package devel
Summary:       %{summary}
BuildArch:     noarch

# devel subpackage BuildRequires
%if 0%{?with_check} && ! 0%{?with_bundled}
# These buildrequires are only for our tests (check)
BuildRequires: golang(github.com/Sirupsen/logrus)
BuildRequires: golang(github.com/docker/libcompose/config)
BuildRequires: golang(github.com/docker/libcompose/lookup)
BuildRequires: golang(github.com/docker/libcompose/project)
BuildRequires: golang(github.com/docker/libcompose/yaml)
BuildRequires: golang(github.com/fatih/structs)
BuildRequires: golang(github.com/ghodss/yaml)
BuildRequires: golang(github.com/openshift/origin/pkg/build/api)
BuildRequires: golang(github.com/openshift/origin/pkg/build/api/install)
BuildRequires: golang(github.com/openshift/origin/pkg/client)
BuildRequires: golang(github.com/openshift/origin/pkg/cmd/cli/config)
BuildRequires: golang(github.com/openshift/origin/pkg/deploy/api)
BuildRequires: golang(github.com/openshift/origin/pkg/deploy/api/install)
BuildRequires: golang(github.com/openshift/origin/pkg/deploy/cmd)
BuildRequires: golang(github.com/openshift/origin/pkg/image/api)
BuildRequires: golang(github.com/openshift/origin/pkg/image/api/install)
BuildRequires: golang(github.com/openshift/origin/pkg/route/api)
BuildRequires: golang(github.com/openshift/origin/pkg/route/api/install)
BuildRequires: golang(github.com/spf13/cobra)
BuildRequires: golang(github.com/spf13/viper)
BuildRequires: golang(k8s.io/kubernetes/pkg/api)
BuildRequires: golang(k8s.io/kubernetes/pkg/api/install)
BuildRequires: golang(k8s.io/kubernetes/pkg/api/resource)
BuildRequires: golang(k8s.io/kubernetes/pkg/api/unversioned)
BuildRequires: golang(k8s.io/kubernetes/pkg/apis/extensions)
BuildRequires: golang(k8s.io/kubernetes/pkg/apis/extensions/install)
BuildRequires: golang(k8s.io/kubernetes/pkg/client/unversioned)
BuildRequires: golang(k8s.io/kubernetes/pkg/client/unversioned/clientcmd)
BuildRequires: golang(k8s.io/kubernetes/pkg/kubectl)
BuildRequires: golang(k8s.io/kubernetes/pkg/kubectl/cmd/util)
BuildRequires: golang(k8s.io/kubernetes/pkg/runtime)
BuildRequires: golang(k8s.io/kubernetes/pkg/util/intstr)
%endif

# devel subpackage Requires. This is basically the source code from
# all of the libraries that kompose imports during build.
Requires:      golang(github.com/Sirupsen/logrus)
Requires:      golang(github.com/docker/libcompose/config)
Requires:      golang(github.com/docker/libcompose/lookup)
Requires:      golang(github.com/docker/libcompose/project)
Requires:      golang(github.com/docker/libcompose/yaml)
Requires:      golang(github.com/fatih/structs)
Requires:      golang(github.com/ghodss/yaml)
Requires:      golang(github.com/openshift/origin/pkg/build/api)
Requires:      golang(github.com/openshift/origin/pkg/build/api/install)
Requires:      golang(github.com/openshift/origin/pkg/client)
Requires:      golang(github.com/openshift/origin/pkg/cmd/cli/config)
Requires:      golang(github.com/openshift/origin/pkg/deploy/api)
Requires:      golang(github.com/openshift/origin/pkg/deploy/api/install)
Requires:      golang(github.com/openshift/origin/pkg/deploy/cmd)
Requires:      golang(github.com/openshift/origin/pkg/image/api)
Requires:      golang(github.com/openshift/origin/pkg/image/api/install)
Requires:      golang(github.com/openshift/origin/pkg/route/api)
Requires:      golang(github.com/openshift/origin/pkg/route/api/install)
Requires:      golang(github.com/spf13/cobra)
Requires:      golang(github.com/spf13/viper)
Requires:      golang(k8s.io/kubernetes/pkg/api)
Requires:      golang(k8s.io/kubernetes/pkg/api/install)
Requires:      golang(k8s.io/kubernetes/pkg/api/resource)
Requires:      golang(k8s.io/kubernetes/pkg/api/unversioned)
Requires:      golang(k8s.io/kubernetes/pkg/apis/extensions)
Requires:      golang(k8s.io/kubernetes/pkg/apis/extensions/install)
Requires:      golang(k8s.io/kubernetes/pkg/client/unversioned)
Requires:      golang(k8s.io/kubernetes/pkg/client/unversioned/clientcmd)
Requires:      golang(k8s.io/kubernetes/pkg/kubectl)
Requires:      golang(k8s.io/kubernetes/pkg/kubectl/cmd/util)
Requires:      golang(k8s.io/kubernetes/pkg/runtime)
Requires:      golang(k8s.io/kubernetes/pkg/util/intstr)

# devel subpackage Provides
Provides:      golang(%{import_path}/cmd) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/app) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/kobject) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/loader) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/loader/bundle) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/loader/compose) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/testutils) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/transformer) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/transformer/kubernetes) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/transformer/openshift) = %{version}-%{release}

%description devel
%{summary}

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package unit-test-devel
Summary:         Unit tests for %{name} package
%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}

%if 0%{?with_check} && ! 0%{?with_bundled}
%endif


%description unit-test-devel
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%setup -q -n %{repo}-%{commit}

%build
# set up temporary build gopath in pwd
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s ../../../ src/%{import_path}

%if ! 0%{?with_bundled}
export GOPATH=$(pwd):%{gopath}
%else
# No dependency directories so far
export GOPATH=$(pwd):%{gopath}
%endif

export LDFLAGS=%{ldflags}
%gobuild %{buildflags} -o bin/kompose %{import_path}/

%install
install -d -p %{buildroot}%{_bindir}
install -p -m 0755 bin/kompose %{buildroot}%{_bindir}

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . \( -iname "*.go" -or -iname "*.s" \) \! -iname "*_test.go" | grep -v "vendor") ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test-devel.file-list
for file in $(find . -iname "*_test.go" | grep -v "vendor") ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test-devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

# check uses buildroot macro so that unit-tests can be run over the
# files that are about to be installed with the rpm.
%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%else
# Since we aren't packaging up the vendor directory we need to link
# back to it somehow. Hack it up so that we can add the vendor
# directory from BUILD dir as a gopath to be searched when executing
# tests from the BUILDROOT dir.
ln -s ./ ./vendor/src # ./vendor/src -> ./vendor

export GOPATH=%{buildroot}/%{gopath}:$(pwd)/vendor:%{gopath}
%endif

%if ! 0%{?gotest:1}
%global gotest go test -ldflags "${LDFLAGS:-}"
%endif

export LDFLAGS=%{ldflags}
%gotest %{buildflags} %{testflags} %{import_path}/pkg/loader/bundle
%gotest %{buildflags} %{testflags} %{import_path}/pkg/loader/compose
%gotest %{buildflags} %{testflags} %{import_path}/pkg/transformer
%gotest %{buildflags} %{testflags} %{import_path}/pkg/transformer/kubernetes
%gotest %{buildflags} %{testflags} %{import_path}/pkg/transformer/openshift
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE
%doc CHANGELOG.md ROADMAP.md CONTRIBUTING.md code-of-conduct.md README.md RELEASE.md
%{_bindir}/kompose

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENSE
%doc CHANGELOG.md ROADMAP.md CONTRIBUTING.md code-of-conduct.md README.md RELEASE.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files unit-test-devel -f unit-test-devel.file-list
%license LICENSE
%doc CHANGELOG.md ROADMAP.md CONTRIBUTING.md code-of-conduct.md README.md RELEASE.md
%endif

%changelog
* Sat Feb 25 2017 Suraj Deshmukh <surajssd009005@gmail.com> - 0.3.0-0.1.git135165b
- Update to kompose version 0.3.0

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-0.2.git92ea047
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Nov 26 2016 Dusty Mabe <dusty@dustymabe.com> - 0.1.2-0.1.git92ea047
- Update to kompose version 0.1.2

* Thu Sep 22 2016 dustymabe - 0.1.0-0.1.git8227684
- First package for Fedora
