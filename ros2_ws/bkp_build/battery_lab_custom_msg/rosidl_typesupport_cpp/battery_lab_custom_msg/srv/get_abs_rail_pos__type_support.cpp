// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from battery_lab_custom_msg:srv/GetAbsRailPos.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "battery_lab_custom_msg/srv/detail/get_abs_rail_pos__functions.h"
#include "battery_lab_custom_msg/srv/detail/get_abs_rail_pos__struct.hpp"
#include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
#include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace battery_lab_custom_msg
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _GetAbsRailPos_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GetAbsRailPos_Request_type_support_ids_t;

static const _GetAbsRailPos_Request_type_support_ids_t _GetAbsRailPos_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _GetAbsRailPos_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GetAbsRailPos_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GetAbsRailPos_Request_type_support_symbol_names_t _GetAbsRailPos_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, battery_lab_custom_msg, srv, GetAbsRailPos_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, battery_lab_custom_msg, srv, GetAbsRailPos_Request)),
  }
};

typedef struct _GetAbsRailPos_Request_type_support_data_t
{
  void * data[2];
} _GetAbsRailPos_Request_type_support_data_t;

static _GetAbsRailPos_Request_type_support_data_t _GetAbsRailPos_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GetAbsRailPos_Request_message_typesupport_map = {
  2,
  "battery_lab_custom_msg",
  &_GetAbsRailPos_Request_message_typesupport_ids.typesupport_identifier[0],
  &_GetAbsRailPos_Request_message_typesupport_symbol_names.symbol_name[0],
  &_GetAbsRailPos_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t GetAbsRailPos_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GetAbsRailPos_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &battery_lab_custom_msg__srv__GetAbsRailPos_Request__get_type_hash,
  &battery_lab_custom_msg__srv__GetAbsRailPos_Request__get_type_description,
  &battery_lab_custom_msg__srv__GetAbsRailPos_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace battery_lab_custom_msg

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<battery_lab_custom_msg::srv::GetAbsRailPos_Request>()
{
  return &::battery_lab_custom_msg::srv::rosidl_typesupport_cpp::GetAbsRailPos_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, battery_lab_custom_msg, srv, GetAbsRailPos_Request)() {
  return get_message_type_support_handle<battery_lab_custom_msg::srv::GetAbsRailPos_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "battery_lab_custom_msg/srv/detail/get_abs_rail_pos__functions.h"
// already included above
// #include "battery_lab_custom_msg/srv/detail/get_abs_rail_pos__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace battery_lab_custom_msg
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _GetAbsRailPos_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GetAbsRailPos_Response_type_support_ids_t;

static const _GetAbsRailPos_Response_type_support_ids_t _GetAbsRailPos_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _GetAbsRailPos_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GetAbsRailPos_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GetAbsRailPos_Response_type_support_symbol_names_t _GetAbsRailPos_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, battery_lab_custom_msg, srv, GetAbsRailPos_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, battery_lab_custom_msg, srv, GetAbsRailPos_Response)),
  }
};

typedef struct _GetAbsRailPos_Response_type_support_data_t
{
  void * data[2];
} _GetAbsRailPos_Response_type_support_data_t;

static _GetAbsRailPos_Response_type_support_data_t _GetAbsRailPos_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GetAbsRailPos_Response_message_typesupport_map = {
  2,
  "battery_lab_custom_msg",
  &_GetAbsRailPos_Response_message_typesupport_ids.typesupport_identifier[0],
  &_GetAbsRailPos_Response_message_typesupport_symbol_names.symbol_name[0],
  &_GetAbsRailPos_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t GetAbsRailPos_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GetAbsRailPos_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &battery_lab_custom_msg__srv__GetAbsRailPos_Response__get_type_hash,
  &battery_lab_custom_msg__srv__GetAbsRailPos_Response__get_type_description,
  &battery_lab_custom_msg__srv__GetAbsRailPos_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace battery_lab_custom_msg

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<battery_lab_custom_msg::srv::GetAbsRailPos_Response>()
{
  return &::battery_lab_custom_msg::srv::rosidl_typesupport_cpp::GetAbsRailPos_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, battery_lab_custom_msg, srv, GetAbsRailPos_Response)() {
  return get_message_type_support_handle<battery_lab_custom_msg::srv::GetAbsRailPos_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "battery_lab_custom_msg/srv/detail/get_abs_rail_pos__functions.h"
// already included above
// #include "battery_lab_custom_msg/srv/detail/get_abs_rail_pos__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace battery_lab_custom_msg
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _GetAbsRailPos_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GetAbsRailPos_Event_type_support_ids_t;

static const _GetAbsRailPos_Event_type_support_ids_t _GetAbsRailPos_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _GetAbsRailPos_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GetAbsRailPos_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GetAbsRailPos_Event_type_support_symbol_names_t _GetAbsRailPos_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, battery_lab_custom_msg, srv, GetAbsRailPos_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, battery_lab_custom_msg, srv, GetAbsRailPos_Event)),
  }
};

typedef struct _GetAbsRailPos_Event_type_support_data_t
{
  void * data[2];
} _GetAbsRailPos_Event_type_support_data_t;

static _GetAbsRailPos_Event_type_support_data_t _GetAbsRailPos_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GetAbsRailPos_Event_message_typesupport_map = {
  2,
  "battery_lab_custom_msg",
  &_GetAbsRailPos_Event_message_typesupport_ids.typesupport_identifier[0],
  &_GetAbsRailPos_Event_message_typesupport_symbol_names.symbol_name[0],
  &_GetAbsRailPos_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t GetAbsRailPos_Event_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GetAbsRailPos_Event_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &battery_lab_custom_msg__srv__GetAbsRailPos_Event__get_type_hash,
  &battery_lab_custom_msg__srv__GetAbsRailPos_Event__get_type_description,
  &battery_lab_custom_msg__srv__GetAbsRailPos_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace battery_lab_custom_msg

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<battery_lab_custom_msg::srv::GetAbsRailPos_Event>()
{
  return &::battery_lab_custom_msg::srv::rosidl_typesupport_cpp::GetAbsRailPos_Event_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, battery_lab_custom_msg, srv, GetAbsRailPos_Event)() {
  return get_message_type_support_handle<battery_lab_custom_msg::srv::GetAbsRailPos_Event>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "battery_lab_custom_msg/srv/detail/get_abs_rail_pos__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace battery_lab_custom_msg
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _GetAbsRailPos_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GetAbsRailPos_type_support_ids_t;

static const _GetAbsRailPos_type_support_ids_t _GetAbsRailPos_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _GetAbsRailPos_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GetAbsRailPos_type_support_symbol_names_t;
#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GetAbsRailPos_type_support_symbol_names_t _GetAbsRailPos_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, battery_lab_custom_msg, srv, GetAbsRailPos)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, battery_lab_custom_msg, srv, GetAbsRailPos)),
  }
};

typedef struct _GetAbsRailPos_type_support_data_t
{
  void * data[2];
} _GetAbsRailPos_type_support_data_t;

static _GetAbsRailPos_type_support_data_t _GetAbsRailPos_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GetAbsRailPos_service_typesupport_map = {
  2,
  "battery_lab_custom_msg",
  &_GetAbsRailPos_service_typesupport_ids.typesupport_identifier[0],
  &_GetAbsRailPos_service_typesupport_symbol_names.symbol_name[0],
  &_GetAbsRailPos_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t GetAbsRailPos_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GetAbsRailPos_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
  ::rosidl_typesupport_cpp::get_message_type_support_handle<battery_lab_custom_msg::srv::GetAbsRailPos_Request>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<battery_lab_custom_msg::srv::GetAbsRailPos_Response>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<battery_lab_custom_msg::srv::GetAbsRailPos_Event>(),
  &::rosidl_typesupport_cpp::service_create_event_message<battery_lab_custom_msg::srv::GetAbsRailPos>,
  &::rosidl_typesupport_cpp::service_destroy_event_message<battery_lab_custom_msg::srv::GetAbsRailPos>,
  &battery_lab_custom_msg__srv__GetAbsRailPos__get_type_hash,
  &battery_lab_custom_msg__srv__GetAbsRailPos__get_type_description,
  &battery_lab_custom_msg__srv__GetAbsRailPos__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace battery_lab_custom_msg

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<battery_lab_custom_msg::srv::GetAbsRailPos>()
{
  return &::battery_lab_custom_msg::srv::rosidl_typesupport_cpp::GetAbsRailPos_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, battery_lab_custom_msg, srv, GetAbsRailPos)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<battery_lab_custom_msg::srv::GetAbsRailPos>();
}

#ifdef __cplusplus
}
#endif
