# Copyright (c) 2012-2013, Mark Peek <mark@peek.org>
# All rights reserved.
#
# See LICENSE file for full license.

from . import AWSObject, Tags


class Activity(AWSObject):
    resource_type = "AWS::StepFunctions::Activity"
    props = {
        'Name': (str, True),
        'Tags': (Tags, False),
    }


class StateMachine(AWSObject):
    resource_type = "AWS::StepFunctions::StateMachine"
    props = {
        'StateMachineName': (str, False),
        'DefinitionString': (str, True),
        'RoleArn': (str, True),
        'Tags': (Tags, False),

    }
