// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from battery_lab_custom_msg:srv/CaptureImage.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "battery_lab_custom_msg/srv/capture_image.hpp"


#ifndef BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__CAPTURE_IMAGE__BUILDER_HPP_
#define BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__CAPTURE_IMAGE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "battery_lab_custom_msg/srv/detail/capture_image__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace battery_lab_custom_msg
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::battery_lab_custom_msg::srv::CaptureImage_Request>()
{
  return ::battery_lab_custom_msg::srv::CaptureImage_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace battery_lab_custom_msg


namespace battery_lab_custom_msg
{

namespace srv
{

namespace builder
{

class Init_CaptureImage_Response_image
{
public:
  Init_CaptureImage_Response_image()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::battery_lab_custom_msg::srv::CaptureImage_Response image(::battery_lab_custom_msg::srv::CaptureImage_Response::_image_type arg)
  {
    msg_.image = std::move(arg);
    return std::move(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::CaptureImage_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::battery_lab_custom_msg::srv::CaptureImage_Response>()
{
  return battery_lab_custom_msg::srv::builder::Init_CaptureImage_Response_image();
}

}  // namespace battery_lab_custom_msg


namespace battery_lab_custom_msg
{

namespace srv
{

namespace builder
{

class Init_CaptureImage_Event_response
{
public:
  explicit Init_CaptureImage_Event_response(::battery_lab_custom_msg::srv::CaptureImage_Event & msg)
  : msg_(msg)
  {}
  ::battery_lab_custom_msg::srv::CaptureImage_Event response(::battery_lab_custom_msg::srv::CaptureImage_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::CaptureImage_Event msg_;
};

class Init_CaptureImage_Event_request
{
public:
  explicit Init_CaptureImage_Event_request(::battery_lab_custom_msg::srv::CaptureImage_Event & msg)
  : msg_(msg)
  {}
  Init_CaptureImage_Event_response request(::battery_lab_custom_msg::srv::CaptureImage_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_CaptureImage_Event_response(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::CaptureImage_Event msg_;
};

class Init_CaptureImage_Event_info
{
public:
  Init_CaptureImage_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CaptureImage_Event_request info(::battery_lab_custom_msg::srv::CaptureImage_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_CaptureImage_Event_request(msg_);
  }

private:
  ::battery_lab_custom_msg::srv::CaptureImage_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::battery_lab_custom_msg::srv::CaptureImage_Event>()
{
  return battery_lab_custom_msg::srv::builder::Init_CaptureImage_Event_info();
}

}  // namespace battery_lab_custom_msg

#endif  // BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__CAPTURE_IMAGE__BUILDER_HPP_
