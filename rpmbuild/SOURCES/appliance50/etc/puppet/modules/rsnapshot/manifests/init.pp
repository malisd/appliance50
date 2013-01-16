class rsnapshot {

    include cronie
    include mysql

    package { 'rsnapshot':
        ensure => installed
    }
        
    file { '/etc/cron.d/rsnapshot':
        ensure => file,
        group => 'root',
        mode => 644,
        owner => 'root',
        path => '/etc/cron.d/rsnapshot',
        require => Package['rsnapshot'],
        source => 'puppet:///modules/rsnapshot/etc/cron.d/rsnapshot'
    }
}
