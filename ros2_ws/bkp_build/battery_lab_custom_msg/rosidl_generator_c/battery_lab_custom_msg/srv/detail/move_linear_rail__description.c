// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from battery_lab_custom_msg:srv/MoveLinearRail.idl
// generated code does not contain a copyright notice

#include "battery_lab_custom_msg/srv/detail/move_linear_rail__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
const rosidl_type_hash_t *
battery_lab_custom_msg__srv__MoveLinearRail__get_type_hash(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x4b, 0x3d, 0x38, 0x0f, 0xf3, 0x62, 0x72, 0xfb,
      0x4d, 0xae, 0xd8, 0x53, 0xbd, 0xb6, 0xdf, 0x91,
      0x3f, 0x34, 0x6b, 0xac, 0xdd, 0x2b, 0xd1, 0x28,
      0xd1, 0x21, 0xec, 0xb1, 0x99, 0x7d, 0x0f, 0x48,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
const rosidl_type_hash_t *
battery_lab_custom_msg__srv__MoveLinearRail_Request__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x4c, 0x5a, 0xf1, 0xe8, 0xf9, 0xd9, 0x23, 0x5c,
      0x09, 0xa1, 0xfc, 0xdf, 0xd6, 0x6d, 0xa1, 0x2b,
      0xec, 0x48, 0x2a, 0xaa, 0xee, 0xeb, 0x76, 0x84,
      0xd4, 0x0a, 0x65, 0xf0, 0xab, 0x14, 0x55, 0x79,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
const rosidl_type_hash_t *
battery_lab_custom_msg__srv__MoveLinearRail_Response__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x4a, 0x30, 0x1f, 0xfb, 0x60, 0xff, 0x8b, 0x7f,
      0x31, 0x2c, 0x50, 0x13, 0x75, 0xaf, 0xbb, 0xbe,
      0xd3, 0x11, 0xd2, 0x35, 0xf1, 0x97, 0xd1, 0x12,
      0x5b, 0x17, 0xc6, 0x97, 0x20, 0x9c, 0x0a, 0x18,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
const rosidl_type_hash_t *
battery_lab_custom_msg__srv__MoveLinearRail_Event__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xd3, 0xf4, 0xa0, 0x50, 0xf2, 0xa2, 0x18, 0x59,
      0x84, 0x31, 0x80, 0x0d, 0xe6, 0xca, 0x7b, 0x13,
      0x37, 0x0a, 0x18, 0x17, 0xcb, 0x80, 0x82, 0xa4,
      0x4d, 0xcc, 0xc8, 0x08, 0xb1, 0x48, 0xa2, 0x17,
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

static char battery_lab_custom_msg__srv__MoveLinearRail__TYPE_NAME[] = "battery_lab_custom_msg/srv/MoveLinearRail";
static char battery_lab_custom_msg__srv__MoveLinearRail_Event__TYPE_NAME[] = "battery_lab_custom_msg/srv/MoveLinearRail_Event";
static char battery_lab_custom_msg__srv__MoveLinearRail_Request__TYPE_NAME[] = "battery_lab_custom_msg/srv/MoveLinearRail_Request";
static char battery_lab_custom_msg__srv__MoveLinearRail_Response__TYPE_NAME[] = "battery_lab_custom_msg/srv/MoveLinearRail_Response";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";
static char service_msgs__msg__ServiceEventInfo__TYPE_NAME[] = "service_msgs/msg/ServiceEventInfo";

// Define type names, field names, and default values
static char battery_lab_custom_msg__srv__MoveLinearRail__FIELD_NAME__request_message[] = "request_message";
static char battery_lab_custom_msg__srv__MoveLinearRail__FIELD_NAME__response_message[] = "response_message";
static char battery_lab_custom_msg__srv__MoveLinearRail__FIELD_NAME__event_message[] = "event_message";

static rosidl_runtime_c__type_description__Field battery_lab_custom_msg__srv__MoveLinearRail__FIELDS[] = {
  {
    {battery_lab_custom_msg__srv__MoveLinearRail__FIELD_NAME__request_message, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {battery_lab_custom_msg__srv__MoveLinearRail_Request__TYPE_NAME, 49, 49},
    },
    {NULL, 0, 0},
  },
  {
    {battery_lab_custom_msg__srv__MoveLinearRail__FIELD_NAME__response_message, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {battery_lab_custom_msg__srv__MoveLinearRail_Response__TYPE_NAME, 50, 50},
    },
    {NULL, 0, 0},
  },
  {
    {battery_lab_custom_msg__srv__MoveLinearRail__FIELD_NAME__event_message, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {battery_lab_custom_msg__srv__MoveLinearRail_Event__TYPE_NAME, 47, 47},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription battery_lab_custom_msg__srv__MoveLinearRail__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {battery_lab_custom_msg__srv__MoveLinearRail_Event__TYPE_NAME, 47, 47},
    {NULL, 0, 0},
  },
  {
    {battery_lab_custom_msg__srv__MoveLinearRail_Request__TYPE_NAME, 49, 49},
    {NULL, 0, 0},
  },
  {
    {battery_lab_custom_msg__srv__MoveLinearRail_Response__TYPE_NAME, 50, 50},
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
battery_lab_custom_msg__srv__MoveLinearRail__get_type_description(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {battery_lab_custom_msg__srv__MoveLinearRail__TYPE_NAME, 41, 41},
      {battery_lab_custom_msg__srv__MoveLinearRail__FIELDS, 3, 3},
    },
    {battery_lab_custom_msg__srv__MoveLinearRail__REFERENCED_TYPE_DESCRIPTIONS, 5, 5},
  };
  if (!constructed) {
    description.referenced_type_descriptions.data[0].fields = battery_lab_custom_msg__srv__MoveLinearRail_Event__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[1].fields = battery_lab_custom_msg__srv__MoveLinearRail_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[2].fields = battery_lab_custom_msg__srv__MoveLinearRail_Response__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[3].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[4].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char battery_lab_custom_msg__srv__MoveLinearRail_Request__FIELD_NAME__target_position[] = "target_position";

static rosidl_runtime_c__type_description__Field battery_lab_custom_msg__srv__MoveLinearRail_Request__FIELDS[] = {
  {
    {battery_lab_custom_msg__srv__MoveLinearRail_Request__FIELD_NAME__target_position, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
battery_lab_custom_msg__srv__MoveLinearRail_Request__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {battery_lab_custom_msg__srv__MoveLinearRail_Request__TYPE_NAME, 49, 49},
      {battery_lab_custom_msg__srv__MoveLinearRail_Request__FIELDS, 1, 1},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char battery_lab_custom_msg__srv__MoveLinearRail_Response__FIELD_NAME__success[] = "success";

static rosidl_runtime_c__type_description__Field battery_lab_custom_msg__srv__MoveLinearRail_Response__FIELDS[] = {
  {
    {battery_lab_custom_msg__srv__MoveLinearRail_Response__FIELD_NAME__success, 7, 7},
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
battery_lab_custom_msg__srv__MoveLinearRail_Response__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {battery_lab_custom_msg__srv__MoveLinearRail_Response__TYPE_NAME, 50, 50},
      {battery_lab_custom_msg__srv__MoveLinearRail_Response__FIELDS, 1, 1},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char battery_lab_custom_msg__srv__MoveLinearRail_Event__FIELD_NAME__info[] = "info";
static char battery_lab_custom_msg__srv__MoveLinearRail_Event__FIELD_NAME__request[] = "request";
static char battery_lab_custom_msg__srv__MoveLinearRail_Event__FIELD_NAME__response[] = "response";

static rosidl_runtime_c__type_description__Field battery_lab_custom_msg__srv__MoveLinearRail_Event__FIELDS[] = {
  {
    {battery_lab_custom_msg__srv__MoveLinearRail_Event__FIELD_NAME__info, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    },
    {NULL, 0, 0},
  },
  {
    {battery_lab_custom_msg__srv__MoveLinearRail_Event__FIELD_NAME__request, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {battery_lab_custom_msg__srv__MoveLinearRail_Request__TYPE_NAME, 49, 49},
    },
    {NULL, 0, 0},
  },
  {
    {battery_lab_custom_msg__srv__MoveLinearRail_Event__FIELD_NAME__response, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {battery_lab_custom_msg__srv__MoveLinearRail_Response__TYPE_NAME, 50, 50},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription battery_lab_custom_msg__srv__MoveLinearRail_Event__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {battery_lab_custom_msg__srv__MoveLinearRail_Request__TYPE_NAME, 49, 49},
    {NULL, 0, 0},
  },
  {
    {battery_lab_custom_msg__srv__MoveLinearRail_Response__TYPE_NAME, 50, 50},
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
battery_lab_custom_msg__srv__MoveLinearRail_Event__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {battery_lab_custom_msg__srv__MoveLinearRail_Event__TYPE_NAME, 47, 47},
      {battery_lab_custom_msg__srv__MoveLinearRail_Event__FIELDS, 3, 3},
    },
    {battery_lab_custom_msg__srv__MoveLinearRail_Event__REFERENCED_TYPE_DESCRIPTIONS, 4, 4},
  };
  if (!constructed) {
    description.referenced_type_descriptions.data[0].fields = battery_lab_custom_msg__srv__MoveLinearRail_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[1].fields = battery_lab_custom_msg__srv__MoveLinearRail_Response__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[2].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[3].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "float32 target_position\n"
  "---\n"
  "bool success";

static char srv_encoding[] = "srv";
static char implicit_encoding[] = "implicit";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
battery_lab_custom_msg__srv__MoveLinearRail__get_individual_type_description_source(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {battery_lab_custom_msg__srv__MoveLinearRail__TYPE_NAME, 41, 41},
    {srv_encoding, 3, 3},
    {toplevel_type_raw_source, 40, 40},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
battery_lab_custom_msg__srv__MoveLinearRail_Request__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {battery_lab_custom_msg__srv__MoveLinearRail_Request__TYPE_NAME, 49, 49},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
battery_lab_custom_msg__srv__MoveLinearRail_Response__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {battery_lab_custom_msg__srv__MoveLinearRail_Response__TYPE_NAME, 50, 50},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
battery_lab_custom_msg__srv__MoveLinearRail_Event__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {battery_lab_custom_msg__srv__MoveLinearRail_Event__TYPE_NAME, 47, 47},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
battery_lab_custom_msg__srv__MoveLinearRail__get_type_description_sources(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[6];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 6, 6};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *battery_lab_custom_msg__srv__MoveLinearRail__get_individual_type_description_source(NULL),
    sources[1] = *battery_lab_custom_msg__srv__MoveLinearRail_Event__get_individual_type_description_source(NULL);
    sources[2] = *battery_lab_custom_msg__srv__MoveLinearRail_Request__get_individual_type_description_source(NULL);
    sources[3] = *battery_lab_custom_msg__srv__MoveLinearRail_Response__get_individual_type_description_source(NULL);
    sources[4] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[5] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
battery_lab_custom_msg__srv__MoveLinearRail_Request__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *battery_lab_custom_msg__srv__MoveLinearRail_Request__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
battery_lab_custom_msg__srv__MoveLinearRail_Response__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *battery_lab_custom_msg__srv__MoveLinearRail_Response__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
battery_lab_custom_msg__srv__MoveLinearRail_Event__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[5];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 5, 5};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *battery_lab_custom_msg__srv__MoveLinearRail_Event__get_individual_type_description_source(NULL),
    sources[1] = *battery_lab_custom_msg__srv__MoveLinearRail_Request__get_individual_type_description_source(NULL);
    sources[2] = *battery_lab_custom_msg__srv__MoveLinearRail_Response__get_individual_type_description_source(NULL);
    sources[3] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[4] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
