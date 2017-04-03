class profiles::memcached::default {

        package { 'memcached':
		 ensure => 'installed',
        }

        file { '/etc/sysconfig/memcached':
                notify  => Service['memcached'],
                owner   => root,
                group   => root,
                mode    => 755,
                content => template('profiles/memcached/memcached.erb'),
		require => Package['memcached'],
        }

	file {'memcache_ulimit':
		path    => '/etc/security/limits.conf',
		owner   => root,
		group   => root,
		mode    => 755,
		content => template('profiles/memcached/limits.conf.erb'),
		require => Package['memcached'],	
	}
	
	service { 'memcached':
		ensure  => 'running',
		enable  => 'true',
		require => File['/etc/sysconfig/memcached'],
	}
}
