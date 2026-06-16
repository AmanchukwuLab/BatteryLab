// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from battery_lab_custom_msg:srv/SartoriusCtrl.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "battery_lab_custom_msg/srv/sartorius_ctrl.hpp"


#ifndef BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__SARTORIUS_CTRL__BUILDER_HPP_
#define BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__SARTORIUS_CTRL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "battery_lab_custom_msg/srv/detail/sartorius_ctrl__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace battery_lab_custom_msg
{

namespace srv
{

namespace builder
{

class Init_SartoriusCtrl_Request_volume
{
public:
  explicit Init_SartoriusCtrl_Request_volume(::battery_lab_custom_msg::srv::SartoriusCtrl_Request & msg)
  : msg_(msg)
  {}
  ::battery_lab_custom_msg::srv::SartoriusCtrl_Request volume(::battery_lab_custom_msg::srv::SartoriusCtrl_Request::_volume_type arg)
  {
    msg_.volume = std::move(arg);
    return std::move(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::SartoriusCtrl_Request msg_;
};

class Init_SartoriusCtrl_Request_command
{
public:
  Init_SartoriusCtrl_Request_command()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SartoriusCtrl_Request_volume command(::battery_lab_custom_msg::srv::SartoriusCtrl_Request::_command_type arg)
  {
    msg_.command = std::move(arg);
    return Init_SartoriusCtrl_Request_volume(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::SartoriusCtrl_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::battery_lab_custom_msg::srv::SartoriusCtrl_Request>()
{
  return battery_lab_custom_msg::srv::builder::Init_SartoriusCtrl_Request_command();
}

}  // namespace battery_lab_custom_msg


namespace battery_lab_custom_msg
{

namespace srv
{

namespace builder
{

class Init_SartoriusCtrl_Response_int_result
{
public:
  explicit Init_SartoriusCtrl_Response_int_result(::battery_lab_custom_msg::srv::SartoriusCtrl_Response & msg)
  : msg_(msg)
  {}
  ::battery_lab_custom_msg::srv::SartoriusCtrl_Response int_result(::battery_lab_custom_msg::srv::SartoriusCtrl_Response::_int_result_type arg)
  {
    msg_.int_result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::SartoriusCtrl_Response msg_;
};

class Init_SartoriusCtrl_Response_float_result
{
public:
  explicit Init_SartoriusCtrl_Response_float_result(::battery_lab_custom_msg::srv::SartoriusCtrl_Response & msg)
  : msg_(msg)
  {}
  Init_SartoriusCtrl_Response_int_result float_result(::battery_lab_custom_msg::srv::SartoriusCtrl_Response::_float_result_type arg)
  {
    msg_.float_result = std::move(arg);
    return Init_SartoriusCtrl_Response_int_result(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::SartoriusCtrl_Response msg_;
};

class Init_SartoriusCtrl_Response_status
{
public:
  Init_SartoriusCtrl_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SartoriusCtrl_Response_float_result status(::battery_lab_custom_msg::srv::SartoriusCtrl_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_SartoriusCtrl_Response_float_result(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::SartoriusCtrl_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::battery_lab_custom_msg::srv::SartoriusCtrl_Response>()
{
  return battery_lab_custom_msg::srv::builder::Init_SartoriusCtrl_Response_status();
}

}  // namespace battery_lab_custom_msg


namespace battery_lab_custom_msg
{

namespace srv
{

namespace builder
{

class Init_SartoriusCtrl_Event_response
{
public:
  explicit Init_SartoriusCtrl_Event_response(::battery_lab_custom_msg::srv::SartoriusCtrl_Event & msg)
  : msg_(msg)
  {}
  ::battery_lab_custom_msg::srv::SartoriusCtrl_Event response(::battery_lab_custom_msg::srv::SartoriusCtrl_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::SartoriusCtrl_Event msg_;
};

class Init_SartoriusCtrl_Event_request
{
public:
  explicit Init_SartoriusCtrl_Event_request(::battery_lab_custom_msg::srv::SartoriusCtrl_Event & msg)
  : msg_(msg)
  {}
  Init_SartoriusCtrl_Event_response request(::battery_lab_custom_msg::srv::SartoriusCtrl_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_SartoriusCtrl_Event_response(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::SartoriusCtrl_Event msg_;
};

class Init_SartoriusCtrl_Event_info
{
public:
  Init_SartoriusCtrl_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SartoriusCtrl_Event_request info(::battery_lab_custom_msg::srv::SartoriusCtrl_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_SartoriusCtrl_Event_request(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::SartoriusCtrl_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::battery_lab_custom_msg::srv::SartoriusCtrl_Event>()
{
  return battery_lab_custom_msg::srv::builder::Init_SartoriusCtrl_Event_info();
}

}  // namespace battery_lab_custom_msg

#endif  // BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__SARTORIUS_CTRL__BUILDER_HPP_
