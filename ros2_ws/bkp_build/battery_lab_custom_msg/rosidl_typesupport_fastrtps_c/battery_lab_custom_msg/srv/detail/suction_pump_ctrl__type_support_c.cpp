// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from battery_lab_custom_msg:srv/SuctionPumpCtrl.idl
// generated code does not contain a copyright notice
#include "battery_lab_custom_msg/srv/detail/suction_pump_ctrl__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <cstddef>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/serialization_helpers.hpp"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "battery_lab_custom_msg/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "battery_lab_custom_msg/srv/detail/suction_pump_ctrl__struct.h"
#include "battery_lab_custom_msg/srv/detail/suction_pump_ctrl__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "rosidl_runtime_c/string.h"  // command
#include "rosidl_runtime_c/string_functions.h"  // command

// forward declare type support functions


using _SuctionPumpCtrl_Request__ros_msg_type = battery_lab_custom_msg__srv__SuctionPumpCtrl_Request;


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_battery_lab_custom_msg
bool cdr_serialize_battery_lab_custom_msg__srv__SuctionPumpCtrl_Request(
  const battery_lab_custom_msg__srv__SuctionPumpCtrl_Request * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: command
  {
    const rosidl_runtime_c__String * str = &ros_message->command;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_battery_lab_custom_msg
bool cdr_deserialize_battery_lab_custom_msg__srv__SuctionPumpCtrl_Request(
  eprosima::fastcdr::Cdr & cdr,
  battery_lab_custom_msg__srv__SuctionPumpCtrl_Request * ros_message)
{
  // Field name: command
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->command.data) {
      rosidl_runtime_c__String__init(&ros_message->command);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->command,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'command'\n");
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_battery_lab_custom_msg
size_t get_serialized_size_battery_lab_custom_msg__srv__SuctionPumpCtrl_Request(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _SuctionPumpCtrl_Request__ros_msg_type * ros_message = static_cast<const _SuctionPumpCtrl_Request__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: command
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->command.size + 1);

  return current_alignment - initial_alignment;
}


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_battery_lab_custom_msg
size_t max_serialized_size_battery_lab_custom_msg__srv__SuctionPumpCtrl_Request(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // Field name: command
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }


  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = battery_lab_custom_msg__srv__SuctionPumpCtrl_Request;
    is_plain =
      (
      offsetof(DataType, command) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_battery_lab_custom_msg
bool cdr_serialize_key_battery_lab_custom_msg__srv__SuctionPumpCtrl_Request(
  const battery_lab_custom_msg__srv__SuctionPumpCtrl_Request * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: command
  {
    const rosidl_runtime_c__String * str = &ros_message->command;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_battery_lab_custom_msg
size_t get_serialized_size_key_battery_lab_custom_msg__srv__SuctionPumpCtrl_Request(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _SuctionPumpCtrl_Request__ros_msg_type * ros_message = static_cast<const _SuctionPumpCtrl_Request__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;

  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: command
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->command.size + 1);

  return current_alignment - initial_alignment;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_battery_lab_custom_msg
size_t max_serialized_size_key_battery_lab_custom_msg__srv__SuctionPumpCtrl_Request(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;
  // Field name: command
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = battery_lab_custom_msg__srv__SuctionPumpCtrl_Request;
    is_plain =
      (
      offsetof(DataType, command) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}


static bool _SuctionPumpCtrl_Request__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const battery_lab_custom_msg__srv__SuctionPumpCtrl_Request * ros_message = static_cast<const battery_lab_custom_msg__srv__SuctionPumpCtrl_Request *>(untyped_ros_message);
  (void)ros_message;
  return cdr_serialize_battery_lab_custom_msg__srv__SuctionPumpCtrl_Request(ros_message, cdr);
}

static bool _SuctionPumpCtrl_Request__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  battery_lab_custom_msg__srv__SuctionPumpCtrl_Request * ros_message = static_cast<battery_lab_custom_msg__srv__SuctionPumpCtrl_Request *>(untyped_ros_message);
  (void)ros_message;
  return cdr_deserialize_battery_lab_custom_msg__srv__SuctionPumpCtrl_Request(cdr, ros_message);
}

static uint32_t _SuctionPumpCtrl_Request__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_battery_lab_custom_msg__srv__SuctionPumpCtrl_Request(
      untyped_ros_message, 0));
}

static size_t _SuctionPumpCtrl_Request__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_battery_lab_custom_msg__srv__SuctionPumpCtrl_Request(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_SuctionPumpCtrl_Request = {
  "battery_lab_custom_msg::srv",
  "SuctionPumpCtrl_Request",
  _SuctionPumpCtrl_Request__cdr_serialize,
  _SuctionPumpCtrl_Request__cdr_deserialize,
  _SuctionPumpCtrl_Request__get_serialized_size,
  _SuctionPumpCtrl_Request__max_serialized_size,
  nullptr
};

static rosidl_message_type_support_t _SuctionPumpCtrl_Request__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_SuctionPumpCtrl_Request,
  get_message_typesupport_handle_function,
  &battery_lab_custom_msg__srv__SuctionPumpCtrl_Request__get_type_hash,
  &battery_lab_custom_msg__srv__SuctionPumpCtrl_Request__get_type_description,
  &battery_lab_custom_msg__srv__SuctionPumpCtrl_Request__get_type_description_sources,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, battery_lab_custom_msg, srv, SuctionPumpCtrl_Request)() {
  return &_SuctionPumpCtrl_Request__type_support;
}

#if defined(__cplusplus)
}
#endif

// already included above
// #include <cassert>
// already included above
// #include <cstddef>
// already included above
// #include <limits>
// already included above
// #include <string>
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "rosidl_typesupport_fastrtps_c/serialization_helpers.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
// already included above
// #include "battery_lab_custom_msg/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
// already included above
// #include "battery_lab_custom_msg/srv/detail/suction_pump_ctrl__struct.h"
// already included above
// #include "battery_lab_custom_msg/srv/detail/suction_pump_ctrl__functions.h"
// already included above
// #include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

// already included above
// #include "rosidl_runtime_c/string.h"  // status
// already included above
// #include "rosidl_runtime_c/string_functions.h"  // status

// forward declare type support functions


using _SuctionPumpCtrl_Response__ros_msg_type = battery_lab_custom_msg__srv__SuctionPumpCtrl_Response;


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_battery_lab_custom_msg
bool cdr_serialize_battery_lab_custom_msg__srv__SuctionPumpCtrl_Response(
  const battery_lab_custom_msg__srv__SuctionPumpCtrl_Response * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: status
  {
    const rosidl_runtime_c__String * str = &ros_message->status;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_battery_lab_custom_msg
bool cdr_deserialize_battery_lab_custom_msg__srv__SuctionPumpCtrl_Response(
  eprosima::fastcdr::Cdr & cdr,
  battery_lab_custom_msg__srv__SuctionPumpCtrl_Response * ros_message)
{
  // Field name: status
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->status.data) {
      rosidl_runtime_c__String__init(&ros_message->status);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->status,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'status'\n");
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_battery_lab_custom_msg
size_t get_serialized_size_battery_lab_custom_msg__srv__SuctionPumpCtrl_Response(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _SuctionPumpCtrl_Response__ros_msg_type * ros_message = static_cast<const _SuctionPumpCtrl_Response__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: status
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->status.size + 1);

  return current_alignment - initial_alignment;
}


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_battery_lab_custom_msg
size_t max_serialized_size_battery_lab_custom_msg__srv__SuctionPumpCtrl_Response(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // Field name: status
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }


  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = battery_lab_custom_msg__srv__SuctionPumpCtrl_Response;
    is_plain =
      (
      offsetof(DataType, status) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_battery_lab_custom_msg
bool cdr_serialize_key_battery_lab_custom_msg__srv__SuctionPumpCtrl_Response(
  const battery_lab_custom_msg__srv__SuctionPumpCtrl_Response * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: status
  {
    const rosidl_runtime_c__String * str = &ros_message->status;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_battery_lab_custom_msg
size_t get_serialized_size_key_battery_lab_custom_msg__srv__SuctionPumpCtrl_Response(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _SuctionPumpCtrl_Response__ros_msg_type * ros_message = static_cast<const _SuctionPumpCtrl_Response__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;

  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: status
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->status.size + 1);

  return current_alignment - initial_alignment;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_battery_lab_custom_msg
size_t max_serialized_size_key_battery_lab_custom_msg__srv__SuctionPumpCtrl_Response(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;
  // Field name: status
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = battery_lab_custom_msg__srv__SuctionPumpCtrl_Response;
    is_plain =
      (
      offsetof(DataType, status) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}


static bool _SuctionPumpCtrl_Response__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const battery_lab_custom_msg__srv__SuctionPumpCtrl_Response * ros_message = static_cast<const battery_lab_custom_msg__srv__SuctionPumpCtrl_Response *>(untyped_ros_message);
  (void)ros_message;
  return cdr_serialize_battery_lab_custom_msg__srv__SuctionPumpCtrl_Response(ros_message, cdr);
}

static bool _SuctionPumpCtrl_Response__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  battery_lab_custom_msg__srv__SuctionPumpCtrl_Response * ros_message = static_cast<battery_lab_custom_msg__srv__SuctionPumpCtrl_Response *>(untyped_ros_message);
  (void)ros_message;
  return cdr_deserialize_battery_lab_custom_msg__srv__SuctionPumpCtrl_Response(cdr, ros_message);
}

static uint32_t _SuctionPumpCtrl_Response__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_battery_lab_custom_msg__srv__SuctionPumpCtrl_Response(
      untyped_ros_message, 0));
}

static size_t _SuctionPumpCtrl_Response__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_battery_lab_custom_msg__srv__SuctionPumpCtrl_Response(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_SuctionPumpCtrl_Response = {
  "battery_lab_custom_msg::srv",
  "SuctionPumpCtrl_Response",
  _SuctionPumpCtrl_Response__cdr_serialize,
  _SuctionPumpCtrl_Response__cdr_deserialize,
  _SuctionPumpCtrl_Response__get_serialized_size,
  _SuctionPumpCtrl_Response__max_serialized_size,
  nullptr
};

static rosidl_message_type_support_t _SuctionPumpCtrl_Response__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_SuctionPumpCtrl_Response,
  get_message_typesupport_handle_function,
  &battery_lab_custom_msg__srv__SuctionPumpCtrl_Response__get_type_hash,
  &battery_lab_custom_msg__srv__SuctionPumpCtrl_Response__get_type_description,
  &battery_lab_custom_msg__srv__SuctionPumpCtrl_Response__get_type_description_sources,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, battery_lab_custom_msg, srv, SuctionPumpCtrl_Response)() {
  return &_SuctionPumpCtrl_Response__type_support;
}

#if defined(__cplusplus)
}
#endif

// already included above
// #include <cassert>
// already included above
// #include <cstddef>
// already included above
// #include <limits>
// already included above
// #include <string>
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "rosidl_typesupport_fastrtps_c/serialization_helpers.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
// already included above
// #include "battery_lab_custom_msg/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
// already included above
// #include "battery_lab_custom_msg/srv/detail/suction_pump_ctrl__struct.h"
// already included above
// #include "battery_lab_custom_msg/srv/detail/suction_pump_ctrl__functions.h"
// already included above
// #include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "service_msgs/msg/detail/service_event_info__functions.h"  // info

// forward declare type support functions

bool cdr_serialize_battery_lab_custom_msg__srv__SuctionPumpCtrl_Request(
  const battery_lab_custom_msg__srv__SuctionPumpCtrl_Request * ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool cdr_deserialize_battery_lab_custom_msg__srv__SuctionPumpCtrl_Request(
  eprosima::fastcdr::Cdr & cdr,
  battery_lab_custom_msg__srv__SuctionPumpCtrl_Request * ros_message);

size_t get_serialized_size_battery_lab_custom_msg__srv__SuctionPumpCtrl_Request(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_battery_lab_custom_msg__srv__SuctionPumpCtrl_Request(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool cdr_serialize_key_battery_lab_custom_msg__srv__SuctionPumpCtrl_Request(
  const battery_lab_custom_msg__srv__SuctionPumpCtrl_Request * ros_message,
  eprosima::fastcdr::Cdr & cdr);

size_t get_serialized_size_key_battery_lab_custom_msg__srv__SuctionPumpCtrl_Request(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_key_battery_lab_custom_msg__srv__SuctionPumpCtrl_Request(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, battery_lab_custom_msg, srv, SuctionPumpCtrl_Request)();

bool cdr_serialize_battery_lab_custom_msg__srv__SuctionPumpCtrl_Response(
  const battery_lab_custom_msg__srv__SuctionPumpCtrl_Response * ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool cdr_deserialize_battery_lab_custom_msg__srv__SuctionPumpCtrl_Response(
  eprosima::fastcdr::Cdr & cdr,
  battery_lab_custom_msg__srv__SuctionPumpCtrl_Response * ros_message);

size_t get_serialized_size_battery_lab_custom_msg__srv__SuctionPumpCtrl_Response(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_battery_lab_custom_msg__srv__SuctionPumpCtrl_Response(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool cdr_serialize_key_battery_lab_custom_msg__srv__SuctionPumpCtrl_Response(
  const battery_lab_custom_msg__srv__SuctionPumpCtrl_Response * ros_message,
  eprosima::fastcdr::Cdr & cdr);

size_t get_serialized_size_key_battery_lab_custom_msg__srv__SuctionPumpCtrl_Response(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_key_battery_lab_custom_msg__srv__SuctionPumpCtrl_Response(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, battery_lab_custom_msg, srv, SuctionPumpCtrl_Response)();

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_battery_lab_custom_msg
bool cdr_serialize_service_msgs__msg__ServiceEventInfo(
  const service_msgs__msg__ServiceEventInfo * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_battery_lab_custom_msg
bool cdr_deserialize_service_msgs__msg__ServiceEventInfo(
  eprosima::fastcdr::Cdr & cdr,
  service_msgs__msg__ServiceEventInfo * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_battery_lab_custom_msg
size_t get_serialized_size_service_msgs__msg__ServiceEventInfo(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_battery_lab_custom_msg
size_t max_serialized_size_service_msgs__msg__ServiceEventInfo(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_battery_lab_custom_msg
bool cdr_serialize_key_service_msgs__msg__ServiceEventInfo(
  const service_msgs__msg__ServiceEventInfo * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_battery_lab_custom_msg
size_t get_serialized_size_key_service_msgs__msg__ServiceEventInfo(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_battery_lab_custom_msg
size_t max_serialized_size_key_service_msgs__msg__ServiceEventInfo(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_battery_lab_custom_msg
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, service_msgs, msg, ServiceEventInfo)();


using _SuctionPumpCtrl_Event__ros_msg_type = battery_lab_custom_msg__srv__SuctionPumpCtrl_Event;


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_battery_lab_custom_msg
bool cdr_serialize_battery_lab_custom_msg__srv__SuctionPumpCtrl_Event(
  const battery_lab_custom_msg__srv__SuctionPumpCtrl_Event * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: info
  {
    cdr_serialize_service_msgs__msg__ServiceEventInfo(
      &ros_message->info, cdr);
  }

  // Field name: request
  {
    size_t size = ros_message->request.size;
    auto array_ptr = ros_message->request.data;
    if (size > 1) {
      fprintf(stderr, "array size exceeds upper bound\n");
      return false;
    }
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; ++i) {
      cdr_serialize_battery_lab_custom_msg__srv__SuctionPumpCtrl_Request(
        &array_ptr[i], cdr);
    }
  }

  // Field name: response
  {
    size_t size = ros_message->response.size;
    auto array_ptr = ros_message->response.data;
    if (size > 1) {
      fprintf(stderr, "array size exceeds upper bound\n");
      return false;
    }
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; ++i) {
      cdr_serialize_battery_lab_custom_msg__srv__SuctionPumpCtrl_Response(
        &array_ptr[i], cdr);
    }
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_battery_lab_custom_msg
bool cdr_deserialize_battery_lab_custom_msg__srv__SuctionPumpCtrl_Event(
  eprosima::fastcdr::Cdr & cdr,
  battery_lab_custom_msg__srv__SuctionPumpCtrl_Event * ros_message)
{
  // Field name: info
  {
    cdr_deserialize_service_msgs__msg__ServiceEventInfo(cdr, &ros_message->info);
  }

  // Field name: request
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    if (ros_message->request.data) {
      battery_lab_custom_msg__srv__SuctionPumpCtrl_Request__Sequence__fini(&ros_message->request);
    }
    if (!battery_lab_custom_msg__srv__SuctionPumpCtrl_Request__Sequence__init(&ros_message->request, size)) {
      fprintf(stderr, "failed to create array for field 'request'");
      return false;
    }
    auto array_ptr = ros_message->request.data;
    for (size_t i = 0; i < size; ++i) {
      cdr_deserialize_battery_lab_custom_msg__srv__SuctionPumpCtrl_Request(cdr, &array_ptr[i]);
    }
  }

  // Field name: response
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    if (ros_message->response.data) {
      battery_lab_custom_msg__srv__SuctionPumpCtrl_Response__Sequence__fini(&ros_message->response);
    }
    if (!battery_lab_custom_msg__srv__SuctionPumpCtrl_Response__Sequence__init(&ros_message->response, size)) {
      fprintf(stderr, "failed to create array for field 'response'");
      return false;
    }
    auto array_ptr = ros_message->response.data;
    for (size_t i = 0; i < size; ++i) {
      cdr_deserialize_battery_lab_custom_msg__srv__SuctionPumpCtrl_Response(cdr, &array_ptr[i]);
    }
  }

  return true;
}  // NOLINT(readability/fn_size)


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_battery_lab_custom_msg
size_t get_serialized_size_battery_lab_custom_msg__srv__SuctionPumpCtrl_Event(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _SuctionPumpCtrl_Event__ros_msg_type * ros_message = static_cast<const _SuctionPumpCtrl_Event__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: info
  current_alignment += get_serialized_size_service_msgs__msg__ServiceEventInfo(
    &(ros_message->info), current_alignment);

  // Field name: request
  {
    size_t array_size = ros_message->request.size;
    auto array_ptr = ros_message->request.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += get_serialized_size_battery_lab_custom_msg__srv__SuctionPumpCtrl_Request(
        &array_ptr[index], current_alignment);
    }
  }

  // Field name: response
  {
    size_t array_size = ros_message->response.size;
    auto array_ptr = ros_message->response.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += get_serialized_size_battery_lab_custom_msg__srv__SuctionPumpCtrl_Response(
        &array_ptr[index], current_alignment);
    }
  }

  return current_alignment - initial_alignment;
}


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_battery_lab_custom_msg
size_t max_serialized_size_battery_lab_custom_msg__srv__SuctionPumpCtrl_Event(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // Field name: info
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_service_msgs__msg__ServiceEventInfo(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: request
  {
    size_t array_size = 1;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_battery_lab_custom_msg__srv__SuctionPumpCtrl_Request(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: response
  {
    size_t array_size = 1;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_battery_lab_custom_msg__srv__SuctionPumpCtrl_Response(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }


  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = battery_lab_custom_msg__srv__SuctionPumpCtrl_Event;
    is_plain =
      (
      offsetof(DataType, response) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_battery_lab_custom_msg
bool cdr_serialize_key_battery_lab_custom_msg__srv__SuctionPumpCtrl_Event(
  const battery_lab_custom_msg__srv__SuctionPumpCtrl_Event * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: info
  {
    cdr_serialize_key_service_msgs__msg__ServiceEventInfo(
      &ros_message->info, cdr);
  }

  // Field name: request
  {
    size_t size = ros_message->request.size;
    auto array_ptr = ros_message->request.data;
    if (size > 1) {
      fprintf(stderr, "array size exceeds upper bound\n");
      return false;
    }
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; ++i) {
      cdr_serialize_key_battery_lab_custom_msg__srv__SuctionPumpCtrl_Request(
        &array_ptr[i], cdr);
    }
  }

  // Field name: response
  {
    size_t size = ros_message->response.size;
    auto array_ptr = ros_message->response.data;
    if (size > 1) {
      fprintf(stderr, "array size exceeds upper bound\n");
      return false;
    }
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; ++i) {
      cdr_serialize_key_battery_lab_custom_msg__srv__SuctionPumpCtrl_Response(
        &array_ptr[i], cdr);
    }
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_battery_lab_custom_msg
size_t get_serialized_size_key_battery_lab_custom_msg__srv__SuctionPumpCtrl_Event(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _SuctionPumpCtrl_Event__ros_msg_type * ros_message = static_cast<const _SuctionPumpCtrl_Event__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;

  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: info
  current_alignment += get_serialized_size_key_service_msgs__msg__ServiceEventInfo(
    &(ros_message->info), current_alignment);

  // Field name: request
  {
    size_t array_size = ros_message->request.size;
    auto array_ptr = ros_message->request.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += get_serialized_size_key_battery_lab_custom_msg__srv__SuctionPumpCtrl_Request(
        &array_ptr[index], current_alignment);
    }
  }

  // Field name: response
  {
    size_t array_size = ros_message->response.size;
    auto array_ptr = ros_message->response.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += get_serialized_size_key_battery_lab_custom_msg__srv__SuctionPumpCtrl_Response(
        &array_ptr[index], current_alignment);
    }
  }

  return current_alignment - initial_alignment;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_battery_lab_custom_msg
size_t max_serialized_size_key_battery_lab_custom_msg__srv__SuctionPumpCtrl_Event(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;
  // Field name: info
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_service_msgs__msg__ServiceEventInfo(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: request
  {
    size_t array_size = 1;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_battery_lab_custom_msg__srv__SuctionPumpCtrl_Request(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: response
  {
    size_t array_size = 1;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_battery_lab_custom_msg__srv__SuctionPumpCtrl_Response(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = battery_lab_custom_msg__srv__SuctionPumpCtrl_Event;
    is_plain =
      (
      offsetof(DataType, response) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}


static bool _SuctionPumpCtrl_Event__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const battery_lab_custom_msg__srv__SuctionPumpCtrl_Event * ros_message = static_cast<const battery_lab_custom_msg__srv__SuctionPumpCtrl_Event *>(untyped_ros_message);
  (void)ros_message;
  return cdr_serialize_battery_lab_custom_msg__srv__SuctionPumpCtrl_Event(ros_message, cdr);
}

static bool _SuctionPumpCtrl_Event__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  battery_lab_custom_msg__srv__SuctionPumpCtrl_Event * ros_message = static_cast<battery_lab_custom_msg__srv__SuctionPumpCtrl_Event *>(untyped_ros_message);
  (void)ros_message;
  return cdr_deserialize_battery_lab_custom_msg__srv__SuctionPumpCtrl_Event(cdr, ros_message);
}

static uint32_t _SuctionPumpCtrl_Event__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_battery_lab_custom_msg__srv__SuctionPumpCtrl_Event(
      untyped_ros_message, 0));
}

static size_t _SuctionPumpCtrl_Event__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_battery_lab_custom_msg__srv__SuctionPumpCtrl_Event(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_SuctionPumpCtrl_Event = {
  "battery_lab_custom_msg::srv",
  "SuctionPumpCtrl_Event",
  _SuctionPumpCtrl_Event__cdr_serialize,
  _SuctionPumpCtrl_Event__cdr_deserialize,
  _SuctionPumpCtrl_Event__get_serialized_size,
  _SuctionPumpCtrl_Event__max_serialized_size,
  nullptr
};

static rosidl_message_type_support_t _SuctionPumpCtrl_Event__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_SuctionPumpCtrl_Event,
  get_message_typesupport_handle_function,
  &battery_lab_custom_msg__srv__SuctionPumpCtrl_Event__get_type_hash,
  &battery_lab_custom_msg__srv__SuctionPumpCtrl_Event__get_type_description,
  &battery_lab_custom_msg__srv__SuctionPumpCtrl_Event__get_type_description_sources,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, battery_lab_custom_msg, srv, SuctionPumpCtrl_Event)() {
  return &_SuctionPumpCtrl_Event__type_support;
}

#if defined(__cplusplus)
}
#endif

#include "rosidl_typesupport_fastrtps_cpp/service_type_support.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "battery_lab_custom_msg/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "battery_lab_custom_msg/srv/suction_pump_ctrl.h"

#if defined(__cplusplus)
extern "C"
{
#endif

static service_type_support_callbacks_t SuctionPumpCtrl__callbacks = {
  "battery_lab_custom_msg::srv",
  "SuctionPumpCtrl",
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, battery_lab_custom_msg, srv, SuctionPumpCtrl_Request)(),
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, battery_lab_custom_msg, srv, SuctionPumpCtrl_Response)(),
};

static rosidl_service_type_support_t SuctionPumpCtrl__handle = {
  rosidl_typesupport_fastrtps_c__identifier,
  &SuctionPumpCtrl__callbacks,
  get_service_typesupport_handle_function,
  &_SuctionPumpCtrl_Request__type_support,
  &_SuctionPumpCtrl_Response__type_support,
  &_SuctionPumpCtrl_Event__type_support,
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    battery_lab_custom_msg,
    srv,
    SuctionPumpCtrl
  ),
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    battery_lab_custom_msg,
    srv,
    SuctionPumpCtrl
  ),
  &battery_lab_custom_msg__srv__SuctionPumpCtrl__get_type_hash,
  &battery_lab_custom_msg__srv__SuctionPumpCtrl__get_type_description,
  &battery_lab_custom_msg__srv__SuctionPumpCtrl__get_type_description_sources,
};

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, battery_lab_custom_msg, srv, SuctionPumpCtrl)() {
  return &SuctionPumpCtrl__handle;
}

#if defined(__cplusplus)
}
#endif
