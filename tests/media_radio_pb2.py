# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: media_radio.proto
# Protobuf Python Version: 5.29.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    3,
    '',
    'media_radio.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11media_radio.proto\x12\x05\x65vent\"\x80\x01\n\x11MediaRadioPayload\x12\r\n\x05\x62rand\x18\x01 \x01(\t\x12\x11\n\tsub_brand\x18\x02 \x01(\t\x12\x15\n\rcampaign_name\x18\x03 \x01(\t\x12\x12\n\nstart_date\x18\x04 \x01(\t\x12\x0c\n\x04\x63ost\x18\x05 \x01(\x01\x12\x10\n\x08\x63urrency\x18\x06 \x01(\t\"\xe7\x01\n\x12MediaRadioEnvelope\x12\x12\n\nevent_uuid\x18\x01 \x01(\t\x12\x10\n\x08\x65vent_ts\x18\x02 \x01(\x03\x12\x12\n\nevent_type\x18\x03 \x01(\t\x12\x13\n\x0boccurred_ts\x18\x04 \x01(\x03\x12\x0f\n\x07\x63hannel\x18\x05 \x01(\t\x12\x16\n\x0erequest_origin\x18\x06 \x01(\t\x12)\n\x07payload\x18\x07 \x01(\x0b\x32\x18.event.MediaRadioPayload\x12.\n\x0cprev_payload\x18\x08 \x01(\x0b\x32\x18.event.MediaRadioPayloadb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'media_radio_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_MEDIARADIOPAYLOAD']._serialized_start=29
  _globals['_MEDIARADIOPAYLOAD']._serialized_end=157
  _globals['_MEDIARADIOENVELOPE']._serialized_start=160
  _globals['_MEDIARADIOENVELOPE']._serialized_end=391
# @@protoc_insertion_point(module_scope)
