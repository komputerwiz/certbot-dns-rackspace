# certbot-dns-rackspace

Certbot plugin for ACME DNS-01 Challenge on Rackspace Cloud DNS

## Usage

    certbot certonly \
      -a dns-rackspace \
      -d example.com \
      --dns-rackspace-credentials="/path/to/creds.ini" \
      --dns-rackspace-zone=example.com \
      --dns-rackspace-propagation-seconds=30

## Example Configuration

Save the following somewhere safe, like a protected `rax.ini` file accessible only to certbot.

    dns_rackspace_username = foobarbaz
    dns_rackspace_api_key = 1337cafef00dd00dbabe
