# Copyright 2019 Axis Communications AB.
#
# For a full list of individual contributors, please see the commit history.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import graphene
from eiffel_graphql_api.graphql.schemas.events import SourceChangeSubmitted, SourceChangeCreated
from ..utils import find_one


class Base(graphene.ObjectType):
    source_change_submitted = graphene.Field(SourceChangeSubmitted)

    def __init__(self, link):
        self.link = link

    def resolve_source_change_submitted(self, info):
        from ..union import NotFound
        event = find_one("EiffelSourceChangeSubmittedEvent", {"meta.id": self.link.get("target")})
        if event is None:
            return NotFound(self.link, "Could not find event in database.")
        return SourceChangeSubmitted(event)


class SourceChange(graphene.ObjectType):
    source_change_created = graphene.Field(SourceChangeCreated)

    def __init__(self, link):
        self.link = link

    def resolve_source_change_submitted(self, info):
        from ..union import NotFound
        event = find_one("EiffelSourceChangeCreatedEvent", {"meta.id": self.link.get("target")})
        if event is None:
            return NotFound(self.link, "Could not find event in database.")
        return SourceChangeCreated(event)


class SourceSubmittedPreviousVersion(Base): pass
class SourceCreatedPreviousVersion(SourceChange): pass
