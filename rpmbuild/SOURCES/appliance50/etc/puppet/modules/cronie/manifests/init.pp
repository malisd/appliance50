class cronie {

    package { 'cronie':
        ensure => installed
    }

    service { 'crond':
        ensure => running,
        require => Package['cronie']
    }
}
