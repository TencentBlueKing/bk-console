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

import uuid
from builtins import object

from django.db import models
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _l

from audit.constants import AuditEventOperationTypeEnum


class AuditEventLog(models.Model):
    OP_TYPE_CHOICES = (
        (AuditEventOperationTypeEnum.QUERY, _(u"查询")),
        (AuditEventOperationTypeEnum.CREATE, _(u"创建")),
        (AuditEventOperationTypeEnum.DELETE, _(u"删除")),
        (AuditEventOperationTypeEnum.MODIFY, _(u"修改")),
    )

    event_id = models.UUIDField(default=uuid.uuid4, editable=False)
    system = models.CharField(max_length=64, blank=False, null=False)
    username = models.CharField(max_length=64, blank=False, null=False)

    op_time = models.DateTimeField(auto_now_add=True)
    op_type = models.CharField(max_length=32, choices=OP_TYPE_CHOICES, blank=False, null=False)
    op_object_type = models.CharField(max_length=32, blank=False, null=False)
    op_object_id = models.CharField(max_length=64, blank=True, null=True)
    op_object_name = models.CharField(max_length=64, blank=True, null=True)

    data_before = models.TextField(null=True, blank=True)
    data_after = models.TextField(null=True, blank=True)

    comment = models.TextField(null=True, blank=True)

    class Meta(object):
        db_table = "audit_event_log"
        verbose_name = _l(u"操作审计日志")
        verbose_name_plural = _l(u"操作审计日志")
