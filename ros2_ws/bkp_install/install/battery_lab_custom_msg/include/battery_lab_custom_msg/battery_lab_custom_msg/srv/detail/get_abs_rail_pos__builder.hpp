// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from battery_lab_custom_msg:srv/GetAbsRailPos.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "battery_lab_custom_msg/srv/get_abs_rail_pos.hpp"


#ifndef BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__GET_ABS_RAIL_POS__BUILDER_HPP_
#define BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__GET_ABS_RAIL_POS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "battery_lab_custom_msg/srv/detail/get_abs_rail_pos__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace battery_lab_custom_msg
{

namespace srv
{

namespace builder
{

class Init_GetAbsRailPos_Request_get
{
public:
  Init_GetAbsRailPos_Request_get()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::battery_lab_custom_msg::srv::GetAbsRailPos_Request get(::battery_lab_custom_msg::srv::GetAbsRailPos_Request::_get_type arg)
  {
    msg_.get = std::move(arg);
    return std::move(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::GetAbsRailPos_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::battery_lab_custom_msg::srv::GetAbsRailPos_Request>()
{
  return battery_lab_custom_msg::srv::builder::Init_GetAbsRailPos_Request_get();
}

}  // namespace battery_lab_custom_msg


namespace battery_lab_custom_msg
{

namespace srv
{

namespace builder
{

class Init_GetAbsRailPos_Response_connected
{
public:
  explicit Init_GetAbsRailPos_Response_connected(::battery_lab_custom_msg::srv::GetAbsRailPos_Response & msg)
  : msg_(msg)
  {}
  ::battery_lab_custom_msg::srv::GetAbsRailPos_Response connected(::battery_lab_custom_msg::srv::GetAbsRailPos_Response::_connected_type arg)
  {
    msg_.connected = std::move(arg);
    return std::move(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::GetAbsRailPos_Response msg_;
};

class Init_GetAbsRailPos_Response_current_pos
{
public:
  Init_GetAbsRailPos_Response_current_pos()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GetAbsRailPos_Response_connected current_pos(::battery_lab_custom_msg::srv::GetAbsRailPos_Response::_current_pos_type arg)
  {
    msg_.current_pos = std::move(arg);
    return Init_GetAbsRailPos_Response_connected(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::GetAbsRailPos_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::battery_lab_custom_msg::srv::GetAbsRailPos_Response>()
{
  return battery_lab_custom_msg::srv::builder::Init_GetAbsRailPos_Response_current_pos();
}

}  // namespace battery_lab_custom_msg


namespace battery_lab_custom_msg
{

namespace srv
{

namespace builder
{

class Init_GetAbsRailPos_Event_response
{
public:
  explicit Init_GetAbsRailPos_Event_response(::battery_lab_custom_msg::srv::GetAbsRailPos_Event & msg)
  : msg_(msg)
  {}
  ::battery_lab_custom_msg::srv::GetAbsRailPos_Event response(::battery_lab_custom_msg::srv::GetAbsRailPos_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::GetAbsRailPos_Event msg_;
};

class Init_GetAbsRailPos_Event_request
{
public:
  explicit Init_GetAbsRailPos_Event_request(::battery_lab_custom_msg::srv::GetAbsRailPos_Event & msg)
  : msg_(msg)
  {}
  Init_GetAbsRailPos_Event_response request(::battery_lab_custom_msg::srv::GetAbsRailPos_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_GetAbsRailPos_Event_response(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::GetAbsRailPos_Event msg_;
};

class Init_GetAbsRailPos_Event_info
{
public:
  Init_GetAbsRailPos_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GetAbsRailPos_Event_request info(::battery_lab_custom_msg::srv::GetAbsRailPos_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_GetAbsRailPos_Event_request(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::GetAbsRailPos_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::battery_lab_custom_msg::srv::GetAbsRailPos_Event>()
{
  return battery_lab_custom_msg::srv::builder::Init_GetAbsRailPos_Event_info();
}

}  // namespace battery_lab_custom_msg

#endif  // BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__GET_ABS_RAIL_POS__BUILDER_HPP_
