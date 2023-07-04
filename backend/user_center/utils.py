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
from django.conf import settings

from common.constants import ROLECODE_DICT, RoleCodeEnum


def get_smart_paas_domain():
    """
    智能获取paas域名，80端口去除
    """
    host_port = settings.PAAS_DOMAIN.split(":")
    port = host_port[1] if len(host_port) >= 2 else ""
    paas_domain = host_port[0] if port in ["80"] else settings.PAAS_DOMAIN
    return paas_domain


def get_role_display(role):
    if role.isdigit():
        return ROLECODE_DICT.get(int(role)) or ROLECODE_DICT[RoleCodeEnum.STAFF]
    return ROLECODE_DICT[RoleCodeEnum.STAFF]
