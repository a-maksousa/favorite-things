# Copyright (c) 2019, Mark Peek <mark@peek.org>
# All rights reserved.
#
# See LICENSE file for full license.
from . import AWSObject, AWSProperty, Tags
from .validators import boolean, integer


class LustreConfiguration(AWSProperty):
    props = {
        'ExportPath': (str, False),
        'ImportedFileChunkSize': (integer, False),
        'ImportPath': (str, False),
        'WeeklyMaintenanceStartTime': (str, False),

    }


class WindowsConfiguration(AWSProperty):
    props = {
        'ActiveDirectoryId': (str, False),
        'AutomaticBackupRetentionDays': (integer, False),
        'CopyTagsToBackups': (boolean, False),
        'DailyAutomaticBackupStartTime': (str, False),
        'ThroughputCapacity': (integer, False),
        'WeeklyMaintenanceStartTime': (str, False),
    }


class FileSystem(AWSObject):
    resource_type = 'AWS::FSx::FileSystem'

    props = {
        'BackupId': (str, False),
        'FileSystemType': (str, False),
        'KmsKeyId': (str, False),
        'LustreConfiguration': (LustreConfiguration, False),
        'SecurityGroupIds': ([str], False),
        'StorageCapacity': (integer, False),
        'SubnetIds': ([str], False),
        'Tags': (Tags, False),
        'WindowsConfiguration': (WindowsConfiguration, False),
    }
