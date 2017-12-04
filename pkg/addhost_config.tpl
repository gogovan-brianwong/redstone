general_list = [

            { 'nodeinfo_list': {
                        'hostname': '{{ hostname }}',
                        'hostip': '{{ hostip }}',
                        'domain': '{{ domain }}',
                        },
            },
            { 'cert_files': {
                        'cacert': '{{ cacert }}',
                        'cakey': '{{ cakey }}',
                        'registry_ca': '{{ registry_ca }}',
                        'ssl_conf': '{{ ssl_conf }}',

                        },
            },
            {'local_path_list': {
                'tpl_path': '{{ tpl_path }}',
                'conf_archive_path': '{{ conf_archive_path }}',
                'cert_archive_path': '{{ cert_archive_path }}',
                        },
            }
        ]

deploy_list = [

    { 'generate_list': [

                {'remote_dir': '/etc/kubernetes/ssl',
                                'files': [ '{{ hostname }}' + '.pem', '{{ hostname }}' + '-key.pem' ] },
                {'remote_dir': '/etc/kubernetes/tokens',
                                'files': ['system:' + '{{ hostname }}' + '.token']},
                ]
    },
    { 'render_file_list': [
                { 'remote_dir': '/etc/kubernetes', 'files': [ 'kubelet.env', 'node-kubeconfig.yaml' ] },
                { 'remote_dir': '/etc/kubernetes/manifests', 'files': [ 'flannel-pod.manifest','kube-proxy.manifest' ] },

                { 'remote_dir': '/etc/kubernetes/ssl', 'files': [ 'worker-openssl.conf' ]},
                ]
    },
    { 'netcopy_list': [
                    { 'remote_dir': '/etc/kubernetes/ssl', 'files': [ 'ca.pem' ] },
                    { 'remote_dir': '/etc/docker/certs.d/registry.allbright.local:5000', 'files': ['ca.crt'] },
                    { 'remote_dir': '/etc/systemd/system', 'files': [ 'kubelet.service' ]},
                    { 'remote_dir': '/opt/bin', 'files': [ 'kubelet', 'kube-gen-token.sh', 'mk-docker-opts.sh', 'deploy-script.sh' ] },
                    { 'remote_dir': '/etc/flannel/certs', 'files': ['ca_cert.crt', 'cert.crt', 'key.pem' ]}

                    ],
    },

]
