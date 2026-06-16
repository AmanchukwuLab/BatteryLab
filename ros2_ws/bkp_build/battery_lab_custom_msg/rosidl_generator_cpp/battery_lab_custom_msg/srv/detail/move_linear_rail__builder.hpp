// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from battery_lab_custom_msg:srv/MoveLinearRail.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "battery_lab_custom_msg/srv/move_linear_rail.hpp"


#ifndef BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__MOVE_LINEAR_RAIL__BUILDER_HPP_
#define BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__MOVE_LINEAR_RAIL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "battery_lab_custom_msg/srv/detail/move_linear_rail__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace battery_lab_custom_msg
{

namespace srv
{

namespace builder
{

class Init_MoveLinearRail_Request_target_position
{
public:
  Init_MoveLinearRail_Request_target_position()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::battery_lab_custom_msg::srv::MoveLinearRail_Request target_position(::battery_lab_custom_msg::srv::MoveLinearRail_Request::_target_position_type arg)
  {
    msg_.target_position = std::move(arg);
    return std::move(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::MoveLinearRail_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::battery_lab_custom_msg::srv::MoveLinearRail_Request>()
{
  return battery_lab_custom_msg::srv::builder::Init_MoveLinearRail_Request_target_position();
}

}  // namespace battery_lab_custom_msg


namespace battery_lab_custom_msg
{

namespace srv
{

namespace builder
{

class Init_MoveLinearRail_Response_success
{
public:
  Init_MoveLinearRail_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::battery_lab_custom_msg::srv::MoveLinearRail_Response success(::battery_lab_custom_msg::srv::MoveLinearRail_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::MoveLinearRail_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::battery_lab_custom_msg::srv::MoveLinearRail_Response>()
{
  return battery_lab_custom_msg::srv::builder::Init_MoveLinearRail_Response_success();
}

}  // namespace battery_lab_custom_msg


namespace battery_lab_custom_msg
{

namespace srv
{

namespace builder
{

class Init_MoveLinearRail_Event_response
{
public:
  explicit Init_MoveLinearRail_Event_response(::battery_lab_custom_msg::srv::MoveLinearRail_Event & msg)
  : msg_(msg)
  {}
  ::battery_lab_custom_msg::srv::MoveLinearRail_Event response(::battery_lab_custom_msg::srv::MoveLinearRail_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::MoveLinearRail_Event msg_;
};

class Init_MoveLinearRail_Event_request
{
public:
  explicit Init_MoveLinearRail_Event_request(::battery_lab_custom_msg::srv::MoveLinearRail_Event & msg)
  : msg_(msg)
  {}
  Init_MoveLinearRail_Event_response request(::battery_lab_custom_msg::srv::MoveLinearRail_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_MoveLinearRail_Event_response(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::MoveLinearRail_Event msg_;
};

class Init_MoveLinearRail_Event_info
{
public:
  Init_MoveLinearRail_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveLinearRail_Event_request info(::battery_lab_custom_msg::srv::MoveLinearRail_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_MoveLinearRail_Event_request(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::MoveLinearRail_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::battery_lab_custom_msg::srv::MoveLinearRail_Event>()
{
  return battery_lab_custom_msg::srv::builder::Init_MoveLinearRail_Event_info();
}

}  // namespace battery_lab_custom_msg

#endif  // BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__MOVE_LINEAR_RAIL__BUILDER_HPP_
