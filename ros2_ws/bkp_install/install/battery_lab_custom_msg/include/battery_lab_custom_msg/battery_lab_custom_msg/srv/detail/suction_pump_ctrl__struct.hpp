// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from battery_lab_custom_msg:srv/SuctionPumpCtrl.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "battery_lab_custom_msg/srv/suction_pump_ctrl.hpp"


#ifndef BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__SUCTION_PUMP_CTRL__STRUCT_HPP_
#define BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__SUCTION_PUMP_CTRL__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__battery_lab_custom_msg__srv__SuctionPumpCtrl_Request __attribute__((deprecated))
#else
# define DEPRECATED__battery_lab_custom_msg__srv__SuctionPumpCtrl_Request __declspec(deprecated)
#endif

namespace battery_lab_custom_msg
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct SuctionPumpCtrl_Request_
{
  using Type = SuctionPumpCtrl_Request_<ContainerAllocator>;

  explicit SuctionPumpCtrl_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->command = "";
    }
  }

  explicit SuctionPumpCtrl_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : command(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->command = "";
    }
  }

  // field types and members
  using _command_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _command_type command;

  // setters for named parameter idiom
  Type & set__command(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->command = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    battery_lab_custom_msg::srv::SuctionPumpCtrl_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const battery_lab_custom_msg::srv::SuctionPumpCtrl_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<battery_lab_custom_msg::srv::SuctionPumpCtrl_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<battery_lab_custom_msg::srv::SuctionPumpCtrl_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      battery_lab_custom_msg::srv::SuctionPumpCtrl_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<battery_lab_custom_msg::srv::SuctionPumpCtrl_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      battery_lab_custom_msg::srv::SuctionPumpCtrl_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<battery_lab_custom_msg::srv::SuctionPumpCtrl_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<battery_lab_custom_msg::srv::SuctionPumpCtrl_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<battery_lab_custom_msg::srv::SuctionPumpCtrl_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__battery_lab_custom_msg__srv__SuctionPumpCtrl_Request
    std::shared_ptr<battery_lab_custom_msg::srv::SuctionPumpCtrl_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__battery_lab_custom_msg__srv__SuctionPumpCtrl_Request
    std::shared_ptr<battery_lab_custom_msg::srv::SuctionPumpCtrl_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SuctionPumpCtrl_Request_ & other) const
  {
    if (this->command != other.command) {
      return false;
    }
    return true;
  }
  bool operator!=(const SuctionPumpCtrl_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SuctionPumpCtrl_Request_

// alias to use template instance with default allocator
using SuctionPumpCtrl_Request =
  battery_lab_custom_msg::srv::SuctionPumpCtrl_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace battery_lab_custom_msg


#ifndef _WIN32
# define DEPRECATED__battery_lab_custom_msg__srv__SuctionPumpCtrl_Response __attribute__((deprecated))
#else
# define DEPRECATED__battery_lab_custom_msg__srv__SuctionPumpCtrl_Response __declspec(deprecated)
#endif

namespace battery_lab_custom_msg
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct SuctionPumpCtrl_Response_
{
  using Type = SuctionPumpCtrl_Response_<ContainerAllocator>;

  explicit SuctionPumpCtrl_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = "";
    }
  }

  explicit SuctionPumpCtrl_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : status(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = "";
    }
  }

  // field types and members
  using _status_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _status_type status;

  // setters for named parameter idiom
  Type & set__status(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->status = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    battery_lab_custom_msg::srv::SuctionPumpCtrl_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const battery_lab_custom_msg::srv::SuctionPumpCtrl_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<battery_lab_custom_msg::srv::SuctionPumpCtrl_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<battery_lab_custom_msg::srv::SuctionPumpCtrl_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      battery_lab_custom_msg::srv::SuctionPumpCtrl_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<battery_lab_custom_msg::srv::SuctionPumpCtrl_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      battery_lab_custom_msg::srv::SuctionPumpCtrl_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<battery_lab_custom_msg::srv::SuctionPumpCtrl_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<battery_lab_custom_msg::srv::SuctionPumpCtrl_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<battery_lab_custom_msg::srv::SuctionPumpCtrl_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__battery_lab_custom_msg__srv__SuctionPumpCtrl_Response
    std::shared_ptr<battery_lab_custom_msg::srv::SuctionPumpCtrl_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__battery_lab_custom_msg__srv__SuctionPumpCtrl_Response
    std::shared_ptr<battery_lab_custom_msg::srv::SuctionPumpCtrl_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SuctionPumpCtrl_Response_ & other) const
  {
    if (this->status != other.status) {
      return false;
    }
    return true;
  }
  bool operator!=(const SuctionPumpCtrl_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SuctionPumpCtrl_Response_

// alias to use template instance with default allocator
using SuctionPumpCtrl_Response =
  battery_lab_custom_msg::srv::SuctionPumpCtrl_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace battery_lab_custom_msg


// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__battery_lab_custom_msg__srv__SuctionPumpCtrl_Event __attribute__((deprecated))
#else
# define DEPRECATED__battery_lab_custom_msg__srv__SuctionPumpCtrl_Event __declspec(deprecated)
#endif

namespace battery_lab_custom_msg
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct SuctionPumpCtrl_Event_
{
  using Type = SuctionPumpCtrl_Event_<ContainerAllocator>;

  explicit SuctionPumpCtrl_Event_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_init)
  {
    (void)_init;
  }

  explicit SuctionPumpCtrl_Event_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _info_type =
    service_msgs::msg::ServiceEventInfo_<ContainerAllocator>;
  _info_type info;
  using _request_type =
    rosidl_runtime_cpp::BoundedVector<battery_lab_custom_msg::srv::SuctionPumpCtrl_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<battery_lab_custom_msg::srv::SuctionPumpCtrl_Request_<ContainerAllocator>>>;
  _request_type request;
  using _response_type =
    rosidl_runtime_cpp::BoundedVector<battery_lab_custom_msg::srv::SuctionPumpCtrl_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<battery_lab_custom_msg::srv::SuctionPumpCtrl_Response_<ContainerAllocator>>>;
  _response_type response;

  // setters for named parameter idiom
  Type & set__info(
    const service_msgs::msg::ServiceEventInfo_<ContainerAllocator> & _arg)
  {
    this->info = _arg;
    return *this;
  }
  Type & set__request(
    const rosidl_runtime_cpp::BoundedVector<battery_lab_custom_msg::srv::SuctionPumpCtrl_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<battery_lab_custom_msg::srv::SuctionPumpCtrl_Request_<ContainerAllocator>>> & _arg)
  {
    this->request = _arg;
    return *this;
  }
  Type & set__response(
    const rosidl_runtime_cpp::BoundedVector<battery_lab_custom_msg::srv::SuctionPumpCtrl_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<battery_lab_custom_msg::srv::SuctionPumpCtrl_Response_<ContainerAllocator>>> & _arg)
  {
    this->response = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    battery_lab_custom_msg::srv::SuctionPumpCtrl_Event_<ContainerAllocator> *;
  using ConstRawPtr =
    const battery_lab_custom_msg::srv::SuctionPumpCtrl_Event_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<battery_lab_custom_msg::srv::SuctionPumpCtrl_Event_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<battery_lab_custom_msg::srv::SuctionPumpCtrl_Event_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      battery_lab_custom_msg::srv::SuctionPumpCtrl_Event_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<battery_lab_custom_msg::srv::SuctionPumpCtrl_Event_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      battery_lab_custom_msg::srv::SuctionPumpCtrl_Event_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<battery_lab_custom_msg::srv::SuctionPumpCtrl_Event_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<battery_lab_custom_msg::srv::SuctionPumpCtrl_Event_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<battery_lab_custom_msg::srv::SuctionPumpCtrl_Event_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__battery_lab_custom_msg__srv__SuctionPumpCtrl_Event
    std::shared_ptr<battery_lab_custom_msg::srv::SuctionPumpCtrl_Event_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__battery_lab_custom_msg__srv__SuctionPumpCtrl_Event
    std::shared_ptr<battery_lab_custom_msg::srv::SuctionPumpCtrl_Event_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SuctionPumpCtrl_Event_ & other) const
  {
    if (this->info != other.info) {
      return false;
    }
    if (this->request != other.request) {
      return false;
    }
    if (this->response != other.response) {
      return false;
    }
    return true;
  }
  bool operator!=(const SuctionPumpCtrl_Event_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SuctionPumpCtrl_Event_

// alias to use template instance with default allocator
using SuctionPumpCtrl_Event =
  battery_lab_custom_msg::srv::SuctionPumpCtrl_Event_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace battery_lab_custom_msg

namespace battery_lab_custom_msg
{

namespace srv
{

struct SuctionPumpCtrl
{
  using Request = battery_lab_custom_msg::srv::SuctionPumpCtrl_Request;
  using Response = battery_lab_custom_msg::srv::SuctionPumpCtrl_Response;
  using Event = battery_lab_custom_msg::srv::SuctionPumpCtrl_Event;
};

}  // namespace srv

}  // namespace battery_lab_custom_msg

#endif  // BATTERY_LAB_CUSTOM_MSG__SRV__DETAIL__SUCTION_PUMP_CTRL__STRUCT_HPP_
