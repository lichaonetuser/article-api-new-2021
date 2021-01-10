# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: base.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='base.proto',
  package='',
  syntax='proto2',
  serialized_pb=_b('\n\nbase.proto\"\xbd\x05\n\x06Header\x12\x13\n\x0bmessagetype\x18\x01 \x01(\t\x12\x0e\n\x06\x61pp_id\x18\x02 \x01(\t\x12\x10\n\x08\x61pp_name\x18\x03 \x01(\t\x12\x0f\n\x07\x63\x61rrier\x18\x04 \x01(\t\x12\x0f\n\x07\x63hannel\x18\x05 \x01(\t\x12\x0c\n\x04lang\x18\x06 \x01(\t\x12\x14\n\x0c\x63hannel_lang\x18\x07 \x01(\t\x12\x13\n\x0b\x64\x65vice_type\x18\x08 \x01(\t\x12\x12\n\njail_break\x18\t \x01(\x08\x12\r\n\x05model\x18\n \x01(\t\x12\x0b\n\x03osn\x18\x0b \x01(\t\x12\x0b\n\x03osv\x18\x0c \x01(\t\x12\x12\n\nphone_type\x18\r \x01(\t\x12\x18\n\x10unique_device_id\x18\x0e \x01(\t\x12\x0f\n\x07version\x18\x0f \x01(\t\x12\x14\n\x0cversion_code\x18\x10 \x01(\x03\x12\x0e\n\x06\x61\x63\x63\x65ss\x18\x11 \x01(\t\x12\x12\n\nresolution\x18\x12 \x01(\t\x12\x10\n\x08timezone\x18\x13 \x01(\x03\x12\x1b\n\x13\x64\x65vice_manufacturer\x18\x14 \x01(\t\x12\x12\n\nip_address\x18\x15 \x01(\t\x12\x0b\n\x03geo\x18\x16 \x01(\t\x12\x10\n\x08geo_city\x18\x17 \x01(\t\x12\x0b\n\x03uid\x18\x18 \x01(\t\x12\x11\n\tsign_hash\x18\x19 \x01(\t\x12\x12\n\nandroid_id\x18\x1a \x01(\t\x12\x11\n\tclient_id\x18\x1b \x01(\t\x12\x12\n\ninstall_id\x18\x1c \x01(\t\x12\x0e\n\x06os_api\x18\x1d \x01(\x03\x12\x14\n\x0c\x64\x65vice_brand\x18\x1e \x01(\t\x12\x0b\n\x03\x64pi\x18\x1f \x01(\x03\x12\x0f\n\x07\x63ountry\x18  \x01(\t\x12\x14\n\x0c\x63\x61rrier_code\x18! \x01(\t\x12\x0b\n\x03rom\x18\" \x01(\t\x12\x17\n\x0fis_first_launch\x18# \x01(\x08\x12\x1e\n\x16is_update_first_launch\x18$ \x01(\x08\x12\x0e\n\x06\x65_flag\x18% \x01(\t*I\n\x06\x41\x63\x63\x65ss\x12\x0f\n\x0b\x41\x43\x43\x45SS_WIFI\x10\x00\x12\r\n\tACCESS_3G\x10\x01\x12\r\n\tACCESS_4G\x10\x02\x12\x10\n\x0c\x41\x43\x43\x45SS_OTHER\x10\x03*\"\n\x0b\x43ontentType\x12\x13\n\x0f\x43ONTENT_ARTICLE\x10\x00')
)

_ACCESS = _descriptor.EnumDescriptor(
  name='Access',
  full_name='Access',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ACCESS_WIFI', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ACCESS_3G', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ACCESS_4G', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ACCESS_OTHER', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=718,
  serialized_end=791,
)
_sym_db.RegisterEnumDescriptor(_ACCESS)

Access = enum_type_wrapper.EnumTypeWrapper(_ACCESS)
_CONTENTTYPE = _descriptor.EnumDescriptor(
  name='ContentType',
  full_name='ContentType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='CONTENT_ARTICLE', index=0, number=0,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=793,
  serialized_end=827,
)
_sym_db.RegisterEnumDescriptor(_CONTENTTYPE)

ContentType = enum_type_wrapper.EnumTypeWrapper(_CONTENTTYPE)
ACCESS_WIFI = 0
ACCESS_3G = 1
ACCESS_4G = 2
ACCESS_OTHER = 3
CONTENT_ARTICLE = 0



_HEADER = _descriptor.Descriptor(
  name='Header',
  full_name='Header',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='messagetype', full_name='Header.messagetype', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='app_id', full_name='Header.app_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='app_name', full_name='Header.app_name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='carrier', full_name='Header.carrier', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='channel', full_name='Header.channel', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='lang', full_name='Header.lang', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='channel_lang', full_name='Header.channel_lang', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='device_type', full_name='Header.device_type', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='jail_break', full_name='Header.jail_break', index=8,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='model', full_name='Header.model', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='osn', full_name='Header.osn', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='osv', full_name='Header.osv', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='phone_type', full_name='Header.phone_type', index=12,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='unique_device_id', full_name='Header.unique_device_id', index=13,
      number=14, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='version', full_name='Header.version', index=14,
      number=15, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='version_code', full_name='Header.version_code', index=15,
      number=16, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='access', full_name='Header.access', index=16,
      number=17, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='resolution', full_name='Header.resolution', index=17,
      number=18, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='timezone', full_name='Header.timezone', index=18,
      number=19, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='device_manufacturer', full_name='Header.device_manufacturer', index=19,
      number=20, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ip_address', full_name='Header.ip_address', index=20,
      number=21, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='geo', full_name='Header.geo', index=21,
      number=22, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='geo_city', full_name='Header.geo_city', index=22,
      number=23, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='uid', full_name='Header.uid', index=23,
      number=24, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sign_hash', full_name='Header.sign_hash', index=24,
      number=25, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='android_id', full_name='Header.android_id', index=25,
      number=26, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='client_id', full_name='Header.client_id', index=26,
      number=27, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='install_id', full_name='Header.install_id', index=27,
      number=28, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='os_api', full_name='Header.os_api', index=28,
      number=29, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='device_brand', full_name='Header.device_brand', index=29,
      number=30, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dpi', full_name='Header.dpi', index=30,
      number=31, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='country', full_name='Header.country', index=31,
      number=32, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='carrier_code', full_name='Header.carrier_code', index=32,
      number=33, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='rom', full_name='Header.rom', index=33,
      number=34, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='is_first_launch', full_name='Header.is_first_launch', index=34,
      number=35, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='is_update_first_launch', full_name='Header.is_update_first_launch', index=35,
      number=36, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='e_flag', full_name='Header.e_flag', index=36,
      number=37, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=15,
  serialized_end=716,
)

DESCRIPTOR.message_types_by_name['Header'] = _HEADER
DESCRIPTOR.enum_types_by_name['Access'] = _ACCESS
DESCRIPTOR.enum_types_by_name['ContentType'] = _CONTENTTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Header = _reflection.GeneratedProtocolMessageType('Header', (_message.Message,), dict(
  DESCRIPTOR = _HEADER,
  __module__ = 'base_pb2'
  # @@protoc_insertion_point(class_scope:Header)
  ))
_sym_db.RegisterMessage(Header)


# @@protoc_insertion_point(module_scope)
