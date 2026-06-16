// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from battery_lab_custom_msg:srv/GetAbsRailPos.idl
// generated code does not contain a copyright notice

#include "battery_lab_custom_msg/srv/detail/get_abs_rail_pos__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
const rosidl_type_hash_t *
battery_lab_custom_msg__srv__GetAbsRailPos__get_type_hash(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x4d, 0xcd, 0x90, 0xe0, 0x67, 0x61, 0xb7, 0xb8,
      0x4a, 0x1b, 0xb2, 0xab, 0x24, 0xe1, 0xe1, 0x04,
      0xf1, 0x50, 0xae, 0x56, 0xc1, 0x62, 0x88, 0xf8,
      0xc1, 0x70, 0x4b, 0x72, 0x5d, 0x80, 0xd0, 0xcd,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
const rosidl_type_hash_t *
battery_lab_custom_msg__srv__GetAbsRailPos_Request__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x26, 0xa1, 0x1c, 0x7a, 0xc6, 0x40, 0x98, 0x7b,
      0xb3, 0x20, 0xd4, 0x5e, 0x9b, 0x59, 0x5f, 0xae,
      0x83, 0xea, 0x87, 0x49, 0xef, 0xd1, 0x10, 0xd2,
      0xae, 0x87, 0xda, 0x4d, 0xda, 0xc7, 0x1c, 0x7f,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
const rosidl_type_hash_t *
battery_lab_custom_msg__srv__GetAbsRailPos_Response__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x0b, 0xda, 0xee, 0xe0, 0x82, 0x6c, 0x02, 0x35,
      0x70, 0x55, 0xf8, 0x8f, 0x1f, 0x8f, 0x69, 0x55,
      0xe7, 0x19, 0x1a, 0x21, 0x15, 0xa4, 0x83, 0x20,
      0xaf, 0x85, 0xda, 0x5b, 0x0f, 0x52, 0xc8, 0xa6,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
const rosidl_type_hash_t *
battery_lab_custom_msg__srv__GetAbsRailPos_Event__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x30, 0x7c, 0xea, 0xf2, 0xa5, 0x19, 0xe8, 0x79,
      0x7d, 0xb3, 0xa2, 0x9c, 0xb0, 0x57, 0x2f, 0xac,
      0x43, 0xc9, 0x07, 0xf2, 0xe2, 0xa6, 0x5c, 0x09,
      0xef, 0xdb, 0x8a, 0x15, 0xae, 0x4d, 0x38, 0xc7,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "builtin_interfaces/msg/detail/time__functions.h"
#include "service_msgs/msg/detail/service_event_info__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t builtin_interfaces__msg__Time__EXPECTED_HASH = {1, {
    0xb1, 0x06, 0x23, 0x5e, 0x25, 0xa4, 0xc5, 0xed,
    0x35, 0x09, 0x8a, 0xa0, 0xa6, 0x1a, 0x3e, 0xe9,
    0xc9, 0xb1, 0x8d, 0x19, 0x7f, 0x39, 0x8b, 0x0e,
    0x42, 0x06, 0xce, 0xa9, 0xac, 0xf9, 0xc1, 0x97,
  }};
static const rosidl_type_hash_t service_msgs__msg__ServiceEventInfo__EXPECTED_HASH = {1, {
    0x41, 0xbc, 0xbb, 0xe0, 0x7a, 0x75, 0xc9, 0xb5,
    0x2b, 0xc9, 0x6b, 0xfd, 0x5c, 0x24, 0xd7, 0xf0,
    0xfc, 0x0a, 0x08, 0xc0, 0xcb, 0x79, 0x21, 0xb3,
    0x37, 0x3c, 0x57, 0x32, 0x34, 0x5a, 0x6f, 0x45,
  }};
#endif

static char battery_lab_custom_msg__srv__GetAbsRailPos__TYPE_NAME[] = "battery_lab_custom_msg/srv/GetAbsRailPos";
static char battery_lab_custom_msg__srv__GetAbsRailPos_Event__TYPE_NAME[] = "battery_lab_custom_msg/srv/GetAbsRailPos_Event";
static char battery_lab_custom_msg__srv__GetAbsRailPos_Request__TYPE_NAME[] = "battery_lab_custom_msg/srv/GetAbsRailPos_Request";
static char battery_lab_custom_msg__srv__GetAbsRailPos_Response__TYPE_NAME[] = "battery_lab_custom_msg/srv/GetAbsRailPos_Response";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";
static char service_msgs__msg__ServiceEventInfo__TYPE_NAME[] = "service_msgs/msg/ServiceEventInfo";

// Define type names, field names, and default values
static char battery_lab_custom_msg__srv__GetAbsRailPos__FIELD_NAME__request_message[] = "request_message";
static char battery_lab_custom_msg__srv__GetAbsRailPos__FIELD_NAME__response_message[] = "response_message";
static char battery_lab_custom_msg__srv__GetAbsRailPos__FIELD_NAME__event_message[] = "event_message";

static rosidl_runtime_c__type_description__Field battery_lab_custom_msg__srv__GetAbsRailPos__FIELDS[] = {
  {
    {battery_lab_custom_msg__srv__GetAbsRailPos__FIELD_NAME__request_message, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {battery_lab_custom_msg__srv__GetAbsRailPos_Request__TYPE_NAME, 48, 48},
    },
    {NULL, 0, 0},
  },
  {
    {battery_lab_custom_msg__srv__GetAbsRailPos__FIELD_NAME__response_message, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {battery_lab_custom_msg__srv__GetAbsRailPos_Response__TYPE_NAME, 49, 49},
    },
    {NULL, 0, 0},
  },
  {
    {battery_lab_custom_msg__srv__GetAbsRailPos__FIELD_NAME__event_message, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {battery_lab_custom_msg__srv__GetAbsRailPos_Event__TYPE_NAME, 46, 46},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription battery_lab_custom_msg__srv__GetAbsRailPos__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {battery_lab_custom_msg__srv__GetAbsRailPos_Event__TYPE_NAME, 46, 46},
    {NULL, 0, 0},
  },
  {
    {battery_lab_custom_msg__srv__GetAbsRailPos_Request__TYPE_NAME, 48, 48},
    {NULL, 0, 0},
  },
  {
    {battery_lab_custom_msg__srv__GetAbsRailPos_Response__TYPE_NAME, 49, 49},
    {NULL, 0, 0},
  },
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
battery_lab_custom_msg__srv__GetAbsRailPos__get_type_description(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {battery_lab_custom_msg__srv__GetAbsRailPos__TYPE_NAME, 40, 40},
      {battery_lab_custom_msg__srv__GetAbsRailPos__FIELDS, 3, 3},
    },
    {battery_lab_custom_msg__srv__GetAbsRailPos__REFERENCED_TYPE_DESCRIPTIONS, 5, 5},
  };
  if (!constructed) {
    description.referenced_type_descriptions.data[0].fields = battery_lab_custom_msg__srv__GetAbsRailPos_Event__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[1].fields = battery_lab_custom_msg__srv__GetAbsRailPos_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[2].fields = battery_lab_custom_msg__srv__GetAbsRailPos_Response__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[3].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[4].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char battery_lab_custom_msg__srv__GetAbsRailPos_Request__FIELD_NAME__get[] = "get";

static rosidl_runtime_c__type_description__Field battery_lab_custom_msg__srv__GetAbsRailPos_Request__FIELDS[] = {
  {
    {battery_lab_custom_msg__srv__GetAbsRailPos_Request__FIELD_NAME__get, 3, 3},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
battery_lab_custom_msg__srv__GetAbsRailPos_Request__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {battery_lab_custom_msg__srv__GetAbsRailPos_Request__TYPE_NAME, 48, 48},
      {battery_lab_custom_msg__srv__GetAbsRailPos_Request__FIELDS, 1, 1},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char battery_lab_custom_msg__srv__GetAbsRailPos_Response__FIELD_NAME__current_pos[] = "current_pos";
static char battery_lab_custom_msg__srv__GetAbsRailPos_Response__FIELD_NAME__connected[] = "connected";

static rosidl_runtime_c__type_description__Field battery_lab_custom_msg__srv__GetAbsRailPos_Response__FIELDS[] = {
  {
    {battery_lab_custom_msg__srv__GetAbsRailPos_Response__FIELD_NAME__current_pos, 11, 11},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {battery_lab_custom_msg__srv__GetAbsRailPos_Response__FIELD_NAME__connected, 9, 9},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
battery_lab_custom_msg__srv__GetAbsRailPos_Response__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {battery_lab_custom_msg__srv__GetAbsRailPos_Response__TYPE_NAME, 49, 49},
      {battery_lab_custom_msg__srv__GetAbsRailPos_Response__FIELDS, 2, 2},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char battery_lab_custom_msg__srv__GetAbsRailPos_Event__FIELD_NAME__info[] = "info";
static char battery_lab_custom_msg__srv__GetAbsRailPos_Event__FIELD_NAME__request[] = "request";
static char battery_lab_custom_msg__srv__GetAbsRailPos_Event__FIELD_NAME__response[] = "response";

static rosidl_runtime_c__type_description__Field battery_lab_custom_msg__srv__GetAbsRailPos_Event__FIELDS[] = {
  {
    {battery_lab_custom_msg__srv__GetAbsRailPos_Event__FIELD_NAME__info, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    },
    {NULL, 0, 0},
  },
  {
    {battery_lab_custom_msg__srv__GetAbsRailPos_Event__FIELD_NAME__request, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {battery_lab_custom_msg__srv__GetAbsRailPos_Request__TYPE_NAME, 48, 48},
    },
    {NULL, 0, 0},
  },
  {
    {battery_lab_custom_msg__srv__GetAbsRailPos_Event__FIELD_NAME__response, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {battery_lab_custom_msg__srv__GetAbsRailPos_Response__TYPE_NAME, 49, 49},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription battery_lab_custom_msg__srv__GetAbsRailPos_Event__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {battery_lab_custom_msg__srv__GetAbsRailPos_Request__TYPE_NAME, 48, 48},
    {NULL, 0, 0},
  },
  {
    {battery_lab_custom_msg__srv__GetAbsRailPos_Response__TYPE_NAME, 49, 49},
    {NULL, 0, 0},
  },
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
battery_lab_custom_msg__srv__GetAbsRailPos_Event__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {battery_lab_custom_msg__srv__GetAbsRailPos_Event__TYPE_NAME, 46, 46},
      {battery_lab_custom_msg__srv__GetAbsRailPos_Event__FIELDS, 3, 3},
    },
    {battery_lab_custom_msg__srv__GetAbsRailPos_Event__REFERENCED_TYPE_DESCRIPTIONS, 4, 4},
  };
  if (!constructed) {
    description.referenced_type_descriptions.data[0].fields = battery_lab_custom_msg__srv__GetAbsRailPos_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[1].fields = battery_lab_custom_msg__srv__GetAbsRailPos_Response__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[2].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[3].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "int32 get\n"
  "---\n"
  "float32 current_pos\n"
  "bool connected";

static char srv_encoding[] = "srv";
static char implicit_encoding[] = "implicit";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
battery_lab_custom_msg__srv__GetAbsRailPos__get_individual_type_description_source(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {battery_lab_custom_msg__srv__GetAbsRailPos__TYPE_NAME, 40, 40},
    {srv_encoding, 3, 3},
    {toplevel_type_raw_source, 48, 48},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
battery_lab_custom_msg__srv__GetAbsRailPos_Request__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {battery_lab_custom_msg__srv__GetAbsRailPos_Request__TYPE_NAME, 48, 48},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
battery_lab_custom_msg__srv__GetAbsRailPos_Response__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {battery_lab_custom_msg__srv__GetAbsRailPos_Response__TYPE_NAME, 49, 49},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
battery_lab_custom_msg__srv__GetAbsRailPos_Event__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {battery_lab_custom_msg__srv__GetAbsRailPos_Event__TYPE_NAME, 46, 46},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
battery_lab_custom_msg__srv__GetAbsRailPos__get_type_description_sources(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[6];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 6, 6};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *battery_lab_custom_msg__srv__GetAbsRailPos__get_individual_type_description_source(NULL),
    sources[1] = *battery_lab_custom_msg__srv__GetAbsRailPos_Event__get_individual_type_description_source(NULL);
    sources[2] = *battery_lab_custom_msg__srv__GetAbsRailPos_Request__get_individual_type_description_source(NULL);
    sources[3] = *battery_lab_custom_msg__srv__GetAbsRailPos_Response__get_individual_type_description_source(NULL);
    sources[4] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[5] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
battery_lab_custom_msg__srv__GetAbsRailPos_Request__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *battery_lab_custom_msg__srv__GetAbsRailPos_Request__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
battery_lab_custom_msg__srv__GetAbsRailPos_Response__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *battery_lab_custom_msg__srv__GetAbsRailPos_Response__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
battery_lab_custom_msg__srv__GetAbsRailPos_Event__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[5];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 5, 5};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *battery_lab_custom_msg__srv__GetAbsRailPos_Event__get_individual_type_description_source(NULL),
    sources[1] = *battery_lab_custom_msg__srv__GetAbsRailPos_Request__get_individual_type_description_source(NULL);
    sources[2] = *battery_lab_custom_msg__srv__GetAbsRailPos_Response__get_individual_type_description_source(NULL);
    sources[3] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[4] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
