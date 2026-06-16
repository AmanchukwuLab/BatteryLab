// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from battery_lab_custom_msg:srv/MoveLinearRail.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "battery_lab_custom_msg/srv/move_linear_rail.h"


#ifndef BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__MOVE_LINEAR_RAIL__FUNCTIONS_H_
#define BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__MOVE_LINEAR_RAIL__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/action_type_support_struct.h"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_runtime_c/service_type_support_struct.h"
#include "rosidl_runtime_c/type_description/type_description__struct.h"
#include "rosidl_runtime_c/type_description/type_source__struct.h"
#include "rosidl_runtime_c/type_hash.h"
#include "rosidl_runtime_c/visibility_control.h"
#include "battery_lab_custom_msg/msg/rosidl_generator_c__visibility_control.h"

#include "battery_lab_custom_msg/srv/detail/move_linear_rail__struct.h"

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
const rosidl_type_hash_t *
battery_lab_custom_msg__srv__MoveLinearRail__get_type_hash(
  const rosidl_service_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
const rosidl_runtime_c__type_description__TypeDescription *
battery_lab_custom_msg__srv__MoveLinearRail__get_type_description(
  const rosidl_service_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
const rosidl_runtime_c__type_description__TypeSource *
battery_lab_custom_msg__srv__MoveLinearRail__get_individual_type_description_source(
  const rosidl_service_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
const rosidl_runtime_c__type_description__TypeSource__Sequence *
battery_lab_custom_msg__srv__MoveLinearRail__get_type_description_sources(
  const rosidl_service_type_support_t * type_support);

/// Initialize srv/MoveLinearRail message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * battery_lab_custom_msg__srv__MoveLinearRail_Request
 * )) before or use
 * battery_lab_custom_msg__srv__MoveLinearRail_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
bool
battery_lab_custom_msg__srv__MoveLinearRail_Request__init(battery_lab_custom_msg__srv__MoveLinearRail_Request * msg);

/// Finalize srv/MoveLinearRail message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
void
battery_lab_custom_msg__srv__MoveLinearRail_Request__fini(battery_lab_custom_msg__srv__MoveLinearRail_Request * msg);

/// Create srv/MoveLinearRail message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * battery_lab_custom_msg__srv__MoveLinearRail_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
battery_lab_custom_msg__srv__MoveLinearRail_Request *
battery_lab_custom_msg__srv__MoveLinearRail_Request__create(void);

/// Destroy srv/MoveLinearRail message.
/**
 * It calls
 * battery_lab_custom_msg__srv__MoveLinearRail_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
void
battery_lab_custom_msg__srv__MoveLinearRail_Request__destroy(battery_lab_custom_msg__srv__MoveLinearRail_Request * msg);

/// Check for srv/MoveLinearRail message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
bool
battery_lab_custom_msg__srv__MoveLinearRail_Request__are_equal(const battery_lab_custom_msg__srv__MoveLinearRail_Request * lhs, const battery_lab_custom_msg__srv__MoveLinearRail_Request * rhs);

/// Copy a srv/MoveLinearRail message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
bool
battery_lab_custom_msg__srv__MoveLinearRail_Request__copy(
  const battery_lab_custom_msg__srv__MoveLinearRail_Request * input,
  battery_lab_custom_msg__srv__MoveLinearRail_Request * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
const rosidl_type_hash_t *
battery_lab_custom_msg__srv__MoveLinearRail_Request__get_type_hash(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
const rosidl_runtime_c__type_description__TypeDescription *
battery_lab_custom_msg__srv__MoveLinearRail_Request__get_type_description(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
const rosidl_runtime_c__type_description__TypeSource *
battery_lab_custom_msg__srv__MoveLinearRail_Request__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
const rosidl_runtime_c__type_description__TypeSource__Sequence *
battery_lab_custom_msg__srv__MoveLinearRail_Request__get_type_description_sources(
  const rosidl_message_type_support_t * type_support);

/// Initialize array of srv/MoveLinearRail messages.
/**
 * It allocates the memory for the number of elements and calls
 * battery_lab_custom_msg__srv__MoveLinearRail_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
bool
battery_lab_custom_msg__srv__MoveLinearRail_Request__Sequence__init(battery_lab_custom_msg__srv__MoveLinearRail_Request__Sequence * array, size_t size);

/// Finalize array of srv/MoveLinearRail messages.
/**
 * It calls
 * battery_lab_custom_msg__srv__MoveLinearRail_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
void
battery_lab_custom_msg__srv__MoveLinearRail_Request__Sequence__fini(battery_lab_custom_msg__srv__MoveLinearRail_Request__Sequence * array);

/// Create array of srv/MoveLinearRail messages.
/**
 * It allocates the memory for the array and calls
 * battery_lab_custom_msg__srv__MoveLinearRail_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
battery_lab_custom_msg__srv__MoveLinearRail_Request__Sequence *
battery_lab_custom_msg__srv__MoveLinearRail_Request__Sequence__create(size_t size);

/// Destroy array of srv/MoveLinearRail messages.
/**
 * It calls
 * battery_lab_custom_msg__srv__MoveLinearRail_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
void
battery_lab_custom_msg__srv__MoveLinearRail_Request__Sequence__destroy(battery_lab_custom_msg__srv__MoveLinearRail_Request__Sequence * array);

/// Check for srv/MoveLinearRail message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
bool
battery_lab_custom_msg__srv__MoveLinearRail_Request__Sequence__are_equal(const battery_lab_custom_msg__srv__MoveLinearRail_Request__Sequence * lhs, const battery_lab_custom_msg__srv__MoveLinearRail_Request__Sequence * rhs);

/// Copy an array of srv/MoveLinearRail messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
bool
battery_lab_custom_msg__srv__MoveLinearRail_Request__Sequence__copy(
  const battery_lab_custom_msg__srv__MoveLinearRail_Request__Sequence * input,
  battery_lab_custom_msg__srv__MoveLinearRail_Request__Sequence * output);

/// Initialize srv/MoveLinearRail message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * battery_lab_custom_msg__srv__MoveLinearRail_Response
 * )) before or use
 * battery_lab_custom_msg__srv__MoveLinearRail_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
bool
battery_lab_custom_msg__srv__MoveLinearRail_Response__init(battery_lab_custom_msg__srv__MoveLinearRail_Response * msg);

/// Finalize srv/MoveLinearRail message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
void
battery_lab_custom_msg__srv__MoveLinearRail_Response__fini(battery_lab_custom_msg__srv__MoveLinearRail_Response * msg);

/// Create srv/MoveLinearRail message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * battery_lab_custom_msg__srv__MoveLinearRail_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
battery_lab_custom_msg__srv__MoveLinearRail_Response *
battery_lab_custom_msg__srv__MoveLinearRail_Response__create(void);

/// Destroy srv/MoveLinearRail message.
/**
 * It calls
 * battery_lab_custom_msg__srv__MoveLinearRail_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
void
battery_lab_custom_msg__srv__MoveLinearRail_Response__destroy(battery_lab_custom_msg__srv__MoveLinearRail_Response * msg);

/// Check for srv/MoveLinearRail message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
bool
battery_lab_custom_msg__srv__MoveLinearRail_Response__are_equal(const battery_lab_custom_msg__srv__MoveLinearRail_Response * lhs, const battery_lab_custom_msg__srv__MoveLinearRail_Response * rhs);

/// Copy a srv/MoveLinearRail message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
bool
battery_lab_custom_msg__srv__MoveLinearRail_Response__copy(
  const battery_lab_custom_msg__srv__MoveLinearRail_Response * input,
  battery_lab_custom_msg__srv__MoveLinearRail_Response * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
const rosidl_type_hash_t *
battery_lab_custom_msg__srv__MoveLinearRail_Response__get_type_hash(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
const rosidl_runtime_c__type_description__TypeDescription *
battery_lab_custom_msg__srv__MoveLinearRail_Response__get_type_description(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
const rosidl_runtime_c__type_description__TypeSource *
battery_lab_custom_msg__srv__MoveLinearRail_Response__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
const rosidl_runtime_c__type_description__TypeSource__Sequence *
battery_lab_custom_msg__srv__MoveLinearRail_Response__get_type_description_sources(
  const rosidl_message_type_support_t * type_support);

/// Initialize array of srv/MoveLinearRail messages.
/**
 * It allocates the memory for the number of elements and calls
 * battery_lab_custom_msg__srv__MoveLinearRail_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
bool
battery_lab_custom_msg__srv__MoveLinearRail_Response__Sequence__init(battery_lab_custom_msg__srv__MoveLinearRail_Response__Sequence * array, size_t size);

/// Finalize array of srv/MoveLinearRail messages.
/**
 * It calls
 * battery_lab_custom_msg__srv__MoveLinearRail_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
void
battery_lab_custom_msg__srv__MoveLinearRail_Response__Sequence__fini(battery_lab_custom_msg__srv__MoveLinearRail_Response__Sequence * array);

/// Create array of srv/MoveLinearRail messages.
/**
 * It allocates the memory for the array and calls
 * battery_lab_custom_msg__srv__MoveLinearRail_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
battery_lab_custom_msg__srv__MoveLinearRail_Response__Sequence *
battery_lab_custom_msg__srv__MoveLinearRail_Response__Sequence__create(size_t size);

/// Destroy array of srv/MoveLinearRail messages.
/**
 * It calls
 * battery_lab_custom_msg__srv__MoveLinearRail_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
void
battery_lab_custom_msg__srv__MoveLinearRail_Response__Sequence__destroy(battery_lab_custom_msg__srv__MoveLinearRail_Response__Sequence * array);

/// Check for srv/MoveLinearRail message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
bool
battery_lab_custom_msg__srv__MoveLinearRail_Response__Sequence__are_equal(const battery_lab_custom_msg__srv__MoveLinearRail_Response__Sequence * lhs, const battery_lab_custom_msg__srv__MoveLinearRail_Response__Sequence * rhs);

/// Copy an array of srv/MoveLinearRail messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
bool
battery_lab_custom_msg__srv__MoveLinearRail_Response__Sequence__copy(
  const battery_lab_custom_msg__srv__MoveLinearRail_Response__Sequence * input,
  battery_lab_custom_msg__srv__MoveLinearRail_Response__Sequence * output);

/// Initialize srv/MoveLinearRail message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * battery_lab_custom_msg__srv__MoveLinearRail_Event
 * )) before or use
 * battery_lab_custom_msg__srv__MoveLinearRail_Event__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
bool
battery_lab_custom_msg__srv__MoveLinearRail_Event__init(battery_lab_custom_msg__srv__MoveLinearRail_Event * msg);

/// Finalize srv/MoveLinearRail message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
void
battery_lab_custom_msg__srv__MoveLinearRail_Event__fini(battery_lab_custom_msg__srv__MoveLinearRail_Event * msg);

/// Create srv/MoveLinearRail message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * battery_lab_custom_msg__srv__MoveLinearRail_Event__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
battery_lab_custom_msg__srv__MoveLinearRail_Event *
battery_lab_custom_msg__srv__MoveLinearRail_Event__create(void);

/// Destroy srv/MoveLinearRail message.
/**
 * It calls
 * battery_lab_custom_msg__srv__MoveLinearRail_Event__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
void
battery_lab_custom_msg__srv__MoveLinearRail_Event__destroy(battery_lab_custom_msg__srv__MoveLinearRail_Event * msg);

/// Check for srv/MoveLinearRail message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
bool
battery_lab_custom_msg__srv__MoveLinearRail_Event__are_equal(const battery_lab_custom_msg__srv__MoveLinearRail_Event * lhs, const battery_lab_custom_msg__srv__MoveLinearRail_Event * rhs);

/// Copy a srv/MoveLinearRail message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
bool
battery_lab_custom_msg__srv__MoveLinearRail_Event__copy(
  const battery_lab_custom_msg__srv__MoveLinearRail_Event * input,
  battery_lab_custom_msg__srv__MoveLinearRail_Event * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
const rosidl_type_hash_t *
battery_lab_custom_msg__srv__MoveLinearRail_Event__get_type_hash(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
const rosidl_runtime_c__type_description__TypeDescription *
battery_lab_custom_msg__srv__MoveLinearRail_Event__get_type_description(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
const rosidl_runtime_c__type_description__TypeSource *
battery_lab_custom_msg__srv__MoveLinearRail_Event__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
const rosidl_runtime_c__type_description__TypeSource__Sequence *
battery_lab_custom_msg__srv__MoveLinearRail_Event__get_type_description_sources(
  const rosidl_message_type_support_t * type_support);

/// Initialize array of srv/MoveLinearRail messages.
/**
 * It allocates the memory for the number of elements and calls
 * battery_lab_custom_msg__srv__MoveLinearRail_Event__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
bool
battery_lab_custom_msg__srv__MoveLinearRail_Event__Sequence__init(battery_lab_custom_msg__srv__MoveLinearRail_Event__Sequence * array, size_t size);

/// Finalize array of srv/MoveLinearRail messages.
/**
 * It calls
 * battery_lab_custom_msg__srv__MoveLinearRail_Event__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
void
battery_lab_custom_msg__srv__MoveLinearRail_Event__Sequence__fini(battery_lab_custom_msg__srv__MoveLinearRail_Event__Sequence * array);

/// Create array of srv/MoveLinearRail messages.
/**
 * It allocates the memory for the array and calls
 * battery_lab_custom_msg__srv__MoveLinearRail_Event__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
battery_lab_custom_msg__srv__MoveLinearRail_Event__Sequence *
battery_lab_custom_msg__srv__MoveLinearRail_Event__Sequence__create(size_t size);

/// Destroy array of srv/MoveLinearRail messages.
/**
 * It calls
 * battery_lab_custom_msg__srv__MoveLinearRail_Event__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
void
battery_lab_custom_msg__srv__MoveLinearRail_Event__Sequence__destroy(battery_lab_custom_msg__srv__MoveLinearRail_Event__Sequence * array);

/// Check for srv/MoveLinearRail message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
bool
battery_lab_custom_msg__srv__MoveLinearRail_Event__Sequence__are_equal(const battery_lab_custom_msg__srv__MoveLinearRail_Event__Sequence * lhs, const battery_lab_custom_msg__srv__MoveLinearRail_Event__Sequence * rhs);

/// Copy an array of srv/MoveLinearRail messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_battery_lab_custom_msg
bool
battery_lab_custom_msg__srv__MoveLinearRail_Event__Sequence__copy(
  const battery_lab_custom_msg__srv__MoveLinearRail_Event__Sequence * input,
  battery_lab_custom_msg__srv__MoveLinearRail_Event__Sequence * output);
#ifdef __cplusplus
}
#endif

#endif  // BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__MOVE_LINEAR_RAIL__FUNCTIONS_H_
