// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from battery_lab_custom_msg:srv/GetAbsRailPos.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "battery_lab_custom_msg/srv/get_abs_rail_pos.hpp"


#ifndef BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__GET_ABS_RAIL_POS__TRAITS_HPP_
#define BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__GET_ABS_RAIL_POS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "battery_lab_custom_msg/srv/detail/get_abs_rail_pos__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace battery_lab_custom_msg
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetAbsRailPos_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: get
  {
    out << "get: ";
    rosidl_generator_traits::value_to_yaml(msg.get, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetAbsRailPos_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: get
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "get: ";
    rosidl_generator_traits::value_to_yaml(msg.get, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetAbsRailPos_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace battery_lab_custom_msg

namespace rosidl_generator_traits
{

[[deprecated("use battery_lab_custom_msg::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const battery_lab_custom_msg::srv::GetAbsRailPos_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  battery_lab_custom_msg::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use battery_lab_custom_msg::srv::to_yaml() instead")]]
inline std::string to_yaml(const battery_lab_custom_msg::srv::GetAbsRailPos_Request & msg)
{
  return battery_lab_custom_msg::srv::to_yaml(msg);
}

template<>
inline const char * data_type<battery_lab_custom_msg::srv::GetAbsRailPos_Request>()
{
  return "battery_lab_custom_msg::srv::GetAbsRailPos_Request";
}

template<>
inline const char * name<battery_lab_custom_msg::srv::GetAbsRailPos_Request>()
{
  return "battery_lab_custom_msg/srv/GetAbsRailPos_Request";
}

template<>
struct has_fixed_size<battery_lab_custom_msg::srv::GetAbsRailPos_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<battery_lab_custom_msg::srv::GetAbsRailPos_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<battery_lab_custom_msg::srv::GetAbsRailPos_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace battery_lab_custom_msg
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetAbsRailPos_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: current_pos
  {
    out << "current_pos: ";
    rosidl_generator_traits::value_to_yaml(msg.current_pos, out);
    out << ", ";
  }

  // member: connected
  {
    out << "connected: ";
    rosidl_generator_traits::value_to_yaml(msg.connected, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetAbsRailPos_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: current_pos
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "current_pos: ";
    rosidl_generator_traits::value_to_yaml(msg.current_pos, out);
    out << "\n";
  }

  // member: connected
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "connected: ";
    rosidl_generator_traits::value_to_yaml(msg.connected, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetAbsRailPos_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace battery_lab_custom_msg

namespace rosidl_generator_traits
{

[[deprecated("use battery_lab_custom_msg::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const battery_lab_custom_msg::srv::GetAbsRailPos_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  battery_lab_custom_msg::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use battery_lab_custom_msg::srv::to_yaml() instead")]]
inline std::string to_yaml(const battery_lab_custom_msg::srv::GetAbsRailPos_Response & msg)
{
  return battery_lab_custom_msg::srv::to_yaml(msg);
}

template<>
inline const char * data_type<battery_lab_custom_msg::srv::GetAbsRailPos_Response>()
{
  return "battery_lab_custom_msg::srv::GetAbsRailPos_Response";
}

template<>
inline const char * name<battery_lab_custom_msg::srv::GetAbsRailPos_Response>()
{
  return "battery_lab_custom_msg/srv/GetAbsRailPos_Response";
}

template<>
struct has_fixed_size<battery_lab_custom_msg::srv::GetAbsRailPos_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<battery_lab_custom_msg::srv::GetAbsRailPos_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<battery_lab_custom_msg::srv::GetAbsRailPos_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__traits.hpp"

namespace battery_lab_custom_msg
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetAbsRailPos_Event & msg,
  std::ostream & out)
{
  out << "{";
  // member: info
  {
    out << "info: ";
    to_flow_style_yaml(msg.info, out);
    out << ", ";
  }

  // member: request
  {
    if (msg.request.size() == 0) {
      out << "request: []";
    } else {
      out << "request: [";
      size_t pending_items = msg.request.size();
      for (auto item : msg.request) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: response
  {
    if (msg.response.size() == 0) {
      out << "response: []";
    } else {
      out << "response: [";
      size_t pending_items = msg.response.size();
      for (auto item : msg.response) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetAbsRailPos_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: info
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "info:\n";
    to_block_style_yaml(msg.info, out, indentation + 2);
  }

  // member: request
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.request.size() == 0) {
      out << "request: []\n";
    } else {
      out << "request:\n";
      for (auto item : msg.request) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: response
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.response.size() == 0) {
      out << "response: []\n";
    } else {
      out << "response:\n";
      for (auto item : msg.response) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetAbsRailPos_Event & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace battery_lab_custom_msg

namespace rosidl_generator_traits
{

[[deprecated("use battery_lab_custom_msg::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const battery_lab_custom_msg::srv::GetAbsRailPos_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  battery_lab_custom_msg::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use battery_lab_custom_msg::srv::to_yaml() instead")]]
inline std::string to_yaml(const battery_lab_custom_msg::srv::GetAbsRailPos_Event & msg)
{
  return battery_lab_custom_msg::srv::to_yaml(msg);
}

template<>
inline const char * data_type<battery_lab_custom_msg::srv::GetAbsRailPos_Event>()
{
  return "battery_lab_custom_msg::srv::GetAbsRailPos_Event";
}

template<>
inline const char * name<battery_lab_custom_msg::srv::GetAbsRailPos_Event>()
{
  return "battery_lab_custom_msg/srv/GetAbsRailPos_Event";
}

template<>
struct has_fixed_size<battery_lab_custom_msg::srv::GetAbsRailPos_Event>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<battery_lab_custom_msg::srv::GetAbsRailPos_Event>
  : std::integral_constant<bool, has_bounded_size<battery_lab_custom_msg::srv::GetAbsRailPos_Request>::value && has_bounded_size<battery_lab_custom_msg::srv::GetAbsRailPos_Response>::value && has_bounded_size<service_msgs::msg::ServiceEventInfo>::value> {};

template<>
struct is_message<battery_lab_custom_msg::srv::GetAbsRailPos_Event>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<battery_lab_custom_msg::srv::GetAbsRailPos>()
{
  return "battery_lab_custom_msg::srv::GetAbsRailPos";
}

template<>
inline const char * name<battery_lab_custom_msg::srv::GetAbsRailPos>()
{
  return "battery_lab_custom_msg/srv/GetAbsRailPos";
}

template<>
struct has_fixed_size<battery_lab_custom_msg::srv::GetAbsRailPos>
  : std::integral_constant<
    bool,
    has_fixed_size<battery_lab_custom_msg::srv::GetAbsRailPos_Request>::value &&
    has_fixed_size<battery_lab_custom_msg::srv::GetAbsRailPos_Response>::value
  >
{
};

template<>
struct has_bounded_size<battery_lab_custom_msg::srv::GetAbsRailPos>
  : std::integral_constant<
    bool,
    has_bounded_size<battery_lab_custom_msg::srv::GetAbsRailPos_Request>::value &&
    has_bounded_size<battery_lab_custom_msg::srv::GetAbsRailPos_Response>::value
  >
{
};

template<>
struct is_service<battery_lab_custom_msg::srv::GetAbsRailPos>
  : std::true_type
{
};

template<>
struct is_service_request<battery_lab_custom_msg::srv::GetAbsRailPos_Request>
  : std::true_type
{
};

template<>
struct is_service_response<battery_lab_custom_msg::srv::GetAbsRailPos_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__GET_ABS_RAIL_POS__TRAITS_HPP_
