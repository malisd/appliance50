class mysql {

    package { ['mysql', 'mysql-server']:
        ensure => installed
    }

    service { 'mysqld':
        ensure => running,
        require => Package['mysql-server'],
        subscribe => File['/etc/my.cnf']
    }

    file { '/etc/my.cnf':
        ensure => file,
        group => 'root',
        mode => 644,
        owner => 'root',
        path => '/etc/my.conf',
        require => Package['mysql-server'],
        source => 'puppet:///modules/mysql/etc/my.cnf'
    }

    # http://projects.puppetlabs.com/projects/1/wiki/My_Sql_Server_Patterns 
    $password = 'crimson'
    exec { "Set MySQL server root password":
        command => "mysqladmin -uroot password $password",
        path => "/bin:/usr/bin",
        refreshonly => true,
        subscribe => Package["mysql", "mysql-server"],
        unless => "mysqladmin -uroot -p$password status"
    }
}
