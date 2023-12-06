# Puppet manifest to set up a basic web server with a specific directory structure

# Install Nginx package
package { 'nginx':
  ensure => installed,
}

# Create directories
file { '/data':
  ensure => 'directory',
}

file { '/data/web_static':
  ensure => 'directory',
}

file { '/data/web_static/releases':
  ensure => 'directory',
}

file { '/data/web_static/shared':
  ensure => 'directory',
}

file { '/data/web_static/releases/test':
  ensure => 'directory',
}

# Create a basic HTML file
file { '/data/web_static/releases/test/index.html':
  content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>',
}

# Create a symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
}

