#!/bin/bash
yum install -y httpd
systemctl start httpd
systemctl enable httpd
echo '{{contents_for_web}}' >/var/www/html/index.html
