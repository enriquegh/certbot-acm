"""Let's Encrypt ACM installer plugin."""

from __future__ import print_function

import os
import logging

import zope.interface

import boto3

from certbot import interfaces
from certbot.plugins import common


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@zope.interface.implementer(interfaces.IInstaller)
@zope.interface.provider(interfaces.IPluginFactory)
class Installer(common.Plugin):

    description = "ACM installer"

    def __init__(self, *args, **kwargs):
        logger.error("THIS IS AN ERROR IN THE CONSTRUCTOR")
        super(Installer, self).__init__(*args, **kwargs)

    def get_all_names(self):
        pass

    def view_config_changes(self):
        pass

    def prepare(self):
        pass

    def supported_enhancements(self):
        return []

    def config_test(self):
        pass

    def recovery_routine(self):
        pass

    def enhance(self, domain, enhancement, options=None):
        pass

    def save(self, title=None, temporary=False):
        pass

    def rollback_checkpoints(self, rollback=1):
        pass

    def restart(self):
        logger.error("THIS IS AN ERROR IN RESTART")
        for domain in self.config.domains:
            logger.info("Renew domain: "+domain)
            cert_path = os.path.join(
                self.config.live_dir, domain, 'cert.pem'
            )
            chain_path = os.path.join(
                self.config.live_dir, domain, 'chain.pem'
            )
            fullchain_path = os.path.join(
                self.config.live_dir, domain, 'fullchain.pem'
            )
            key_path = os.path.join(
                self.config.live_dir, domain, 'privkey.pem'
            )
            try:
                open(cert_path, 'r')
            except IOError as e:
                logger.error(e)
                continue
            self.deploy_cert(
                domain, cert_path, key_path, chain_path, fullchain_path
            )

    def more_info(self):
        return ""

    def deploy_cert(self, domain,
                    cert_path, key_path, chain_path, fullchain_path):
        """
        Upload Certificate to ACM
        """
        logger.error("THIS IS AN ERROR IN DEPLOY CERT")
        acm_client = boto3.client('acm')

        certificate = {
            'Certificate': open(cert_path).read(),
            'PrivateKey': open(key_path).read(),
            'CertificateChain': open(chain_path).read()
        }

        try:
            response = acm_client.list_certificates()
            logger.debug(response)

            cert_list = response['CertificateSummaryList']

            if not cert_list:
                logger.debug("No certs found!")
                pass
            else:
                for cert in cert_list:
                    if (cert['DomainName'] == domain):
                        certificate['CertificateArn'] = cert['CertificateArn']

        except api_client.exceptions.NotFoundException:
            logger.info('API Domain not found: %s' % domain)

        response = acm_client.import_certificate(**certificate)
        logger.info('Certificate %s is imported.' % response['CertificateArn'])
