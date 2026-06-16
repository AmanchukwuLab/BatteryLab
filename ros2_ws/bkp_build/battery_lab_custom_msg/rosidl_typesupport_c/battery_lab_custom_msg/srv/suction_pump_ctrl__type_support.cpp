// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from battery_lab_custom_msg:srv/SuctionPumpCtrl.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "battery_lab_custom_msg/srv/detail/suction_pump_ctrl__struct.h"
#include "battery_lab_custom_msg/srv/detail/suction_pump_ctrl__type_support.h"
#include "battery_lab_custom_msg/srv/detail/suction_pump_ctrl__functions.h"
#include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/message_type_support_dispatch.h"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_c/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace battery_lab_custom_msg
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _SuctionPumpCtrl_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _SuctionPumpCtrl_Request_type_support_ids_t;

static const _SuctionPumpCtrl_Request_type_support_ids_t _SuctionPumpCtrl_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _SuctionPumpCtrl_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _SuctionPumpCtrl_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _SuctionPumpCtrl_Request_type_support_symbol_names_t _SuctionPumpCtrl_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, battery_lab_custom_msg, srv, SuctionPumpCtrl_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, battery_lab_custom_msg, srv, SuctionPumpCtrl_Request)),
  }
};

typedef struct _SuctionPumpCtrl_Request_type_support_data_t
{
  void * data[2];
} _SuctionPumpCtrl_Request_type_support_data_t;

static _SuctionPumpCtrl_Request_type_support_data_t _SuctionPumpCtrl_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _SuctionPumpCtrl_Request_message_typesupport_map = {
  2,
  "battery_lab_custom_msg",
  &_SuctionPumpCtrl_Request_message_typesupport_ids.typesupport_identifier[0],
  &_SuctionPumpCtrl_Request_message_typesupport_symbol_names.symbol_name[0],
  &_SuctionPumpCtrl_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t SuctionPumpCtrl_Request_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_SuctionPumpCtrl_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &battery_lab_custom_msg__srv__SuctionPumpCtrl_Request__get_type_hash,
  &battery_lab_custom_msg__srv__SuctionPumpCtrl_Request__get_type_description,
  &battery_lab_custom_msg__srv__SuctionPumpCtrl_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace battery_lab_custom_msg

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, battery_lab_custom_msg, srv, SuctionPumpCtrl_Request)() {
  return &::battery_lab_custom_msg::srv::rosidl_typesupport_c::SuctionPumpCtrl_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "battery_lab_custom_msg/srv/detail/suction_pump_ctrl__struct.h"
// already included above
// #include "battery_lab_custom_msg/srv/detail/suction_pump_ctrl__type_support.h"
// already included above
// #include "battery_lab_custom_msg/srv/detail/suction_pump_ctrl__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace battery_lab_custom_msg
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _SuctionPumpCtrl_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _SuctionPumpCtrl_Response_type_support_ids_t;

static const _SuctionPumpCtrl_Response_type_support_ids_t _SuctionPumpCtrl_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _SuctionPumpCtrl_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _SuctionPumpCtrl_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _SuctionPumpCtrl_Response_type_support_symbol_names_t _SuctionPumpCtrl_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, battery_lab_custom_msg, srv, SuctionPumpCtrl_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, battery_lab_custom_msg, srv, SuctionPumpCtrl_Response)),
  }
};

typedef struct _SuctionPumpCtrl_Response_type_support_data_t
{
  void * data[2];
} _SuctionPumpCtrl_Response_type_support_data_t;

static _SuctionPumpCtrl_Response_type_support_data_t _SuctionPumpCtrl_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _SuctionPumpCtrl_Response_message_typesupport_map = {
  2,
  "battery_lab_custom_msg",
  &_SuctionPumpCtrl_Response_message_typesupport_ids.typesupport_identifier[0],
  &_SuctionPumpCtrl_Response_message_typesupport_symbol_names.symbol_name[0],
  &_SuctionPumpCtrl_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t SuctionPumpCtrl_Response_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_SuctionPumpCtrl_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &battery_lab_custom_msg__srv__SuctionPumpCtrl_Response__get_type_hash,
  &battery_lab_custom_msg__srv__SuctionPumpCtrl_Response__get_type_description,
  &battery_lab_custom_msg__srv__SuctionPumpCtrl_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace battery_lab_custom_msg

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, battery_lab_custom_msg, srv, SuctionPumpCtrl_Response)() {
  return &::battery_lab_custom_msg::srv::rosidl_typesupport_c::SuctionPumpCtrl_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "battery_lab_custom_msg/srv/detail/suction_pump_ctrl__struct.h"
// already included above
// #include "battery_lab_custom_msg/srv/detail/suction_pump_ctrl__type_support.h"
// already included above
// #include "battery_lab_custom_msg/srv/detail/suction_pump_ctrl__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace battery_lab_custom_msg
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _SuctionPumpCtrl_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _SuctionPumpCtrl_Event_type_support_ids_t;

static const _SuctionPumpCtrl_Event_type_support_ids_t _SuctionPumpCtrl_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _SuctionPumpCtrl_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _SuctionPumpCtrl_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _SuctionPumpCtrl_Event_type_support_symbol_names_t _SuctionPumpCtrl_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, battery_lab_custom_msg, srv, SuctionPumpCtrl_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, battery_lab_custom_msg, srv, SuctionPumpCtrl_Event)),
  }
};

typedef struct _SuctionPumpCtrl_Event_type_support_data_t
{
  void * data[2];
} _SuctionPumpCtrl_Event_type_support_data_t;

static _SuctionPumpCtrl_Event_type_support_data_t _SuctionPumpCtrl_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _SuctionPumpCtrl_Event_message_typesupport_map = {
  2,
  "battery_lab_custom_msg",
  &_SuctionPumpCtrl_Event_message_typesupport_ids.typesupport_identifier[0],
  &_SuctionPumpCtrl_Event_message_typesupport_symbol_names.symbol_name[0],
  &_SuctionPumpCtrl_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t SuctionPumpCtrl_Event_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_SuctionPumpCtrl_Event_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &battery_lab_custom_msg__srv__SuctionPumpCtrl_Event__get_type_hash,
  &battery_lab_custom_msg__srv__SuctionPumpCtrl_Event__get_type_description,
  &battery_lab_custom_msg__srv__SuctionPumpCtrl_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace battery_lab_custom_msg

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, battery_lab_custom_msg, srv, SuctionPumpCtrl_Event)() {
  return &::battery_lab_custom_msg::srv::rosidl_typesupport_c::SuctionPumpCtrl_Event_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "battery_lab_custom_msg/srv/detail/suction_pump_ctrl__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
#include "service_msgs/msg/service_event_info.h"
#include "builtin_interfaces/msg/time.h"

namespace battery_lab_custom_msg
{

namespace srv
{

namespace rosidl_typesupport_c
{
typedef struct _SuctionPumpCtrl_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _SuctionPumpCtrl_type_support_ids_t;

static const _SuctionPumpCtrl_type_support_ids_t _SuctionPumpCtrl_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _SuctionPumpCtrl_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _SuctionPumpCtrl_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _SuctionPumpCtrl_type_support_symbol_names_t _SuctionPumpCtrl_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, battery_lab_custom_msg, srv, SuctionPumpCtrl)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, battery_lab_custom_msg, srv, SuctionPumpCtrl)),
  }
};

typedef struct _SuctionPumpCtrl_type_support_data_t
{
  void * data[2];
} _SuctionPumpCtrl_type_support_data_t;

static _SuctionPumpCtrl_type_support_data_t _SuctionPumpCtrl_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _SuctionPumpCtrl_service_typesupport_map = {
  2,
  "battery_lab_custom_msg",
  &_SuctionPumpCtrl_service_typesupport_ids.typesupport_identifier[0],
  &_SuctionPumpCtrl_service_typesupport_symbol_names.symbol_name[0],
  &_SuctionPumpCtrl_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t SuctionPumpCtrl_service_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_SuctionPumpCtrl_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
  &SuctionPumpCtrl_Request_message_type_support_handle,
  &SuctionPumpCtrl_Response_message_type_support_handle,
  &SuctionPumpCtrl_Event_message_type_support_handle,
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

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace battery_lab_custom_msg

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, battery_lab_custom_msg, srv, SuctionPumpCtrl)() {
  return &::battery_lab_custom_msg::srv::rosidl_typesupport_c::SuctionPumpCtrl_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif
