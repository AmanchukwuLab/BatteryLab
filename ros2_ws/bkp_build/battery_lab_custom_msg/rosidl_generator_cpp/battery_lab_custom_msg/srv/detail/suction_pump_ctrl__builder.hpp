// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from battery_lab_custom_msg:srv/SuctionPumpCtrl.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "battery_lab_custom_msg/srv/suction_pump_ctrl.hpp"


#ifndef BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__SUCTION_PUMP_CTRL__BUILDER_HPP_
#define BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__SUCTION_PUMP_CTRL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "battery_lab_custom_msg/srv/detail/suction_pump_ctrl__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace battery_lab_custom_msg
{

namespace srv
{

namespace builder
{

class Init_SuctionPumpCtrl_Request_command
{
public:
  Init_SuctionPumpCtrl_Request_command()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::battery_lab_custom_msg::srv::SuctionPumpCtrl_Request command(::battery_lab_custom_msg::srv::SuctionPumpCtrl_Request::_command_type arg)
  {
    msg_.command = std::move(arg);
    return std::move(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::SuctionPumpCtrl_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::battery_lab_custom_msg::srv::SuctionPumpCtrl_Request>()
{
  return battery_lab_custom_msg::srv::builder::Init_SuctionPumpCtrl_Request_command();
}

}  // namespace battery_lab_custom_msg


namespace battery_lab_custom_msg
{

namespace srv
{

namespace builder
{

class Init_SuctionPumpCtrl_Response_status
{
public:
  Init_SuctionPumpCtrl_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::battery_lab_custom_msg::srv::SuctionPumpCtrl_Response status(::battery_lab_custom_msg::srv::SuctionPumpCtrl_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return std::move(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::SuctionPumpCtrl_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::battery_lab_custom_msg::srv::SuctionPumpCtrl_Response>()
{
  return battery_lab_custom_msg::srv::builder::Init_SuctionPumpCtrl_Response_status();
}

}  // namespace battery_lab_custom_msg


namespace battery_lab_custom_msg
{

namespace srv
{

namespace builder
{

class Init_SuctionPumpCtrl_Event_response
{
public:
  explicit Init_SuctionPumpCtrl_Event_response(::battery_lab_custom_msg::srv::SuctionPumpCtrl_Event & msg)
  : msg_(msg)
  {}
  ::battery_lab_custom_msg::srv::SuctionPumpCtrl_Event response(::battery_lab_custom_msg::srv::SuctionPumpCtrl_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::SuctionPumpCtrl_Event msg_;
};

class Init_SuctionPumpCtrl_Event_request
{
public:
  explicit Init_SuctionPumpCtrl_Event_request(::battery_lab_custom_msg::srv::SuctionPumpCtrl_Event & msg)
  : msg_(msg)
  {}
  Init_SuctionPumpCtrl_Event_response request(::battery_lab_custom_msg::srv::SuctionPumpCtrl_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_SuctionPumpCtrl_Event_response(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::SuctionPumpCtrl_Event msg_;
};

class Init_SuctionPumpCtrl_Event_info
{
public:
  Init_SuctionPumpCtrl_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SuctionPumpCtrl_Event_request info(::battery_lab_custom_msg::srv::SuctionPumpCtrl_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_SuctionPumpCtrl_Event_request(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::SuctionPumpCtrl_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::battery_lab_custom_msg::srv::SuctionPumpCtrl_Event>()
{
  return battery_lab_custom_msg::srv::builder::Init_SuctionPumpCtrl_Event_info();
}

}  // namespace battery_lab_custom_msg

#endif  // BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__SUCTION_PUMP_CTRL__BUILDER_HPP_
