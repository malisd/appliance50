class dhcp {

    package { 'dhclient':
        ensure => installed
    }

    file { '/etc/dhcp/dhclient-eth0.conf':
        ensure => file,
        group => 'root',
        mode => 644,
        owner => 'root',
        path => '/etc/dhcp/dhclient-eth0.conf',
        require => Package['dhclient'],
        source => 'puppet:///modules/dhcp/etc/dhcp/dhclient-eth0.conf'
    }
}
