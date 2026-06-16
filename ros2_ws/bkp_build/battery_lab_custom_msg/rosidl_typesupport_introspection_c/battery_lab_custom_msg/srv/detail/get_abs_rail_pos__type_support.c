// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from battery_lab_custom_msg:srv/GetAbsRailPos.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "battery_lab_custom_msg/srv/detail/get_abs_rail_pos__rosidl_typesupport_introspection_c.h"
#include "battery_lab_custom_msg/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "battery_lab_custom_msg/srv/detail/get_abs_rail_pos__functions.h"
#include "battery_lab_custom_msg/srv/detail/get_abs_rail_pos__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void battery_lab_custom_msg__srv__GetAbsRailPos_Request__rosidl_typesupport_introspection_c__GetAbsRailPos_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  battery_lab_custom_msg__srv__GetAbsRailPos_Request__init(message_memory);
}

void battery_lab_custom_msg__srv__GetAbsRailPos_Request__rosidl_typesupport_introspection_c__GetAbsRailPos_Request_fini_function(void * message_memory)
{
  battery_lab_custom_msg__srv__GetAbsRailPos_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember battery_lab_custom_msg__srv__GetAbsRailPos_Request__rosidl_typesupport_introspection_c__GetAbsRailPos_Request_message_member_array[1] = {
  {
    "get",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(battery_lab_custom_msg__srv__GetAbsRailPos_Request, get),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers battery_lab_custom_msg__srv__GetAbsRailPos_Request__rosidl_typesupport_introspection_c__GetAbsRailPos_Request_message_members = {
  "battery_lab_custom_msg__srv",  // message namespace
  "GetAbsRailPos_Request",  // message name
  1,  // number of fields
  sizeof(battery_lab_custom_msg__srv__GetAbsRailPos_Request),
  false,  // has_any_key_member_
  battery_lab_custom_msg__srv__GetAbsRailPos_Request__rosidl_typesupport_introspection_c__GetAbsRailPos_Request_message_member_array,  // message members
  battery_lab_custom_msg__srv__GetAbsRailPos_Request__rosidl_typesupport_introspection_c__GetAbsRailPos_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  battery_lab_custom_msg__srv__GetAbsRailPos_Request__rosidl_typesupport_introspection_c__GetAbsRailPos_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t battery_lab_custom_msg__srv__GetAbsRailPos_Request__rosidl_typesupport_introspection_c__GetAbsRailPos_Request_message_type_support_handle = {
  0,
  &battery_lab_custom_msg__srv__GetAbsRailPos_Request__rosidl_typesupport_introspection_c__GetAbsRailPos_Request_message_members,
  get_message_typesupport_handle_function,
  &battery_lab_custom_msg__srv__GetAbsRailPos_Request__get_type_hash,
  &battery_lab_custom_msg__srv__GetAbsRailPos_Request__get_type_description,
  &battery_lab_custom_msg__srv__GetAbsRailPos_Request__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_battery_lab_custom_msg
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, battery_lab_custom_msg, srv, GetAbsRailPos_Request)() {
  if (!battery_lab_custom_msg__srv__GetAbsRailPos_Request__rosidl_typesupport_introspection_c__GetAbsRailPos_Request_message_type_support_handle.typesupport_identifier) {
    battery_lab_custom_msg__srv__GetAbsRailPos_Request__rosidl_typesupport_introspection_c__GetAbsRailPos_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &battery_lab_custom_msg__srv__GetAbsRailPos_Request__rosidl_typesupport_introspection_c__GetAbsRailPos_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "battery_lab_custom_msg/srv/detail/get_abs_rail_pos__rosidl_typesupport_introspection_c.h"
// already included above
// #include "battery_lab_custom_msg/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "battery_lab_custom_msg/srv/detail/get_abs_rail_pos__functions.h"
// already included above
// #include "battery_lab_custom_msg/srv/detail/get_abs_rail_pos__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void battery_lab_custom_msg__srv__GetAbsRailPos_Response__rosidl_typesupport_introspection_c__GetAbsRailPos_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  battery_lab_custom_msg__srv__GetAbsRailPos_Response__init(message_memory);
}

void battery_lab_custom_msg__srv__GetAbsRailPos_Response__rosidl_typesupport_introspection_c__GetAbsRailPos_Response_fini_function(void * message_memory)
{
  battery_lab_custom_msg__srv__GetAbsRailPos_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember battery_lab_custom_msg__srv__GetAbsRailPos_Response__rosidl_typesupport_introspection_c__GetAbsRailPos_Response_message_member_array[2] = {
  {
    "current_pos",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(battery_lab_custom_msg__srv__GetAbsRailPos_Response, current_pos),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "connected",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(battery_lab_custom_msg__srv__GetAbsRailPos_Response, connected),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers battery_lab_custom_msg__srv__GetAbsRailPos_Response__rosidl_typesupport_introspection_c__GetAbsRailPos_Response_message_members = {
  "battery_lab_custom_msg__srv",  // message namespace
  "GetAbsRailPos_Response",  // message name
  2,  // number of fields
  sizeof(battery_lab_custom_msg__srv__GetAbsRailPos_Response),
  false,  // has_any_key_member_
  battery_lab_custom_msg__srv__GetAbsRailPos_Response__rosidl_typesupport_introspection_c__GetAbsRailPos_Response_message_member_array,  // message members
  battery_lab_custom_msg__srv__GetAbsRailPos_Response__rosidl_typesupport_introspection_c__GetAbsRailPos_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  battery_lab_custom_msg__srv__GetAbsRailPos_Response__rosidl_typesupport_introspection_c__GetAbsRailPos_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t battery_lab_custom_msg__srv__GetAbsRailPos_Response__rosidl_typesupport_introspection_c__GetAbsRailPos_Response_message_type_support_handle = {
  0,
  &battery_lab_custom_msg__srv__GetAbsRailPos_Response__rosidl_typesupport_introspection_c__GetAbsRailPos_Response_message_members,
  get_message_typesupport_handle_function,
  &battery_lab_custom_msg__srv__GetAbsRailPos_Response__get_type_hash,
  &battery_lab_custom_msg__srv__GetAbsRailPos_Response__get_type_description,
  &battery_lab_custom_msg__srv__GetAbsRailPos_Response__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_battery_lab_custom_msg
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, battery_lab_custom_msg, srv, GetAbsRailPos_Response)() {
  if (!battery_lab_custom_msg__srv__GetAbsRailPos_Response__rosidl_typesupport_introspection_c__GetAbsRailPos_Response_message_type_support_handle.typesupport_identifier) {
    battery_lab_custom_msg__srv__GetAbsRailPos_Response__rosidl_typesupport_introspection_c__GetAbsRailPos_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &battery_lab_custom_msg__srv__GetAbsRailPos_Response__rosidl_typesupport_introspection_c__GetAbsRailPos_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "battery_lab_custom_msg/srv/detail/get_abs_rail_pos__rosidl_typesupport_introspection_c.h"
// already included above
// #include "battery_lab_custom_msg/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "battery_lab_custom_msg/srv/detail/get_abs_rail_pos__functions.h"
// already included above
// #include "battery_lab_custom_msg/srv/detail/get_abs_rail_pos__struct.h"


// Include directives for member types
// Member `info`
#include "service_msgs/msg/service_event_info.h"
// Member `info`
#include "service_msgs/msg/detail/service_event_info__rosidl_typesupport_introspection_c.h"
// Member `request`
// Member `response`
#include "battery_lab_custom_msg/srv/get_abs_rail_pos.h"
// Member `request`
// Member `response`
// already included above
// #include "battery_lab_custom_msg/srv/detail/get_abs_rail_pos__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__GetAbsRailPos_Event_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  battery_lab_custom_msg__srv__GetAbsRailPos_Event__init(message_memory);
}

void battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__GetAbsRailPos_Event_fini_function(void * message_memory)
{
  battery_lab_custom_msg__srv__GetAbsRailPos_Event__fini(message_memory);
}

size_t battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__size_function__GetAbsRailPos_Event__request(
  const void * untyped_member)
{
  const battery_lab_custom_msg__srv__GetAbsRailPos_Request__Sequence * member =
    (const battery_lab_custom_msg__srv__GetAbsRailPos_Request__Sequence *)(untyped_member);
  return member->size;
}

const void * battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__get_const_function__GetAbsRailPos_Event__request(
  const void * untyped_member, size_t index)
{
  const battery_lab_custom_msg__srv__GetAbsRailPos_Request__Sequence * member =
    (const battery_lab_custom_msg__srv__GetAbsRailPos_Request__Sequence *)(untyped_member);
  return &member->data[index];
}

void * battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__get_function__GetAbsRailPos_Event__request(
  void * untyped_member, size_t index)
{
  battery_lab_custom_msg__srv__GetAbsRailPos_Request__Sequence * member =
    (battery_lab_custom_msg__srv__GetAbsRailPos_Request__Sequence *)(untyped_member);
  return &member->data[index];
}

void battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__fetch_function__GetAbsRailPos_Event__request(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const battery_lab_custom_msg__srv__GetAbsRailPos_Request * item =
    ((const battery_lab_custom_msg__srv__GetAbsRailPos_Request *)
    battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__get_const_function__GetAbsRailPos_Event__request(untyped_member, index));
  battery_lab_custom_msg__srv__GetAbsRailPos_Request * value =
    (battery_lab_custom_msg__srv__GetAbsRailPos_Request *)(untyped_value);
  *value = *item;
}

void battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__assign_function__GetAbsRailPos_Event__request(
  void * untyped_member, size_t index, const void * untyped_value)
{
  battery_lab_custom_msg__srv__GetAbsRailPos_Request * item =
    ((battery_lab_custom_msg__srv__GetAbsRailPos_Request *)
    battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__get_function__GetAbsRailPos_Event__request(untyped_member, index));
  const battery_lab_custom_msg__srv__GetAbsRailPos_Request * value =
    (const battery_lab_custom_msg__srv__GetAbsRailPos_Request *)(untyped_value);
  *item = *value;
}

bool battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__resize_function__GetAbsRailPos_Event__request(
  void * untyped_member, size_t size)
{
  battery_lab_custom_msg__srv__GetAbsRailPos_Request__Sequence * member =
    (battery_lab_custom_msg__srv__GetAbsRailPos_Request__Sequence *)(untyped_member);
  battery_lab_custom_msg__srv__GetAbsRailPos_Request__Sequence__fini(member);
  return battery_lab_custom_msg__srv__GetAbsRailPos_Request__Sequence__init(member, size);
}

size_t battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__size_function__GetAbsRailPos_Event__response(
  const void * untyped_member)
{
  const battery_lab_custom_msg__srv__GetAbsRailPos_Response__Sequence * member =
    (const battery_lab_custom_msg__srv__GetAbsRailPos_Response__Sequence *)(untyped_member);
  return member->size;
}

const void * battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__get_const_function__GetAbsRailPos_Event__response(
  const void * untyped_member, size_t index)
{
  const battery_lab_custom_msg__srv__GetAbsRailPos_Response__Sequence * member =
    (const battery_lab_custom_msg__srv__GetAbsRailPos_Response__Sequence *)(untyped_member);
  return &member->data[index];
}

void * battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__get_function__GetAbsRailPos_Event__response(
  void * untyped_member, size_t index)
{
  battery_lab_custom_msg__srv__GetAbsRailPos_Response__Sequence * member =
    (battery_lab_custom_msg__srv__GetAbsRailPos_Response__Sequence *)(untyped_member);
  return &member->data[index];
}

void battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__fetch_function__GetAbsRailPos_Event__response(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const battery_lab_custom_msg__srv__GetAbsRailPos_Response * item =
    ((const battery_lab_custom_msg__srv__GetAbsRailPos_Response *)
    battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__get_const_function__GetAbsRailPos_Event__response(untyped_member, index));
  battery_lab_custom_msg__srv__GetAbsRailPos_Response * value =
    (battery_lab_custom_msg__srv__GetAbsRailPos_Response *)(untyped_value);
  *value = *item;
}

void battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__assign_function__GetAbsRailPos_Event__response(
  void * untyped_member, size_t index, const void * untyped_value)
{
  battery_lab_custom_msg__srv__GetAbsRailPos_Response * item =
    ((battery_lab_custom_msg__srv__GetAbsRailPos_Response *)
    battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__get_function__GetAbsRailPos_Event__response(untyped_member, index));
  const battery_lab_custom_msg__srv__GetAbsRailPos_Response * value =
    (const battery_lab_custom_msg__srv__GetAbsRailPos_Response *)(untyped_value);
  *item = *value;
}

bool battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__resize_function__GetAbsRailPos_Event__response(
  void * untyped_member, size_t size)
{
  battery_lab_custom_msg__srv__GetAbsRailPos_Response__Sequence * member =
    (battery_lab_custom_msg__srv__GetAbsRailPos_Response__Sequence *)(untyped_member);
  battery_lab_custom_msg__srv__GetAbsRailPos_Response__Sequence__fini(member);
  return battery_lab_custom_msg__srv__GetAbsRailPos_Response__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__GetAbsRailPos_Event_message_member_array[3] = {
  {
    "info",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(battery_lab_custom_msg__srv__GetAbsRailPos_Event, info),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "request",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    true,  // is array
    1,  // array size
    true,  // is upper bound
    offsetof(battery_lab_custom_msg__srv__GetAbsRailPos_Event, request),  // bytes offset in struct
    NULL,  // default value
    battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__size_function__GetAbsRailPos_Event__request,  // size() function pointer
    battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__get_const_function__GetAbsRailPos_Event__request,  // get_const(index) function pointer
    battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__get_function__GetAbsRailPos_Event__request,  // get(index) function pointer
    battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__fetch_function__GetAbsRailPos_Event__request,  // fetch(index, &value) function pointer
    battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__assign_function__GetAbsRailPos_Event__request,  // assign(index, value) function pointer
    battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__resize_function__GetAbsRailPos_Event__request  // resize(index) function pointer
  },
  {
    "response",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    true,  // is array
    1,  // array size
    true,  // is upper bound
    offsetof(battery_lab_custom_msg__srv__GetAbsRailPos_Event, response),  // bytes offset in struct
    NULL,  // default value
    battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__size_function__GetAbsRailPos_Event__response,  // size() function pointer
    battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__get_const_function__GetAbsRailPos_Event__response,  // get_const(index) function pointer
    battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__get_function__GetAbsRailPos_Event__response,  // get(index) function pointer
    battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__fetch_function__GetAbsRailPos_Event__response,  // fetch(index, &value) function pointer
    battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__assign_function__GetAbsRailPos_Event__response,  // assign(index, value) function pointer
    battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__resize_function__GetAbsRailPos_Event__response  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__GetAbsRailPos_Event_message_members = {
  "battery_lab_custom_msg__srv",  // message namespace
  "GetAbsRailPos_Event",  // message name
  3,  // number of fields
  sizeof(battery_lab_custom_msg__srv__GetAbsRailPos_Event),
  false,  // has_any_key_member_
  battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__GetAbsRailPos_Event_message_member_array,  // message members
  battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__GetAbsRailPos_Event_init_function,  // function to initialize message memory (memory has to be allocated)
  battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__GetAbsRailPos_Event_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__GetAbsRailPos_Event_message_type_support_handle = {
  0,
  &battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__GetAbsRailPos_Event_message_members,
  get_message_typesupport_handle_function,
  &battery_lab_custom_msg__srv__GetAbsRailPos_Event__get_type_hash,
  &battery_lab_custom_msg__srv__GetAbsRailPos_Event__get_type_description,
  &battery_lab_custom_msg__srv__GetAbsRailPos_Event__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_battery_lab_custom_msg
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, battery_lab_custom_msg, srv, GetAbsRailPos_Event)() {
  battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__GetAbsRailPos_Event_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, service_msgs, msg, ServiceEventInfo)();
  battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__GetAbsRailPos_Event_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, battery_lab_custom_msg, srv, GetAbsRailPos_Request)();
  battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__GetAbsRailPos_Event_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, battery_lab_custom_msg, srv, GetAbsRailPos_Response)();
  if (!battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__GetAbsRailPos_Event_message_type_support_handle.typesupport_identifier) {
    battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__GetAbsRailPos_Event_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__GetAbsRailPos_Event_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "battery_lab_custom_msg/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "battery_lab_custom_msg/srv/detail/get_abs_rail_pos__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers battery_lab_custom_msg__srv__detail__get_abs_rail_pos__rosidl_typesupport_introspection_c__GetAbsRailPos_service_members = {
  "battery_lab_custom_msg__srv",  // service namespace
  "GetAbsRailPos",  // service name
  // the following fields are initialized below on first access
  NULL,  // request message
  // battery_lab_custom_msg__srv__detail__get_abs_rail_pos__rosidl_typesupport_introspection_c__GetAbsRailPos_Request_message_type_support_handle,
  NULL,  // response message
  // battery_lab_custom_msg__srv__detail__get_abs_rail_pos__rosidl_typesupport_introspection_c__GetAbsRailPos_Response_message_type_support_handle
  NULL  // event_message
  // battery_lab_custom_msg__srv__detail__get_abs_rail_pos__rosidl_typesupport_introspection_c__GetAbsRailPos_Response_message_type_support_handle
};


static rosidl_service_type_support_t battery_lab_custom_msg__srv__detail__get_abs_rail_pos__rosidl_typesupport_introspection_c__GetAbsRailPos_service_type_support_handle = {
  0,
  &battery_lab_custom_msg__srv__detail__get_abs_rail_pos__rosidl_typesupport_introspection_c__GetAbsRailPos_service_members,
  get_service_typesupport_handle_function,
  &battery_lab_custom_msg__srv__GetAbsRailPos_Request__rosidl_typesupport_introspection_c__GetAbsRailPos_Request_message_type_support_handle,
  &battery_lab_custom_msg__srv__GetAbsRailPos_Response__rosidl_typesupport_introspection_c__GetAbsRailPos_Response_message_type_support_handle,
  &battery_lab_custom_msg__srv__GetAbsRailPos_Event__rosidl_typesupport_introspection_c__GetAbsRailPos_Event_message_type_support_handle,
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    battery_lab_custom_msg,
    srv,
    GetAbsRailPos
  ),
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    battery_lab_custom_msg,
    srv,
    GetAbsRailPos
  ),
  &battery_lab_custom_msg__srv__GetAbsRailPos__get_type_hash,
  &battery_lab_custom_msg__srv__GetAbsRailPos__get_type_description,
  &battery_lab_custom_msg__srv__GetAbsRailPos__get_type_description_sources,
};

// Forward declaration of message type support functions for service members
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, battery_lab_custom_msg, srv, GetAbsRailPos_Request)(void);

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, battery_lab_custom_msg, srv, GetAbsRailPos_Response)(void);

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, battery_lab_custom_msg, srv, GetAbsRailPos_Event)(void);

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_battery_lab_custom_msg
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, battery_lab_custom_msg, srv, GetAbsRailPos)(void) {
  if (!battery_lab_custom_msg__srv__detail__get_abs_rail_pos__rosidl_typesupport_introspection_c__GetAbsRailPos_service_type_support_handle.typesupport_identifier) {
    battery_lab_custom_msg__srv__detail__get_abs_rail_pos__rosidl_typesupport_introspection_c__GetAbsRailPos_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)battery_lab_custom_msg__srv__detail__get_abs_rail_pos__rosidl_typesupport_introspection_c__GetAbsRailPos_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, battery_lab_custom_msg, srv, GetAbsRailPos_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, battery_lab_custom_msg, srv, GetAbsRailPos_Response)()->data;
  }
  if (!service_members->event_members_) {
    service_members->event_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, battery_lab_custom_msg, srv, GetAbsRailPos_Event)()->data;
  }

  return &battery_lab_custom_msg__srv__detail__get_abs_rail_pos__rosidl_typesupport_introspection_c__GetAbsRailPos_service_type_support_handle;
}
