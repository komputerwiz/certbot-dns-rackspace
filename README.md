# certbot-dns-rackspace
Certbot plugin for ACME DNS-01 Challenge on Rackspace Cloud DNS

## Usage

    certbot certonly \
      -a certbot-dns-rackspace:dns-rackspace \
      -d example.com \
      --certbot-dns-rackspace:dns-rackspace-credentials="/path/to/creds.ini" \
      --certbot-dns-rackspace:dns-rackspace-zone=example.com

## Example Configuration

Save the following somewhere safe, like a protected `rax.ini` file accessible only to certbot.

    certbot_dns_rackspace:dns_rackspace_username = foobarbaz
    certbot_dns_rackspace:dns_rackspace_api_key = 1337cafef00dd00dbabe
