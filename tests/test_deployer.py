import yaml
from mock import MagicMock, patch

from k8s.models.common import ObjectMeta
from schip_spinnaker_webhook.paasbetaapplication import PaasbetaApplicationSpec
from schip_spinnaker_webhook.deployer import Deployer
from schip_spinnaker_webhook.models import Release

APPLICATION_NAME = "test_image"

VALID_IMAGE_NAME = "test_image:a1b2c3d"

VALID_DEPLOY_CONFIG_URL = "http://url_to_config.file"

ANY_NAMESPACE = "any-namespace"

VALID_DEPLOY_CONFIG = """
version: 2
admin_access: true
replicas: 1
resources:
  requests:
    memory: 128m
ports:
  - target_port: 5000
healthchecks:
  liveness:
    http:
      path: /healthz
config:
  volume: true
"""


class TestCreateDeploymentInK8s(object):
    @patch('k8s.base.ApiMixIn.get_or_create')
    def test_deployer_sends_tpr_to_k8s(self, get_or_create):
        k8s_model = MagicMock(spec="schip_spinnaker_webhook.paasbetaapplication.PaasbetaApplication")
        get_or_create.return_value = k8s_model
        k8s_model.save = MagicMock()

        http_client = self._given_config_url_response_content_is(VALID_DEPLOY_CONFIG)

        Deployer(http_client).deploy(
            namespace=ANY_NAMESPACE,
            release=Release(VALID_IMAGE_NAME, VALID_DEPLOY_CONFIG_URL)
        )

        http_client.get.assert_called_once_with(VALID_DEPLOY_CONFIG_URL)

        metadata = ObjectMeta(name=APPLICATION_NAME, namespace=ANY_NAMESPACE, labels={})
        spec = PaasbetaApplicationSpec(
            application=APPLICATION_NAME,
            image=VALID_IMAGE_NAME,
            config=yaml.safe_load(VALID_DEPLOY_CONFIG)
        )
        get_or_create.assert_called_once_with(metadata=metadata, spec=spec)
        k8s_model.save.assert_called_once()

    def _given_config_url_response_content_is(self, config):
        http_client = MagicMock(spec="requests.Session")
        config_response = MagicMock()
        config_response.text = config

        http_client_get = MagicMock()
        http_client_get.return_value = config_response
        http_client.get = http_client_get

        return http_client