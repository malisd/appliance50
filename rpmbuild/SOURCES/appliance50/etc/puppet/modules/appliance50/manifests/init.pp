class appliance50 {

    host { 'appliance.localdomain':
        host_aliases => 'appliance',
        ip => '127.0.0.1'
    }

    file { '/etc/banner':
        ensure => file,
        group => 'root',
        mode => 644,
        owner => 'root',
        path => '/etc/banner',
        source => 'puppet:///modules/appliance50/etc/banner'
    }
}
