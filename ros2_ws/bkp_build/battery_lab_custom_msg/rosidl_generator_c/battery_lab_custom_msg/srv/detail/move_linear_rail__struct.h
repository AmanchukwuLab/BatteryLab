// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from battery_lab_custom_msg:srv/MoveLinearRail.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "battery_lab_custom_msg/srv/move_linear_rail.h"


#ifndef BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__MOVE_LINEAR_RAIL__STRUCT_H_
#define BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__MOVE_LINEAR_RAIL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/MoveLinearRail in the package battery_lab_custom_msg.
typedef struct battery_lab_custom_msg__srv__MoveLinearRail_Request
{
  float target_position;
} battery_lab_custom_msg__srv__MoveLinearRail_Request;

// Struct for a sequence of battery_lab_custom_msg__srv__MoveLinearRail_Request.
typedef struct battery_lab_custom_msg__srv__MoveLinearRail_Request__Sequence
{
  battery_lab_custom_msg__srv__MoveLinearRail_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} battery_lab_custom_msg__srv__MoveLinearRail_Request__Sequence;

// Constants defined in the message

/// Struct defined in srv/MoveLinearRail in the package battery_lab_custom_msg.
typedef struct battery_lab_custom_msg__srv__MoveLinearRail_Response
{
  bool success;
} battery_lab_custom_msg__srv__MoveLinearRail_Response;

// Struct for a sequence of battery_lab_custom_msg__srv__MoveLinearRail_Response.
typedef struct battery_lab_custom_msg__srv__MoveLinearRail_Response__Sequence
{
  battery_lab_custom_msg__srv__MoveLinearRail_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} battery_lab_custom_msg__srv__MoveLinearRail_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  battery_lab_custom_msg__srv__MoveLinearRail_Event__request__MAX_SIZE = 1
};
// response
enum
{
  battery_lab_custom_msg__srv__MoveLinearRail_Event__response__MAX_SIZE = 1
};

/// Struct defined in srv/MoveLinearRail in the package battery_lab_custom_msg.
typedef struct battery_lab_custom_msg__srv__MoveLinearRail_Event
{
  service_msgs__msg__ServiceEventInfo info;
  battery_lab_custom_msg__srv__MoveLinearRail_Request__Sequence request;
  battery_lab_custom_msg__srv__MoveLinearRail_Response__Sequence response;
} battery_lab_custom_msg__srv__MoveLinearRail_Event;

// Struct for a sequence of battery_lab_custom_msg__srv__MoveLinearRail_Event.
typedef struct battery_lab_custom_msg__srv__MoveLinearRail_Event__Sequence
{
  battery_lab_custom_msg__srv__MoveLinearRail_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} battery_lab_custom_msg__srv__MoveLinearRail_Event__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__MOVE_LINEAR_RAIL__STRUCT_H_
