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
"""

from builtins import object

from django.db import models
from django.utils.translation import gettext_lazy as _


class ApiWhiteList(models.Model):
    """
    api 的白名单
    """

    API_NAME_CHOICES = [("app_maker", _(u"轻应用相关接口"))]

    api_name = models.CharField(_(u"接口类别"), max_length=20, choices=API_NAME_CHOICES)
    app_code = models.CharField(_(u"可调用接口的应用编码"), max_length=20)

    def __unicode__(self):
        return "%s(%s)" % (self.api_name, self.app_code)

    def __str__(self):
        return self.api_name

    class Meta(object):
        db_table = "paas_apiwhitelist"
        verbose_name = _(u"PaaS提供的接口白名单")
        verbose_name_plural = _(u"PaaS提供的接口白名单")
