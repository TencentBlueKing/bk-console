# -*- coding: utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making
蓝鲸智云 - 蓝鲸桌面 (BlueKing - bkconsole) available.
Copyright (C) 2022 THL A29 Limited,
a Tencent company. All rights reserved.
Licensed under the MIT License (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the
specific language governing permissions and limitations under the License.

We undertake not to change the open source license (MIT license) applicable

to the current version of the project delivered to anyone in the future.

Component API Client
"""
import json
import logging
from builtins import object

import requests

from . import collections, conf
from .constants import LANG_COMPATIBLE_INFO, SUPPORTED_LANG

# shutdown urllib3's warning
try:
    requests.packages.urllib3.disable_warnings()
except Exception:
    pass


logger = logging.getLogger("root")


class BaseComponentClient(object):
    """Base client class for component"""

    @classmethod
    def setup_components(cls, components):
        cls.available_collections = components

    def __init__(self, app_code=None, app_secret=None, common_args=None, use_test_env=False, language=None):
        """
        :param str app_code: App code to use
        :param str app_secret: App secret to use
        :param dict common_args: Args that will apply to every request
        :param bool use_test_env: whether use test version of components
        """
        self.app_code = app_code or conf.APP_CODE
        self.app_secret = app_secret or conf.SECRET_KEY
        self.common_args = common_args or {}
        self._cached_collections = {}
        self.use_test_env = use_test_env
        self.language = language or self.get_cur_language()
        self._bkapi_authorization = dict(
            self.common_args.copy(), bk_app_code=self.app_code, bk_app_secret=self.app_secret
        )

    def update_bkapi_authorization(self, **auth):
        self._bkapi_authorization.update(auth)

    def set_use_test_env(self, use_test_env):
        """Change the value of use_test_env

        :param bool use_test_env: whether use test version of components
        """
        self.use_test_env = use_test_env

    def set_language(self, language):
        self.language = language

    def get_cur_language(self):
        try:
            from django.utils import translation

            return translation.get_language()
        except Exception:
            return None

    def get_supported_language_variant(self, lang_code, strict=False):
        """
        Returns the language-code that's listed in supported languages, possibly
        selecting a more generic variant. Lang_code if nothing found.

        If `strict` is False (the default), the function will look for an alternative
        country-specific variant when the currently checked is not found.
        """
        if lang_code:
            # If 'fr-ca' is not supported, try special compatible language or language-only 'fr'.
            possible_lang_codes = [lang_code]
            try:
                possible_lang_codes.extend(LANG_COMPATIBLE_INFO.get(lang_code, []))
            except KeyError:
                pass
            generic_lang_code = lang_code.split("-")[0]
            possible_lang_codes.append(generic_lang_code)
            supported_lang_codes = SUPPORTED_LANG

            for code in possible_lang_codes:
                if code in supported_lang_codes:
                    return code
            if not strict:
                # if fr-fr is not supported, try fr-ca.
                for supported_code in supported_lang_codes:
                    if supported_code.startswith(generic_lang_code + "-"):
                        return supported_code
        return lang_code

    def merge_params_data_with_common_args(self, method, params, data, enable_app_secret=False):
        """get common args when request"""
        common_args = dict(app_code=self.app_code, **self.common_args)
        if enable_app_secret:
            common_args["app_secret"] = self.app_secret
        if method == "GET":
            _params = common_args.copy()
            _params.update(params or {})
            params = _params
        elif method == "POST":
            _data = common_args.copy()
            _data.update(data or {})
            data = json.dumps(_data)
        return params, data

    def request(self, method, url, params=None, data=None, **kwargs):
        """Send request"""
        # determine whether access test environment of third-party system
        headers = kwargs.pop("headers", {})
        if self.use_test_env:
            headers["x-use-test-env"] = "1"
        if self.language:
            headers["blueking-language"] = self.get_supported_language_variant(self.language)

        # kwargs headers 实际为空，因为调用方 ComponentAPI 没有传 headers 这个参数，
        # 因此这里没有从 headers 中获取 x-bkapi-authorization 并将其与 self._bkapi_authorization 合并
        headers['x-bkapi-authorization'] = json.dumps(self._bkapi_authorization)
        params, data = self._handle_params_and_data(method, params, data)

        logger.debug("Calling %s %s with params=%s, data=%s, headers=%s", method, url, params, data, headers)
        return requests.request(method, url, params=params, data=data, verify=False, headers=headers, **kwargs)

    def _handle_params_and_data(self, method, params, data):
        if method == 'GET':
            params = params or {}
        elif method == 'POST':
            data = json.dumps(data or {})

        return params, data

    def __getattr__(self, key):
        if key not in self.available_collections:
            return getattr(super(BaseComponentClient, self), key)

        if key not in self._cached_collections:
            collection = self.available_collections[key]
            self._cached_collections[key] = collection(self)
        return self._cached_collections[key]


ComponentClient = BaseComponentClient
ComponentClient.setup_components(collections.AVAILABLE_COLLECTIONS)
