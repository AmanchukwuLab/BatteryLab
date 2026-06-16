// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from battery_lab_custom_msg:srv/CaptureImage.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "battery_lab_custom_msg/srv/capture_image.h"


#ifndef BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__CAPTURE_IMAGE__STRUCT_H_
#define BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__CAPTURE_IMAGE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/CaptureImage in the package battery_lab_custom_msg.
typedef struct battery_lab_custom_msg__srv__CaptureImage_Request
{
  uint8_t structure_needs_at_least_one_member;
} battery_lab_custom_msg__srv__CaptureImage_Request;

// Struct for a sequence of battery_lab_custom_msg__srv__CaptureImage_Request.
typedef struct battery_lab_custom_msg__srv__CaptureImage_Request__Sequence
{
  battery_lab_custom_msg__srv__CaptureImage_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} battery_lab_custom_msg__srv__CaptureImage_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'image'
#include "sensor_msgs/msg/detail/image__struct.h"

/// Struct defined in srv/CaptureImage in the package battery_lab_custom_msg.
typedef struct battery_lab_custom_msg__srv__CaptureImage_Response
{
  sensor_msgs__msg__Image image;
} battery_lab_custom_msg__srv__CaptureImage_Response;

// Struct for a sequence of battery_lab_custom_msg__srv__CaptureImage_Response.
typedef struct battery_lab_custom_msg__srv__CaptureImage_Response__Sequence
{
  battery_lab_custom_msg__srv__CaptureImage_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} battery_lab_custom_msg__srv__CaptureImage_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  battery_lab_custom_msg__srv__CaptureImage_Event__request__MAX_SIZE = 1
};
// response
enum
{
  battery_lab_custom_msg__srv__CaptureImage_Event__response__MAX_SIZE = 1
};

/// Struct defined in srv/CaptureImage in the package battery_lab_custom_msg.
typedef struct battery_lab_custom_msg__srv__CaptureImage_Event
{
  service_msgs__msg__ServiceEventInfo info;
  battery_lab_custom_msg__srv__CaptureImage_Request__Sequence request;
  battery_lab_custom_msg__srv__CaptureImage_Response__Sequence response;
} battery_lab_custom_msg__srv__CaptureImage_Event;

// Struct for a sequence of battery_lab_custom_msg__srv__CaptureImage_Event.
typedef struct battery_lab_custom_msg__srv__CaptureImage_Event__Sequence
{
  battery_lab_custom_msg__srv__CaptureImage_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} battery_lab_custom_msg__srv__CaptureImage_Event__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__CAPTURE_IMAGE__STRUCT_H_
